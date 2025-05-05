import io
import mimetypes
from zipfile import ZipFile

import pillow_heif
from PIL import Image
from fastapi import HTTPException
from starlette import status
from starlette.datastructures import UploadFile

from api.file_manager.minio_helper import minio_helper

pillow_heif.register_heif_opener()

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/heic", "image/jpg"}


class ImageService:

    @staticmethod
    def read_image_from_bytes(image_bytes: bytes) -> Image.Image:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return image

    @staticmethod
    def validate_image(file: UploadFile):
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file type: {file.content_type}. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
            )

    @staticmethod
    async def save_images_from_zip(file: UploadFile):
        from core.kafka import send_one
        contents = await file.read()

        try:
            with ZipFile(io.BytesIO(contents)) as archive:
                for file_info in archive.infolist():
                    if file_info.is_dir():
                        continue

                    with archive.open(file_info.filename) as extracted_file:
                        data = extracted_file.read()

                        try:
                            Image.open(io.BytesIO(data)).verify()
                        except Exception:
                            continue

                        image_format = Image.open(io.BytesIO(data)).format.lower()
                        extension = mimetypes.guess_extension(image_format) or ".jpg"

                        original_name = file_info.filename.split("/")[-1]
                        upload_filename = original_name if original_name.lower().endswith(
                            (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif")
                        ) else original_name + extension

                        url = await minio_helper.upload_bytes_to_minio(
                            file_bytes=data,
                            original_filename=upload_filename,
                            extension=extension,
                            content_type=mimetypes.guess_type(upload_filename)[0] or "application/octet-stream"
                        )

                        await send_one(file_url=url, filename=upload_filename)

            return {"message": "All files successfully saved"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
