from fastapi import APIRouter

from core.elastic import es_helper

router = APIRouter(prefix="/vectors", tags=["Vectors"])


@router.get("/count")
async def get_count_data(index_name:str):
    return await es_helper.count_vectors(index_name=index_name)