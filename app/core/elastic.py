from elasticsearch import AsyncElasticsearch

from core.config import settings


class ElasticHelper:
    def __init__(
            self,
            hosts: str,
    ):
        self.es_client: AsyncElasticsearch = AsyncElasticsearch(
            hosts=hosts,
        )

    async def init_images_index(self):
        exists = await self.es_client.indices.exists(index="image_vectors")
        if not exists:
            await self.es_client.indices.create(index="image_vectors", body={
                "mappings": {
                    "properties": {
                        "filename": {"type": "keyword"},
                        "vector": {
                            "type": "dense_vector",
                            "dims": 2048,
                            "index": True,
                            "similarity": "cosine"
                        }
                    }
                }
            })

    async def search_similar_images(self, vector: list[float], k: int = 5):
        query = {
            "knn": {
                "field": "vector",
                "query_vector": vector,
                "k": k,
                "num_candidates": 10*k
            },
            "fields": [
                "file_url", "original_filename"
            ],
        }

        response = await self.es_client.search(index="image_vectors", body=query)
        return {"result": [
            {
                "file_url": hit["_source"]["file_url"],
                "original_filename": hit["_source"]["original_filename"],
                "score": hit["_score"]
            }
            for hit in response["hits"]["hits"]
        ], "vector": vector}

    async def count_vectors(self, index_name: str):
        response = await self.es_client.count(
            index=index_name,
            body={
                "query": {
                    "exists": {
                        "field": "vector"
                    }
                }
            }
        )
        return response["count"]


es_helper = ElasticHelper(hosts=settings.elastic.endpoint)
