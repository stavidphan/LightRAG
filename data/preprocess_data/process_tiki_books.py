import pandas as pd
import json

# Đọc file Excel
try:
    df = pd.read_excel("./data/tiki_books_vn.xlsx", engine="openpyxl")
except FileNotFoundError:
    print("File không tồn tại.")
    exit()

# Hàm tạo câu mô tả sách
def generate_book_description(row):
    name = row["Name"]
    price = row["Price (vnd)"]
    discount = row["Discount (%)"]
    sold = row["Sold"]
    rating = row["Rating"]
    publisher = ", ".join(eval(row["Publisher"])) if isinstance(row["Publisher"], str) else row["Publisher"]
    manufacturer = ", ".join(eval(row["Manufacturer"])) if isinstance(row["Manufacturer"], str) else row["Manufacturer"]
    authors = ", ".join(eval(row["Authors"])) if isinstance(row["Authors"], str) else row["Authors"]
    link = row["Link"]

    # Xử lý cột Other_sellers
    try:
        sellers_info = json.loads(row["Other_sellers"].replace("'", '"'))  # Chuyển chuỗi JSON về list
        sellers_text = "; ".join([
            f"{s['name']} với giá {s['price']} VND (link: {s['link']})" for s in sellers_info
        ])
    except:
        sellers_text = "Không có thông tin nhà bán khác."

    return {
        "name": name,
        "price": price,
        "discount": discount,
        "sold": sold,
        "rating": rating,
        "publisher": publisher,
        "manufacturer": manufacturer,
        "authors": authors,
        "link": link,
        "sellers": sellers_text
    }

# Chuyển đổi từng dòng thành mô tả văn bản
data = df.apply(generate_book_description, axis=1).tolist()

# Tạo mô tả văn bản cho LightRAG
text_data = []
for book in data:
    text = f"""Sách "{book["name"]}" có giá {book["price"]} VND với mức giảm giá {book["discount"]}%. 
    Hiện đã bán được {book["sold"]} bản và có đánh giá trung bình {book["rating"]} sao.
    Nhà xuất bản là {book["publisher"]}. Sản xuất bởi {book["manufacturer"]}.
    Tác giả là {book["authors"]}. Sản phẩm được bán tại {book["link"]}.
    Các nhà bán khác: {book["sellers"]}.
"""
    text_data.append(text)

# Xuất ra file text để nạp vào LightRAG
with open("./data/tiki_books_vn.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(text_data))

# In kết quả mẫu
print("\n".join(text_data)[:1000])  # In thử 1000 ký tự đầu tiên
