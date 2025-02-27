import pandas as pd
import json

# Đọc file Excel
try:
    df = pd.read_excel("./data/tiki_books_vn.xlsx", engine="openpyxl")
except FileNotFoundError:
    print("File không tồn tại.")
    exit()

# Hàm tạo danh sách câu mô tả sách
def generate_book_sentences(row):
    sentences = []
    
    name = row["Name"] if pd.notna(row["Name"]) else ""
    price = f"{row['Price (vnd)']} VND" if pd.notna(row["Price (vnd)"]) else ""
    discount = f"{row['Discount (%)']}%" if pd.notna(row["Discount (%)"]) else ""
    sold = f"{row['Sold']} bản" if pd.notna(row["Sold"]) else ""
    rating = f"{row['Rating']} sao" if pd.notna(row["Rating"]) else ""
    publisher = ", ".join(eval(row["Publisher"])) if isinstance(row["Publisher"], str) else ""
    manufacturer = ", ".join(eval(row["Manufacturer"])) if isinstance(row["Manufacturer"], str) else ""
    authors = ", ".join(eval(row["Authors"])) if isinstance(row["Authors"], str) else ""
    link = row["Link"] if pd.notna(row["Link"]) else ""

    if name and price:
        sentences.append(f'Sách "{name}" có giá {price}.')
    if name and discount:
        sentences.append(f'Sách "{name}" có mức giảm giá {discount}.')
    if name and sold:
        sentences.append(f'Sách "{name}" hiện đã bán được {sold}.')
    if name and rating:
        sentences.append(f'Sách "{name}" có đánh giá trung bình {rating}.')
    if name and publisher:
        sentences.append(f'Sách "{name}" được xuất bản bởi {publisher}.')
    if name and manufacturer:
        sentences.append(f'Sách "{name}" được sản xuất bởi {manufacturer}.')
    if name and authors:
        sentences.append(f'Sách "{name}" được viết bởi {authors}.')
    if name and link:
        sentences.append(f'Sách "{name}" có thể mua tại {link}.')

    # Xử lý thông tin nhà bán khác
    try:
        sellers_info = json.loads(row["Other_sellers"].replace("'", '"'))  # Chuyển chuỗi JSON về list
        for s in sellers_info:
            sentences.append(f'Sách "{name}" cũng được bán bởi {s["name"]} với giá {s["price"]} VND (link: {s["link"]}).')
    except:
        pass  # Nếu không có dữ liệu nhà bán khác thì bỏ qua

    return sentences

# Chuyển đổi từng dòng thành danh sách câu văn
text_data = []
for _, row in df.iterrows():
    text_data.extend(generate_book_sentences(row))

# Xuất ra file text để nạp vào LightRAG
with open("./data/tiki_books_vn.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(text_data))

print("✅ Dữ liệu đã được ghi vào ./data/tiki_books_vn.txt với từng câu trên một dòng.")


##------------------------------JSON FORMAT----------------------------------------------------------------------------------------##
# import pandas as pd
# import json

# # Đọc file Excel
# try:
#     df = pd.read_excel("./data/tiki_books_vn.xlsx", engine="openpyxl")
# except FileNotFoundError:
#     print("File không tồn tại.")
#     exit()

# # Hàm tạo mô tả sách dạng key-value
# def generate_book_description(row):
#     name = row["Name"] if pd.notna(row["Name"]) else ""
#     price = str(row["Price (vnd)"]) + " VND" if pd.notna(row["Price (vnd)"]) else ""
#     discount = str(row["Discount (%)"]) + "%" if pd.notna(row["Discount (%)"]) else ""
#     sold = str(row["Sold"]) if pd.notna(row["Sold"]) else ""
#     rating = str(row["Rating"]) if pd.notna(row["Rating"]) else ""
#     publisher = ", ".join(eval(row["Publisher"])) if isinstance(row["Publisher"], str) and row["Publisher"] else ""
#     manufacturer = ", ".join(eval(row["Manufacturer"])) if isinstance(row["Manufacturer"], str) and row["Manufacturer"] else ""
#     authors = ", ".join(eval(row["Authors"])) if isinstance(row["Authors"], str) and row["Authors"] else ""
#     link = row["Link"] if pd.notna(row["Link"]) else ""

#     # Xử lý cột Other_sellers
#     try:
#         sellers_info = json.loads(row["Other_sellers"].replace("'", '"'))
#         sellers = [{"name": s["name"], "price": s["price"], "link": s["link"]} for s in sellers_info]
#     except:
#         sellers = []

#     # Tạo khối văn bản key-value
#     book_info_lines = []
#     if name:
#         book_info_lines.append(f"Title: {name}")
#     if authors:
#         book_info_lines.append(f"Authors: {authors}")
#     if publisher:
#         book_info_lines.append(f"Publisher: {publisher}")
#     if manufacturer:
#         book_info_lines.append(f"Manufacturer: {manufacturer}")
#     if price:
#         book_info_lines.append(f"Price: {price}")
#     if discount:
#         book_info_lines.append(f"Discount: {discount}")
#     if sold:
#         book_info_lines.append(f"Sold: {sold}")
#     if rating:
#         book_info_lines.append(f"Rating: {rating}")
#     if link:
#         book_info_lines.append(f"Link: {link}")
    
#     # Xử lý Other_sellers thành từng dòng riêng
#     for seller in sellers:
#         book_info_lines.append(f"Seller: {seller['name']} with price {seller['price']} VND (link: {seller['link']})")

#     return "\n".join(book_info_lines)

# # Chuyển đổi từng dòng thành mô tả văn bản
# text_data = df.apply(generate_book_description, axis=1).tolist()

# # Xuất ra file text để nạp vào LightRAG
# output_file = "./data/tiki_books_json.txt"
# with open(output_file, "w", encoding="utf-8") as f:
#     f.write("\n\n".join(text_data))

# print(f"✅ Dữ liệu đã được ghi vào {output_file}")