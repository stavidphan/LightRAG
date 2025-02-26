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

def custom_chunking(text):
    chunks = text.split("\n\n")
    return [{"text": chunk.strip(), "metadata": {"book_id": i}} for i, chunk in enumerate(chunks) if chunk.strip()]

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    llm_model_name="gemma2:2b",
    llm_model_max_async=4,
    llm_model_max_token_size=8192,
    llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 8192}},
    embedding_func=EmbeddingFunc(
        embedding_dim=1024,
        max_token_size=512,
        func=lambda texts: ollama_embed(
            texts, embed_model="zylonai/multilingual-e5-large", host="http://localhost:11434"
        ),
    ),
    chunking_func=custom_chunking,
    embedding_batch_num=16,  # Batch size cho embedding
    llm_response_cache=True,  # Bật cache cho LLM
)

with open("./data/tiki_books_vn.txt", "r", encoding="utf-8") as f:
   rag.insert(f.read())

with open("./data/books_goodreads_en.txt", "r", encoding="utf-8") as f:
   rag.insert(f.read())

# Prompt tùy chỉnh cho chatbot tư vấn bán sách
system_prompt = """
Bạn là chatbot tư vấn bán sách trên sàn thương mại điện tử. Hãy trả lời câu hỏi của người dùng một cách nhanh chóng, chính xác và đầy đủ thông tin, bao gồm tiêu đề sách, tác giả, nhà xuất bản, thể loại, giá cả, nhà bán và các gợi ý liên quan nếu cần.
"""

# Perform local search
input = "Sách Cây Cam Ngọt Của Tôi được sản xuất bởi nhà xuất bản nào?"
print("\n\n🔎🔎🔎 QUERY: " + input + "\n\n")

# Perform local search
print("\n🔎 **Truy vấn mode `LOCAL`** ...")
response = rag.query(input, param=QueryParam(mode="local", top_k=5), system_prompt=system_prompt)
print("\n🟢 **Kết quả (mode `LOCAL`):**\n" + response)

# Perform global search
print("\n🔎 **Truy vấn mode `GLOBAL`** ...")
response = rag.query(input, param=QueryParam(mode="global", top_k=5), system_prompt=system_prompt)
print("\n🟢 **Kết quả (mode `GLOBAL`):**\n" + response)

# Perform hybrid search
print("\n🔎 **Truy vấn mode `MIX`** ...")
response = rag.query(input, param=QueryParam(mode="mix", top_k=5), system_prompt=system_prompt)
print("\n🟢 **Kết quả (mode `MIX`):**\n" + response)

# stream response
resp = rag.query(
    input,
    param=QueryParam(mode="hybrid", stream=True),
    system_prompt=system_prompt
)

async def print_stream(stream):
    async for chunk in stream:
        print(chunk, end="", flush=True)


if inspect.isasyncgen(resp):
    asyncio.run(print_stream(resp))
else:
    print(resp)
