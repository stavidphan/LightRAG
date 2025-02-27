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

    # Tạo danh sách các câu văn thể hiện thông tin sách
    sentences = []

    if title and authors:
        sentences.append(f'The book "{title}" was written by {", ".join(author_names)}.')
    if title and publisher and publication_year:
        sentences.append(f'The book "{title}" was published by {publisher} in {publication_year}.')
    if title and average_rating and ratings_count:
        sentences.append(f'The book "{title}" has an average rating of {average_rating} based on {ratings_count} ratings.')
    if title and num_pages:
        sentences.append(f'The book "{title}" contains {num_pages} pages.')
    if title and language:
        sentences.append(f'The book "{title}" is available in {language}.')
    if title and series:
        sentences.append(f'The book "{title}" is part of the "{series}" series.')
    if title and format_:
        sentences.append(f'The book "{title}" follows the "{format_}" format.')
    if title and genres:
        sentences.append(f'The book "{title}" belongs to the genres: {genres}.')
    if title and isbn and isbn13:
        sentences.append(f'The ISBN of the book "{title}" is {isbn} (ISBN-13: {isbn13}).')
    if title and goodreads_link:
        sentences.append(f'More information about "{title}" can be found at {goodreads_link}.')
    if title and image_url:
        sentences.append(f'The cover image of the book "{title}" is available at {image_url}.')

    text_data.extend(sentences)

# Ghi nội dung ra file TXT
with open("./data/books_goodreads_en.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(text_data))

print("✅ Data has been saved to ./data/books_goodreads_en.txt")

####---------------------------------JSON Fomat-------------------------------------------------------------------####
# import json

# def preprocess_book_data(input_file, output_file):
#     # Đọc file JSON chứa nhiều dòng
#     with open(input_file, "r", encoding="utf-8") as f:
#         books = [json.loads(line) for line in f]

#     # Tạo danh sách text để xây dựng Knowledge Graph
#     text_data = []
#     for book in books:
#         # Trích xuất các trường, mặc định là chuỗi rỗng nếu không có
#         title = book.get("title", "")
#         description = book.get("description", "")
#         average_rating = book.get("average_rating", "")
#         ratings_count = book.get("ratings_count", "")
#         num_pages = book.get("num_pages", "")
#         publication_year = book.get("publication_year", "")
#         publisher = book.get("publisher", "")
#         isbn = book.get("isbn", "")
#         isbn13 = book.get("isbn13", "")
#         language = book.get("language_code", "")
#         series = book.get("series", "")
#         format_ = book.get("format", "")
#         genres = ", ".join([shelf.get("name", "Unknown") for shelf in book.get("popular_shelves", [])])
#         goodreads_link = book.get("link", "")

#         # Xử lý danh sách tác giả
#         authors = book.get("authors", [])
#         author_names = ", ".join([author.get("name", "Unknown Author") for author in authors])

#         # Tạo khối văn bản key-value ngắn gọn, chỉ giữ các trường có giá trị
#         book_info_lines = []
#         if title:
#             book_info_lines.append(f"Title: {title}")
#         if author_names:
#             book_info_lines.append(f"Authors: {author_names}")
#         if publisher:
#             book_info_lines.append(f"Publisher: {publisher}")
#         if publication_year:
#             book_info_lines.append(f"Year: {publication_year}")
#         if average_rating and ratings_count:
#             book_info_lines.append(f"Rating: {average_rating} ({ratings_count} ratings)")
#         if num_pages:
#             book_info_lines.append(f"Pages: {num_pages}")
#         if language:
#             book_info_lines.append(f"Language: {language}")
#         if series and series != "N/A":
#             book_info_lines.append(f"Series: {series}")
#         if format_ and format_ != "N/A":
#             book_info_lines.append(f"Format: {format_}")
#         if genres:
#             book_info_lines.append(f"Genres: {genres}")
#         if isbn or isbn13:
#             book_info_lines.append(f"ISBN: {isbn or isbn13}")
#         if goodreads_link:
#             book_info_lines.append(f"Link: {goodreads_link}")

#         # Nối các dòng thành một khối
#         book_info = "\n".join(book_info_lines)
#         if book_info:
#             text_data.append(book_info)

#     # Ghi nội dung ra file TXT
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write("\n\n".join(text_data))

#     print(f"✅ Dữ liệu đã được ghi vào {output_file}")

# # Ví dụ sử dụng
# preprocess_book_data("./data/goodreads_books_comics_graphic.json", "./data/books_goodreads_json.txt")