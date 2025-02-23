import asyncio
import inspect
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc

WORKING_DIR = "./dickens"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

# Khởi tạo LightRAG
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
)

# Hàm xử lý truy vấn với 3 mode
def ask_lightRAG(query):
    modes = ["local", "global", "mix"]
    responses = {}

    # Thực hiện truy vấn cho từng mode
    for mode in modes:
        print(f"\n🔎 **Truy vấn mode `{mode}`** ...")
        param = QueryParam(mode=mode, stream=True)  # Luôn bật stream để kiểm tra

        resp = rag.query(query, param=param)

        # Nếu là stream, xử lý bất đồng bộ
        if inspect.isasyncgen(resp):
            async def print_stream(mode, stream):
                print(f"\n🟢 **Kết quả (mode `{mode}`):**")
                async for chunk in stream:
                    print(chunk, end="", flush=True)
                print("\n" + "-" * 50)  # Ngăn cách giữa các mode
            asyncio.run(print_stream(mode, resp))

        # Nếu không phải stream, in trực tiếp
        else:
            responses[mode] = resp

    # In các kết quả không phải stream
    for mode, result in responses.items():
        print(f"\n🟢 **Kết quả (mode `{mode}`):**\n{result}\n" + "-" * 50)


# Vòng lặp nhập câu hỏi
while True:
    query = input("\n💬 Nhập câu hỏi của bạn (hoặc gõ 'exit' để thoát): ")
    if query.lower() == "exit":
        break
    ask_lightRAG(query)