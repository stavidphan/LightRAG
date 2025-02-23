import json

# Đọc file JSON chứa nhiều dòng
with open("./data/goodreads_books_comics_graphic.json", "r", encoding="utf-8") as f:
    books = [json.loads(line) for line in f]

# Tạo danh sách text để xây dựng Knowledge Graph
text_data = []
for book in books:
    title = book.get("title", "N/A")
    description = book.get("description", "N/A")
    average_rating = book.get("average_rating", "N/A")
    ratings_count = book.get("ratings_count", "N/A")
    num_pages = book.get("num_pages", "N/A")
    publication_year = book.get("publication_year", "N/A")
    publisher = book.get("publisher", "N/A")
    isbn = book.get("isbn", "N/A")
    isbn13 = book.get("isbn13", "N/A")
    language = book.get("language_code", "N/A")
    edition = book.get("edition_information", "N/A")
    series = book.get("series", "N/A")
    format_ = book.get("format", "N/A")
    genres = ", ".join([shelf.get("name", "Unknown") for shelf in book.get("popular_shelves", [])])    
    goodreads_link = book.get("link", "N/A")
    image_url = book.get("image_url", "N/A")

    # Xử lý danh sách tác giả
    authors = book.get("authors", [])
    author_names = [author.get("name", "Unknown Author") for author in authors]
    
    # Tạo các câu văn thể hiện mối quan hệ giữa các thực thể
    book_info = f"""
    The book "{title}" was written by {", ".join(author_names)} and published by {publisher} in {publication_year}.
    It has an average rating of {average_rating} based on {ratings_count} ratings.
    This book contains {num_pages} pages and is available in {language}.
    The book is part of the "{series}" series and follows the "{format_}" format.
    Genres include: {genres}.
    The ISBN of the book is {isbn} (ISBN-13: {isbn13}).
    More information can be found at {goodreads_link}.
    Cover image: {image_url}
    """

    text_data.append(book_info.strip())

# Ghi nội dung ra file TXT
with open("./data/books_goodreads_en.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(text_data))

print("✅ Dữ liệu đã được ghi vào ./data/books_goodreads_en.txt")