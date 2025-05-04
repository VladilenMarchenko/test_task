from fastapi import APIRouter
from api.images.controller import router as images_router
from api.vectors.controller import router as vector_router

router = APIRouter(prefix="/api")

router.include_router(images_router)
router.include_router(vector_router)