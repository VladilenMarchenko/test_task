from typing import Optional

from pydantic import BaseModel


class VectoredFile(BaseModel):
    vector: list[float]
    file_url: Optional[str] = None
    filename: Optional[str] = None