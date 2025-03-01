import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import os
from urllib.parse import unquote
from datetime import datetime

def get_html_content(url):
    """
    Lấy nội dung HTML từ URL
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Lỗi khi lấy nội dung từ {url}: {str(e)}")
        return None

def extract_product_links(html_content, source_url=""):
    """
    Trích xuất các link sản phẩm từ thẻ a nằm trong div có class chứa product-item
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Tìm tất cả các div có class chứa product-item
    product_divs = soup.find_all('div', class_=lambda c: c and 'product-item' in c)
    
    product_links = []
    
    for div in product_divs:
        # Tìm thẻ a trong mỗi div product-item
        a_tag = div.find('a')
        if a_tag and 'href' in a_tag.attrs:
            link = a_tag['href']
            
            # Xử lý link đặc biệt như trong mẫu của bạn
            if 'RUTG0N2TTKI' in link or 'ti.ki' in link:
                # Cố gắng trích xuất URL gốc từ link rút gọn
                match = re.search(r'URI-(.*?)(?:&|$)', link)
                if match:
                    try:
                        original_url = match.group(1)
                        # Xử lý các ký tự đặc biệt được mã hóa
                        original_url = original_url.replace('%3A', ':').replace('%2F', '/').replace('&3A', ':').replace('&2F', '/')
                        original_url = unquote(original_url)
                        link = original_url
                    except:
                        pass
            
            # Lấy thêm thông tin sản phẩm từ thẻ div nếu có
            product_name = ""
            price = ""
            
            # Tìm tên sản phẩm
            name_elem = div.find('h3') or div.find('h2') or div.find(class_=lambda c: c and ('name' in c or 'title' in c))
            if name_elem:
                product_name = name_elem.text.strip()
            # Nếu không tìm thấy tên trong các thẻ trên, sử dụng text của thẻ a
            elif a_tag.text:
                product_name = a_tag.text.strip()
            
            # Tìm giá sản phẩm
            price_elem = div.find(class_=lambda c: c and ('price' in c or 'gia' in c))
            if price_elem:
                price = price_elem.text.strip()
            
            product_links.append({
                'link': link,
                'name': product_name,
                'price': price,
                'source_url': source_url,
                'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    return product_links

def decode_tiki_shortened_url(url):
    """
    Giải mã URL rút gọn của Tiki để lấy URL gốc
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        # Gửi request HEAD để lấy URL chuyển hướng mà không cần tải toàn bộ trang
        response = requests.head(url, headers=headers, allow_redirects=True)
        
        # Trả về URL cuối cùng sau khi chuyển hướng
        return response.url
    except Exception as e:
        print(f"Lỗi khi giải mã URL {url}: {str(e)}")
        return url

def append_to_excel(data, filename):
    """
    Ghi tiếp dữ liệu vào file Excel đã tồn tại hoặc tạo file mới nếu chưa có
    """
    # Lấy đường dẫn đầy đủ đến thư mục chứa file code hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    
    # Kiểm tra xem file đã tồn tại chưa
    if os.path.exists(file_path):
        try:
            # Đọc file Excel hiện có
            existing_df = pd.read_excel(file_path)
            
            # Tạo DataFrame mới từ dữ liệu mới
            new_df = pd.DataFrame(data)
            
            # Gộp dữ liệu cũ và mới
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # Loại bỏ các dòng trùng lặp (nếu có)
            combined_df.drop_duplicates(subset=['link'], keep='first', inplace=True)
            
            # Ghi lại vào file
            combined_df.to_excel(file_path, index=False)
            print(f"Đã ghi tiếp {len(new_df)} sản phẩm vào file {filename}")
            return combined_df
            
        except Exception as e:
            print(f"Lỗi khi đọc/ghi file Excel hiện có: {str(e)}")
            print("Tạo file mới...")
            # Nếu có lỗi khi đọc file cũ, tạo file mới
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            print(f"Đã lưu {len(data)} sản phẩm vào file mới {filename}")
            return df
    else:
        # Tạo file mới nếu chưa tồn tại
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        print(f"Đã lưu {len(data)} sản phẩm vào file mới {filename}")
        return df

def main(url="https://sach.sale/tiki/nhanam", excel_filename="product_links_sach_sale.xlsx"):
    """
    Hàm chính để crawl dữ liệu
    """
    print(f"Đang crawl dữ liệu từ: {url}")
    
    # Lấy nội dung HTML từ URL
    html_content = get_html_content(url)
    
    if not html_content:
        print("Không thể lấy nội dung HTML từ URL!")
        return
    
    # Trích xuất link sản phẩm
    product_links = extract_product_links(html_content, source_url=url)
    
    if not product_links:
        print("Không tìm thấy link sản phẩm nào!")
        return
    
    print(f"Đã tìm thấy {len(product_links)} link sản phẩm.")
    
    # Giải mã các URL rút gọn nếu cần
    for i, item in enumerate(product_links):
        link = item['link']
        if 'ti.ki' in link:
            print(f"Đang giải mã URL rút gọn: {link}")
            original_url = decode_tiki_shortened_url(link)
            product_links[i]['original_link'] = original_url
            time.sleep(1)  # Tạm dừng để tránh bị chặn
    
    # Xuất thông tin link sản phẩm
    for i, item in enumerate(product_links):
        print(f"{i+1}. Tên: {item['name']}")
        print(f"   Giá: {item['price']}")
        print(f"   Link: {item['link']}")
        if 'original_link' in item:
            print(f"   Link gốc: {item['original_link']}")
        print("-" * 50)
    
    # Ghi tiếp vào file Excel
    append_to_excel(product_links, excel_filename)

if __name__ == "__main__":
    # Sử dụng URL mặc định
    main()
    
    main(url="https://sach.sale/tiki/kimdong")
    main(url="https://sach.sale/tiki/alphabooks")
    main(url="https://sach.sale/tiki/omega")
    main(url="https://sach.sale/tiki/az")
    main(url="https://sach.sale/tiki/donga")
    main(url="https://sach.sale/tiki/trithuctre")