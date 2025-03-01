import asyncio
import os
import inspect
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from functools import partial
from lightrag.operate import chunking_by_token_size
from lightrag.prompt import PROMPTS

WORKING_DIR = "./dickens_ollama"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# def custom_chunking(content, split_by_character=None, split_by_character_only=False, chunk_token_size=250, chunk_overlap_token_size=0, tiktoken_model_name="gpt-4o-mini"):
#     chunks = content.split("\n")
#     return [{"content": chunk.strip(), "tokens": len(chunk.split()), "metadata": {"book_id": i}} for i, chunk in enumerate(chunks) if chunk.strip()]

custom_chunking = partial(
    chunking_by_token_size,
    split_by_character="\n",
    split_by_character_only=False,
    overlap_token_size=50,
    max_token_size=512,
    tiktoken_model="gpt-4o",
)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    llm_model_name="gemma2:9b",
    llm_model_max_async=4,
    llm_model_max_token_size=8192,
    llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 8192}},
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=8192,
        func=lambda texts: ollama_embed(
            texts, embed_model="nomic-embed-text", host="http://localhost:11434"
        ),
    ),
    chunking_func=custom_chunking
)


with open("./data/tiki_books_vn.txt", "r", encoding="utf-8") as f:
   rag.insert(f.read())
with open("./data/books_goodreads_en.txt", "r", encoding="utf-8") as f:
   rag.insert(f.read())


# Perform local search
input = "Sách Cây Cam Ngọt Của Tôi được sản xuất bởi nhà xuất bản nào?"
print("\n\n🔎🔎🔎 QUERY: " + input + "\n\n")

# Perform local search
print("\n🔎 **Truy vấn mode `LOCAL`** ...")
response = rag.query(input, param=QueryParam(mode="local", top_k=10), system_prompt=PROMPTS["universal_rag_response"])
print("\n🟢 **Kết quả (mode `LOCAL`):**\n" + response)

# Perform global search
print("\n🔎 **Truy vấn mode `GLOBAL`** ...")
response = rag.query(input, param=QueryParam(mode="global", top_k=10), system_prompt=PROMPTS["universal_rag_response"])
print("\n🟢 **Kết quả (mode `GLOBAL`):**\n" + response)

# Perform hybrid search
print("\n🔎 **Truy vấn mode `MIX`** ...")
response = rag.query(input, param=QueryParam(mode="mix", top_k=10), system_prompt=PROMPTS["universal_rag_response"])
print("\n🟢 **Kết quả (mode `MIX`):**\n" + response)

# stream response
resp = rag.query(input, param=QueryParam(mode="hybrid", stream=True), system_prompt=PROMPTS["universal_rag_response"])

async def print_stream(stream):
    async for chunk in stream:
        print(chunk, end="", flush=True)


if inspect.isasyncgen(resp):
    asyncio.run(print_stream(resp))
else:
    print(resp)
