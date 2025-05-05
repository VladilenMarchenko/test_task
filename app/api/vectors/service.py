from uuid import uuid4

from fastapi import UploadFile, HTTPException
from torchvision import models, transforms
import torch

from api.file_manager.minio_helper import minio_helper
from api.images.service import ImageService
from api.vectors.schema import VectoredFile
from core.elastic import es_helper

model = models.resnet50()
model.eval()
torch.set_num_threads(2)

model = torch.nn.Sequential(*list(model.children())[:-1])

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class VectorService:

    @staticmethod
    async def vectorize_from_file(file: UploadFile):
        try:

            file_bytes = await file.read()
            prepared_file = ImageService.read_image_from_bytes(image_bytes=file_bytes)

            input_tensor = preprocess(prepared_file).unsqueeze(0)
            with torch.no_grad():
                vector = model(input_tensor).squeeze().tolist()

            return VectoredFile(
                vector=vector,
                filename=file.filename
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def vectorize_from_url(file_url: str):
        try:
            file_bytes = minio_helper.download_file_as_bytes(file_name=file_url)
            prepared_file = ImageService.read_image_from_bytes(file_bytes)

            input_tensor = preprocess(prepared_file).unsqueeze(0)
            with torch.no_grad():
                vector = model(input_tensor).squeeze().tolist()

            return VectoredFile(
                vector=vector,
                file_url=file_url
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def save_vector_to_elasticsearch(original_filename: str, vector: list[float], file_url: str):
        doc = {
            "file_url": file_url,
            "original_filename": original_filename,
            "vector": vector
        }
        doc_id = str(uuid4())
        await es_helper.es_client.index(index="image_vectors", id=doc_id, document=doc)
        return doc_id
