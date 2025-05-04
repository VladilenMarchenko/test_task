from fastapi import APIRouter, File, UploadFile, HTTPException

from api.file_manager.minio_helper import minio_helper
from api.images.service import ImageService
from api.vectors.service import VectorService
from core.elastic import es_helper

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/save-image")
async def save_image(file: UploadFile):
    return await  minio_helper.upload_file_to_minio(file=file)


@router.post("/vectorize", description="Vectorize and save one image")
async def vectorize_image(file: UploadFile):
    ImageService.validate_image(file)

    file_url = await minio_helper.upload_file_to_minio(
        file=file
    )

    vectored_file = await VectorService.vectorize_from_url(
        file_url=file_url
    )

    doc_id = await VectorService.save_vector_to_elasticsearch(
        vector=vectored_file.vector,
        file_url=file_url,
        original_filename=file.filename
    )

    return {"doc_id": doc_id, "file_url": file_url, "vectored_file": vectored_file}


@router.post("/find", description="Find image by another image")
async def find_similar_images(file: UploadFile = File(...)):
    ImageService.validate_image(file)
    vectored_file = await VectorService.vectorize_from_file(file=file)
    return await es_helper.search_similar_images(vector=vectored_file.vector)


@router.get(
    "/{file_name}",
    description="Get file by id"
)
def get_file_by_name(file_name: str):
    return minio_helper.download_file(file_name=file_name)


@router.post("/process-data-set", description="Process .zip with data set of images, uses Kafka")
async def process_data_set(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="File must be a .zip archive")

    return await ImageService.save_images_from_zip(file=file)
