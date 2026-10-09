import os

# huggingface_hub 在 import 时就会读取 HF_ENDPOINT，因此必须赶在 chromadb /
# sentence_transformers 之前设置。国内网络直连 huggingface.co 会超时
# (WinError 10060)，默认走镜像站下载 bge-small-zh-v1.5。
# 需要覆盖时，在启动前设置同名环境变量即可。
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
