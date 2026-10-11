import time
import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.common.exceptions import BusinessException
from app.common.response import Response
from app.config import KB_ALLOWED_EXTENSIONS, KB_DIR
from app.schemas.kb import KbUploadResponse
from app.services import kb_service

router = APIRouter(prefix="/kb", tags=["知识库管理"])


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    """上传知识库文件"""
    if not file.filename:
        raise BusinessException(message="文件名不能为空")

    original_name = Path(file.filename).name
    ext = Path(original_name).suffix.lower()
    if ext not in KB_ALLOWED_EXTENSIONS:
        raise BusinessException(message=f"不支持的文件格式：{ext}，仅支持 txt/doc/docx/pdf/md")

    # 生成唯一的文件名
    disk_name = f"{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}{ext}"
    save_path = KB_DIR / disk_name

    # 保存文件
    content_bytes = await file.read()
    with open(save_path, "wb") as f:
        f.write(content_bytes)

    # 提取文本内容并加入向量库
    text = kb_service.extract_text_from_file(save_path, ext)
    if text:
        # 对于非 md/txt 文件，额外保存一份 .md 版本以便向量库索引
        if ext not in (".md", ".txt"):
            md_name = f"{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}.md"
            md_path = KB_DIR / md_name
            md_path.write_text(text, encoding="utf-8")
            kb_service.add_document(md_path.stem, text, md_path.name)
        else:
            kb_service.add_document(save_path.stem, text, save_path.name)

    preview = text[:200] if text else "(无文本内容)"
    return Response.success(
        data=KbUploadResponse(
            original_name=original_name,
            disk_name=disk_name,
            size=len(content_bytes),
            content_preview=preview,
        )
    )


@router.get("/files")
def list_files():
    """获取知识库文件列表"""
    if not KB_DIR.exists():
        return Response.success(data=[])
    files = []
    allowed_exts = KB_ALLOWED_EXTENSIONS
    for f in sorted(KB_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if f.suffix.lower() in allowed_exts and f.is_file():
            files.append({
                "name": f.name,
                "size": f.stat().st_size,
                "ext": f.suffix.lower(),
            })
    return Response.success(data=files)
