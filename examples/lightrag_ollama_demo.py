import asyncio
import os
import inspect
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc

WORKING_DIR = "./dickens_ollama"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

def custom_chunking(content, split_by_character=None, split_by_character_only=False, chunk_token_size=250, chunk_overlap_token_size=0, tiktoken_model_name="gpt-4o-mini"):
    lines = content.split("\n")
    chunks = []
    current_chunk = []
    
    for line in lines:
        if line.strip():  # Nếu dòng không trống
            current_chunk.append(line)
        else:  # Nếu dòng trống, kết thúc một khối văn bản
            if current_chunk:
                chunk_content = "\n".join(current_chunk)
                chunks.append({"tokens": len(chunk_content.split()), "content": chunk_content})
                current_chunk = []
    
    # Thêm khối văn bản cuối cùng nếu có
    if current_chunk:
        chunk_content = "\n".join(current_chunk)
        chunks.append({"tokens": len(chunk_content.split()), "content": chunk_content})
    
    return chunks


rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    llm_model_name="qwen2m",
    llm_model_max_async=4,
    llm_model_max_token_size=32768,
    llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 32768}},
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=8192,
        func=lambda texts: ollama_embed(
            texts, embed_model="nomic-embed-text", host="http://localhost:11434"
        ),
    ),
    chunking_func=custom_chunking
)

#with open("./data/tiki_books_vn.txt", "r", encoding="utf-8") as f:
 #   rag.insert(f.read())

#with open("./data/books_goodreads_en.txt", "r", encoding="utf-8") as f:
 #   rag.insert(f.read())

# Perform local search

input = "Mua sách Bản Đồ ở đâu?"
print("\nQUERY: " + input "\n\n")

# Perform local search
print("\n🔎 **Truy vấn mode `LOCAL`** ...")
response = rag.query(input, param=QueryParam(mode="local"))
print("\n🟢 **Kết quả (mode `LOCAL`):**\n" + response)

# Perform global search
print("\n🔎 **Truy vấn mode `GLOBAL`** ...")
response = rag.query(input, param=QueryParam(mode="global"))
print("\n🟢 **Kết quả (mode `GLOBAL`):**\n" + response)

# Perform hybrid search
print("\n🔎 **Truy vấn mode `MIX** ...")
response = rag.query(input, param=QueryParam(mode="mix"))
print("\n🟢 **Kết quả (mode `MIX`):**\n" + response)

# stream response
resp = rag.query(
    input,
    param=QueryParam(mode="hybrid", stream=True),
)

async def print_stream(stream):
    async for chunk in stream:
        print(chunk, end="", flush=True)


if inspect.isasyncgen(resp):
    asyncio.run(print_stream(resp))
else:
    print(resp)
