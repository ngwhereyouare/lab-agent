from fastapi import File
from pydantic import BaseModel


class FileResponse(BaseModel):
    orignal_name: str
    disk_name: str
    size: int
    url: str
