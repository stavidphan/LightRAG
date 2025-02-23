import json

# Đọc dữ liệu đã lọc
with open("filtered_books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

# Chuyển dữ liệu thành dạng text để insert vào LightRAG
text_data = []
for book in books:
    text_data.append(f"""
Title: {book.get("title", "N/A")}
Description: {book.get("description", "N/A")}
Average Rating: {book.get("average_rating", "N/A")}
Ratings Count: {book.get("ratings_count", "N/A")}
Number of Pages: {book.get("num_pages", "N/A")}
Authors: {", ".join(book.get("authors", []))}
Publication Year: {book.get("publication_year", "N/A")}
Publisher: {book.get("publisher", "N/A")}
Goodreads Link: {book.get("link", "N/A")}
Cover Image: {book.get("image_url", "N/A")}
"""  
    )

# Ghi nội dung ra file TXT
with open("book.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(text_data))

print("✅ Dữ liệu đã được ghi vào book.txt")