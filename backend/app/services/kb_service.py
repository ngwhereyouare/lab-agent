from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.utils import embedding_functions

from app.config import BASE_DIR, KB_DIR

CHROMA_DIR = BASE_DIR / "data" / "chroma"
EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"

_collection = None

_embedding_fn = None


def get_embedding_fn():
    """惰加载 embedding 模型：只加载一次，之后复用同一个实例"""
    global _embedding_fn
    if _embedding_fn is not None:
        return _embedding_fn
    _embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )
    return _embedding_fn


def get_collcetion() -> Collection:
    """向量库的初始化"""
    global _collection
    if _collection is not None:
        return _collection
    KB_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    col = client.get_or_create_collection(
        name="lab_kb", embedding_function=get_embedding_fn()
    )
    if col.count() == 0:
        ids = []
        docs = []
        metas = []
        for path in sorted(KB_DIR.glob("*")):
            if path.suffix.lower() not in (".md", ".txt"):
                continue
            text = path.read_text(encoding="UTF-8").strip()
            if not text:
                continue
            docs.append(text)
            ids.append(path.stem)
            metas.append({"source": path.name})
        if docs:
            col.add(ids=ids, documents=docs, metadatas=metas)
    _collection = col
    return col


def warmup():
    """启动时预热"""
    col = get_collcetion()
    if col.count() > 0:
        col.query(query_texts=["预热"], n_results=1)


def search(query: str):
    """根据关键字去检索向量库"""
    col = get_collcetion()
    if col.count() == 0:
        return ""
    limit = min(5, col.count())
    res = col.query(query_texts=[query], n_results=limit)
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    distances = (res.get("distances") or [[]])[0]

    score_parts = []
    for doc, m, dist in zip(docs, metas, distances):
        score = 1 / (1 + dist)
        if score < 0.5:
            continue
        name = m.get("source") or ""
        score_parts.append({"score": score, "content": f"[{name}]\n{doc}"})
    score_parts.sort(key=lambda x: x["score"], reverse=True)
    final_parts = [item["content"] for item in score_parts[:2]]
    return "\n\n".join(final_parts)


def extract_text_from_file(file_path: Path, original_ext: str) -> str:
    """从上传的文件中提取文本内容"""
    ext = original_ext.lower()
    if ext == ".md":
        return file_path.read_text(encoding="utf-8", errors="replace")
    elif ext == ".txt":
        return file_path.read_text(encoding="utf-8", errors="replace")
    elif ext == ".pdf":
        return _extract_pdf_text(file_path)
    elif ext in (".doc", ".docx"):
        return _extract_docx_text(file_path)
    return ""


def _extract_pdf_text(file_path: Path) -> str:
    try:
        import fitz
    except ImportError:
        return ""
    doc = fitz.open(file_path)
    parts = []
    for page in doc:
        parts.append(page.get_text())
    doc.close()
    return "\n".join(parts)


def _extract_docx_text(file_path: Path) -> str:
    try:
        import docx
    except ImportError:
        return ""
    doc = docx.Document(str(file_path))
    return "\n".join(p.text for p in doc.paragraphs)


def add_document(disk_name: str, content: str, source_name: str):
    """将新的文档添加到向量库中"""
    col = get_collcetion()
    existing = col.get(ids=[disk_name])
    if existing and existing.get("ids"):
        col.update(ids=[disk_name], documents=[content], metadatas=[{"source": source_name}])
    else:
        col.add(ids=[disk_name], documents=[content], metadatas=[{"source": source_name}])
