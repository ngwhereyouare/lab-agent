from pydantic import BaseModel


class KbUploadResponse(BaseModel):
    original_name: str
    disk_name: str
    size: int
    content_preview: str
