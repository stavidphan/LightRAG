# import pandas as pd
# import json

# # Đọc file Excel
# try:
#     df = pd.read_excel("./data/tiki_books_vn.xlsx", engine="openpyxl")
# except FileNotFoundError:
#     print("File không tồn tại.")
#     exit()

# # Hàm tạo câu mô tả sách
# def generate_book_description(row):
#     name = row["Name"]
#     price = row["Price (vnd)"]
#     discount = row["Discount (%)"]
#     sold = row["Sold"]
#     rating = row["Rating"]
#     publisher = ", ".join(eval(row["Publisher"])) if isinstance(row["Publisher"], str) else row["Publisher"]
#     manufacturer = ", ".join(eval(row["Manufacturer"])) if isinstance(row["Manufacturer"], str) else row["Manufacturer"]
#     authors = ", ".join(eval(row["Authors"])) if isinstance(row["Authors"], str) else row["Authors"]
#     link = row["Link"]

#     # Xử lý cột Other_sellers
#     try:
#         sellers_info = json.loads(row["Other_sellers"].replace("'", '"'))  # Chuyển chuỗi JSON về list
#         sellers_text = "; ".join([
#             f"{s['name']} với giá {s['price']} VND (link: {s['link']})" for s in sellers_info
#         ])
#     except:
#         sellers_text = "Không có thông tin nhà bán khác."

#     return {
#         "name": name,
#         "price": price,
#         "discount": discount,
#         "sold": sold,
#         "rating": rating,
#         "publisher": publisher,
#         "manufacturer": manufacturer,
#         "authors": authors,
#         "link": link,
#         "sellers": sellers_text
#     }

# # Chuyển đổi từng dòng thành mô tả văn bản
# data = df.apply(generate_book_description, axis=1).tolist()

# # Tạo mô tả văn bản cho LightRAG
# text_data = []
# for book in data:
#     text = f"""Sách "{book["name"]}" có giá {book["price"]} VND với mức giảm giá {book["discount"]}%. 
#     Hiện đã bán được {book["sold"]} bản và có đánh giá trung bình {book["rating"]} sao.
#     Nhà xuất bản là {book["publisher"]}. Sản xuất bởi {book["manufacturer"]}.
#     Tác giả là {book["authors"]}. Sản phẩm được bán tại {book["link"]}.
#     Các nhà bán khác: {book["sellers"]}.
# """
#     text_data.append(text)

# # Xuất ra file text để nạp vào LightRAG
# with open("./data/tiki_books_vn.txt", "w", encoding="utf-8") as f:
#     f.write("\n".join(text_data))


##------------------------------JSON FORMAT----------------------------------------------------------------------------------------##
import pandas as pd
import json

# Đọc file Excel
try:
    df = pd.read_excel("./data/tiki_books_vn.xlsx", engine="openpyxl")
except FileNotFoundError:
    print("File không tồn tại.")
    exit()

# Hàm tạo mô tả sách dạng key-value
def generate_book_description(row):
    name = row["Name"] if pd.notna(row["Name"]) else ""
    price = str(row["Price (vnd)"]) + " VND" if pd.notna(row["Price (vnd)"]) else ""
    discount = str(row["Discount (%)"]) + "%" if pd.notna(row["Discount (%)"]) else ""
    sold = str(row["Sold"]) if pd.notna(row["Sold"]) else ""
    rating = str(row["Rating"]) if pd.notna(row["Rating"]) else ""
    publisher = ", ".join(eval(row["Publisher"])) if isinstance(row["Publisher"], str) and row["Publisher"] else ""
    manufacturer = ", ".join(eval(row["Manufacturer"])) if isinstance(row["Manufacturer"], str) and row["Manufacturer"] else ""
    authors = ", ".join(eval(row["Authors"])) if isinstance(row["Authors"], str) and row["Authors"] else ""
    link = row["Link"] if pd.notna(row["Link"]) else ""

    # Xử lý cột Other_sellers
    try:
        sellers_info = json.loads(row["Other_sellers"].replace("'", '"'))
        sellers = [{"name": s["name"], "price": s["price"], "link": s["link"]} for s in sellers_info]
    except:
        sellers = []

    # Tạo khối văn bản key-value
    book_info_lines = []
    if name:
        book_info_lines.append(f"Title: {name}")
    if authors:
        book_info_lines.append(f"Authors: {authors}")
    if publisher:
        book_info_lines.append(f"Publisher: {publisher}")
    if manufacturer:
        book_info_lines.append(f"Manufacturer: {manufacturer}")
    if price:
        book_info_lines.append(f"Price: {price}")
    if discount:
        book_info_lines.append(f"Discount: {discount}")
    if sold:
        book_info_lines.append(f"Sold: {sold}")
    if rating:
        book_info_lines.append(f"Rating: {rating}")
    if link:
        book_info_lines.append(f"Link: {link}")
    
    # Xử lý Other_sellers thành từng dòng riêng
    for seller in sellers:
        book_info_lines.append(f"Seller: {seller['name']} with price {seller['price']} VND (link: {seller['link']})")

    return "\n".join(book_info_lines)

# Chuyển đổi từng dòng thành mô tả văn bản
text_data = df.apply(generate_book_description, axis=1).tolist()

# Xuất ra file text để nạp vào LightRAG
output_file = "./data/tiki_books_json.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n\n".join(text_data))

print(f"✅ Dữ liệu đã được ghi vào {output_file}")