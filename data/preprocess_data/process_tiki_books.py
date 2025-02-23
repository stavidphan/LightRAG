import pandas as pd
import json

# Đọc file Excel
df = pd.read_excel("./data/tiki_books_vn.xlsx", engine="openpyxl")

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

    return (
        f'Sách "{name}" có giá {price} VND với mức giảm giá {discount}%. '
        f'Hiện đã bán được {sold} bản và có đánh giá trung bình {rating} sao. '
        f'Nhà xuất bản là {publisher}. Sản xuất bởi {manufacturer}. '
        f'Tác giả là {authors}. Sản phẩm được bán tại {link}. '
        f'Các nhà bán khác: {sellers_text}.'
    )

# Chuyển đổi từng dòng thành mô tả văn bản
text_data = "\n".join(df.apply(generate_book_description, axis=1))

# Xuất ra file text để nạp vào LightRAG
with open("./data/tiki_books_vn.txt", "w", encoding="utf-8") as f:
    f.write(text_data)

# In kết quả mẫu
print(text_data[:1000])  # In thử 1000 ký tự đầu tiên