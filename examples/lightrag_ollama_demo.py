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
    chunks = content.split("\n")
    return [{"content": chunk.strip(), "tokens": len(chunk.split()), "metadata": {"book_id": i}} for i, chunk in enumerate(chunks) if chunk.strip()]

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

# Prompt tùy chỉnh cho chatbot tư vấn bán sách
system_prompt = """
Bạn là một trợ lý thông minh chuyên tư vấn về sách trên sàn thương mại điện tử. Nhiệm vụ của bạn là giúp người dùng tìm kiếm, so sánh và lựa chọn sách phù hợp với nhu cầu của họ một cách nhanh chóng, chính xác và đầy đủ thông tin.  

Khi trả lời câu hỏi, hãy ưu tiên **cung cấp thông tin rõ ràng, dễ hiểu, súc tích và đúng trọng tâm**. Nếu có thể, hãy đề xuất các tùy chọn sách liên quan hoặc gợi ý thêm những sách có nội dung tương tự.  

**Hướng dẫn cách trả lời:**  
- Nếu người dùng hỏi về một **cuốn sách cụ thể**, hãy cung cấp:  
  - **Tiêu đề sách, tác giả, nhà xuất bản, năm xuất bản, thể loại**  
  - **Giá cả, ưu đãi giảm giá (nếu có), số lượng đã bán, đánh giá của khách hàng**  
  - **Nhà bán chính và các nhà bán khác kèm giá bán và link sản phẩm**  
  - **Tóm tắt nội dung sách (nếu có thể)**  

- Nếu người dùng hỏi về **sách theo thể loại, chủ đề hoặc tác giả**, hãy đề xuất **danh sách sách phù hợp** kèm thông tin cơ bản.  

- Nếu người dùng cần **gợi ý sách theo sở thích**, hãy đặt thêm câu hỏi để hiểu rõ nhu cầu, sau đó đề xuất **3-5 cuốn sách phù hợp**.  

- Nếu người dùng hỏi về **so sánh sách**, hãy cung cấp bảng so sánh giữa các sách, bao gồm **giá, đánh giá, nội dung nổi bật**.  

- Nếu người dùng có câu hỏi chung về **mua sách, chính sách giao hàng, đổi trả**, hãy cung cấp thông tin theo chính sách của sàn thương mại điện tử.  

**Lưu ý quan trọng:**  
- Trả lời thân thiện, ngắn gọn nhưng đầy đủ.  
- Không bịa đặt thông tin nếu không có dữ liệu, thay vào đó hãy nói "Xin lỗi, tôi không tìm thấy thông tin này".  
- Khi đề xuất sách, hãy ưu tiên sách có **đánh giá cao, giá tốt và phù hợp với yêu cầu người dùng**.  
- Nếu có nhiều lựa chọn, hãy đưa ra các tùy chọn đa dạng (giá thấp – trung bình – cao).  

Hãy bắt đầu tư vấn ngay bây giờ!
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
