# Hướng Dẫn Cài Đặt & Chạy LightRAG với Ollama

## Mục Lục
1. [Kết Nối Server](#1-kết-nối-server)
2. [Cập Nhật Hệ Thống (Tùy Chọn)](#2-cập-nhật-hệ-thống-tùy-chọn)
3. [Clone Repository LightRAG](#3-clone-repository-lightrag)
4. [Cài Đặt Môi Trường Python](#4-cài-đặt-môi-trường-python)
5. [Cài Đặt & Cấu Hình Ollama](#5-cài-đặt--cấu-hình-ollama)
6. [Chuẩn Bị Dữ Liệu](#6-chuẩn-bị-dữ-liệu)
7. [Chạy Model Ollama](#7-chạy-model-ollama)
8. [Chỉnh Sửa File Demo & Chạy Model](#8-chỉnh-sửa-file-demo--chạy-model)
9. [Đẩy Code Lên GitHub](#9-đẩy-code-lên-github)

---

## 1. Kết Nối Server
Mở terminal và kết nối đến server qua SSH:
```bash
ssh -p 47945 user@213.180.0.36
```

---

## 2. Cập Nhật Hệ Thống (Tùy Chọn)
Cập nhật và nâng cấp hệ thống (nếu cần):
```bash
sudo apt update && sudo apt upgrade -y
```

---

## 3. Clone Repository LightRAG
Có hai repository:
- **Repository chính thức:** (Cần sửa đổi và insert data từ đầu)
  ```bash
  git clone https://github.com/HKUDS/LightRAG.git
  ```
- **Repository đã insert data (repo của tôi):**
  ```bash
  git clone https://github.com/stavidphan/LightRAG.git
  ```

Chuyển vào thư mục dự án:
```bash
cd LightRAG/
```

---

## 4. Cài Đặt Môi Trường Python
Cài đặt package cần thiết:
```bash
pip install -e .
```

---

## 5. Cài Đặt & Cấu Hình Ollama

### 5.1. Cài Đặt Ollama
Chạy lệnh cài đặt Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 5.2. Pull Các Model Cần Thiết
```bash
ollama pull qwen2
ollama pull nomic-embed-text

ollama pull gemma2:9b --quantize int8
ollama pull multilingual-e5-large
```

### 5.3. Tạo File Modelfile Cho Model `qwen2`
```bash
ollama show --modelfile qwen2 > Modelfile
nano Modelfile
```
Thêm dòng sau vào file:
```
PARAMETER num_ctx 32768
```

### 5.4. Cấp Quyền Cho Thư Mục Ollama (Nếu Cần)
```bash
sudo chown -R $USER:$USER /usr/share/ollama/.ollama
sudo chmod -R 777 /usr/share/ollama/.ollama
```

### 5.5. Tạo Model Mới Với Cấu Hình Đã Chỉnh Sửa
```bash
sudo ollama create -f Modelfile qwen2m
```

---

## 6. Chuẩn Bị Dữ Liệu
Sao chép dữ liệu từ máy local lên server:
```bash
scp -r -P 47945 /Users/duypt/Downloads/Documents/LightRAG/data user@213.180.0.36:./LightRAG
```

---

## 7. Chạy Model Ollama
Mở một terminal riêng và chạy model `qwen2m`:
```bash
ollama run qwen2m
ollama serve
```

---

## 8. Chỉnh Sửa File Demo & Chạy Model

### 8.1. Chỉnh Sửa File Demo
```bash
nano examples/lightrag_ollama_demo.py
```
**Chỉnh sửa các phần sau:**
- `llm_model_name`
- Phần insert data (nếu clone repo chính thức)

### 8.2. Cài Đặt Phụ Thuộc & Chạy Demo Lần Đầu (Insert Data)
```bash
pip install scipy==1.12.0
python3 examples/lightrag_ollama_demo.py
```

### 8.3. Chạy Ứng Dụng Chính Để Nhập Query
```bash
python3 examples/main.py
```

---

## 9. Đẩy Code Lên GitHub

### 9.1. Xóa Thiết Lập Git Cũ
```bash
git remote remove origin
rm -rf .git
```

### 9.2. Cấu Hình Thông Tin Người Dùng Git
```bash
git config --global user.email "thanhduyphan2123@gmail.com"
git config --global user.name "Stavid Phan"
```

### 9.3. Thêm Remote Origin & Đẩy Code
```bash
git remote add origin https://github.com/stavidphan/LightRAG.git
git branch -M main
git push -u origin main
```

---