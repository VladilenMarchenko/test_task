import io
import mimetypes
import os
import sys
import time
import uuid
import urllib3
from fastapi import UploadFile, HTTPException
from minio import Minio, S3Error
from starlette.responses import StreamingResponse

from core.config import settings
from core.logger_config import get_logger

minio_logger = get_logger(__name__)


class MiniOHelper:
    def __init__(
            self,
            endpoint: str,
            access_key: str,
            secret_key: str,
            bucket_name: str,
            secure: bool = False
    ):
        self.minio_client: Minio = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def ensure_bucket_exists(self, retry_attempts=5, retry_delay=1):
        attempt = 0
        while attempt < retry_attempts:
            try:
                if not self.minio_client.bucket_exists(settings.miniO.bucket_name):
                    self.minio_client.make_bucket(settings.miniO.bucket_name)
                minio_logger.info(f"✅ MinIO bucket '{settings.miniO.bucket_name}' is ready!")
                return
            except (urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError, S3Error) as e:
                attempt += 1
                minio_logger.warning(f"⚠️ [Attempt {attempt}/{retry_attempts}] Failed to connect to MinIO: {e}")
                time.sleep(retry_delay)
        minio_logger.critical("❌ Could not connect to MinIO after multiple attempts. Shutting down...")
        sys.exit(status="Couldn`t connect miniO.")

    async def upload_file_to_minio(self, file: UploadFile) -> str:
        try:
            file_data = await file.read()
            file_stream = io.BytesIO(file_data)

            extension = os.path.splitext(file.filename)[1] or ""
            unique_name = f"{int(time.time())}_{uuid.uuid4().hex}{extension}"

            self.minio_client.put_object(
                settings.miniO.bucket_name,
                unique_name,
                file_stream,
                length=len(file_data),
                content_type=file.content_type
            )

            minio_logger.info(f"File {unique_name} saved!")
            return unique_name

        except S3Error as e:
            minio_logger.exception("S3Error")
            raise HTTPException(status_code=500, detail=f"MinIO Error: {str(e)}")
        except Exception as e:
            minio_logger.exception("Exception")
            raise HTTPException(status_code=500, detail=str(e))

    async def remove_file_from_minio(self, file_name: str):
        self.minio_client.remove_object(settings.miniO.bucket_name, file_name)
        minio_logger.info(f"File: {file_name} was removed")

    def download_file(self, file_name: str):
        try:
            response = self.minio_client.get_object(settings.miniO.bucket_name, file_name)

            return StreamingResponse(
                iter(lambda: response.read(1024 * 1024), b""),
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={file_name}"}
            )

        except S3Error as e:
            if e.code == "NoSuchKey":
                raise HTTPException(status_code=404, detail="File not found in storage.")
            else:
                minio_logger.exception("S3Error")
                raise HTTPException(status_code=500, detail=f"MinIO Error: {str(e)}")
        except Exception as e:
            minio_logger.exception("Exception")
            raise HTTPException(status_code=500, detail=str(e))

    def download_file_as_bytes(self, file_name: str):
        response = self.minio_client.get_object(settings.miniO.bucket_name, file_name)
        return response.read()

    async def upload_bytes_to_minio(
            self,
            file_bytes: bytes,
            original_filename: str,
            extension: str,
            content_type: str | None = None
    ) -> str:
        if not content_type:
            content_type = mimetypes.guess_type(original_filename)[0] or "application/octet-stream"

        unique_name = f"{int(time.time())}_{uuid.uuid4().hex}{extension}"
        file_stream = io.BytesIO(file_bytes)

        self.minio_client.put_object(
            bucket_name=settings.miniO.bucket_name,
            object_name=unique_name,
            data=file_stream,
            length=len(file_bytes),
            content_type=content_type
        )

        minio_logger.info(f"File {unique_name} saved from raw bytes.")
        return unique_name


minio_helper = MiniOHelper(
    endpoint=settings.miniO.endpoint,
    access_key=settings.miniO.access_key,
    secret_key=settings.miniO.secret_key,
    secure=settings.miniO.secure,
    bucket_name=settings.miniO.bucket_name
)
