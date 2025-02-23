import json

# Đọc file JSON chứa nhiều dòng
with open("./goodreads_books_comics_graphic.json", "r", encoding="utf-8") as f:
    books = [json.loads(line) for line in f]

# Chỉ giữ lại các trường quan trọng
filtered_books = []
for book in books:
    filtered_books.append({
        "title": book.get("title", ""),
        "description": book.get("description", ""),
        "average_rating": book.get("average_rating", ""),
        "ratings_count": book.get("ratings_count", ""),
        "num_pages": book.get("num_pages", ""),
        "authors": [author.get("author_id", "") for author in book.get("authors", [])],
        "publication_year": book.get("publication_year", ""),
        "publisher": book.get("publisher", ""),
        "link": book.get("link", ""),
        "image_url": book.get("image_url", ""),
    })

# Lưu lại file JSON mới
with open("filtered_books.json", "w", encoding="utf-8") as f:
    json.dump(filtered_books, f, indent=4, ensure_ascii=False)

print("Lọc dữ liệu thành công! ✅ File filtered_books.json đã được tạo.")
