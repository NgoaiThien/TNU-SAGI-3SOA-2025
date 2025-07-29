# Polarization Image Processing / Xử lý ảnh phân cực

[English](#english) | [Tiếng Việt](#vietnamese)

---

## Quick Start (English)

1. **Install Git (if not installed):**  
   Download and install Git from: https://git-scm.com/downloads
2. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```
3. **(Recommended) Use Python 3.10:**  
   - If you do not use conda, download Python 3.10 from https://www.python.org/downloads/release/python-3100/
   - Make sure to check "Add Python to PATH" during installation.
4. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
   ```
5. **Launch Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```
6. **Open `PolarizationImageProcessing.ipynb` and run all cells.**

## Hướng dẫn nhanh (Tiếng Việt)

1. **Cài đặt Git (nếu chưa có):**  
   Tải và cài đặt Git tại: https://git-scm.com/downloads
2. **Tải mã nguồn về máy:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```
3. **(Khuyến nghị) Sử dụng Python 3.10:**  
   - Nếu không dùng conda, tải Python 3.10 tại https://www.python.org/downloads/release/python-3100/
   - Nhớ chọn "Add Python to PATH" khi cài đặt.
4. **Cài đặt các gói phụ thuộc:**
   ```bash
   pip install -r requirement.txt
   ```
5. **Khởi động Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```
6. **Mở `PolarizationImageProcessing.ipynb` và chạy tất cả các cell.**

## English

### Overview
This project provides tools for analyzing polarization data from astronomical FITS files. It can process 4 polarization images (0°, 45°, 90°, 135°) to calculate Stokes parameters and create polarization maps.

### Requirements
- Python 3.10
- Conda package manager
- FITS files containing polarization data

### Setup Instructions

#### 1. Create Conda Environment (optional)
```bash
# Create a new conda environment with Python 3.10
conda create -n astro_env python=3.10 -y

# Activate the environment
conda activate astro_env
```

#### 2. Install Dependencies
```bash
# Install required packages from requirements.txt
pip install -r requirement.txt
```

#### 3. Launch Jupyter Notebook
```bash
# Launch Jupyter Notebook
jupyter notebook
```

#### 4. Usage
1. Open `PolarizationImageProcessing.ipynb` in Jupyter
2. Run all cells in the notebook to start the file browser interface
3. Select the folder containing your polarization FITS files (.fit)
4. The notebook will automatically:
   - Load 4 polarization images
   - Calculate Stokes parameters (I, Q, U, V)
   - Generate polarization intensity and angle maps
   - Create vector plots showing polarization direction
   - Save results as new images and FITS files

#### Expected File Structure
data can download from here: https://drive.google.com/drive/folders/1OTJtV5GIIWs21TsoNHPQ2TMubLmitLXK?usp=drive_link
```
your_data_folder/
├── Moon3-0004-0.fit    # 0° polarization
├── Moon3-0004-45.fit   # 45° polarization  
├── Moon3-0004-90.fit   # 90° polarization
└── Moon3-0004-135.fit  # 135° polarization
```

## Vietnamese

### Tổng quan
Dự án này cung cấp các công cụ để phân tích dữ liệu phân cực từ các tệp FITS thiên văn. Nó có thể xử lý 4 hình ảnh phân cực (0°, 45°, 90°, 135°) để tính toán các tham số Stokes và tạo bản đồ phân cực.

### Yêu cầu
- Python 3.10
- Trình quản lý gói Conda
- Tệp FITS chứa dữ liệu phân cực

### Hướng dẫn cài đặt

#### 1. Tạo môi trường Conda (tùy chọn)
```bash
# Tạo môi trường conda mới với Python 3.10
conda create -n astro_env python=3.10 -y

# Kích hoạt môi trường
conda activate astro_env
```

#### 2. Cài đặt các gói phụ thuộc
```bash
# Cài đặt các gói cần thiết từ requirements.txt
pip install -r requirement.txt
```

#### 3. Khởi động Jupyter Notebook
```bash
# Khởi chạy Jupyter Notebook
jupyter notebook
```

#### 4. Cách sử dụng
1. Mở `PolarizationImageProcessing.ipynb` trong Jupyter
2. Chạy tất cả các cell của notebook để khởi động giao diện duyệt tệp
3. Chọn thư mục chứa các tệp FITS phân cực (.fit)
4. Notebook sẽ tự động:
   - Tải 4 hình ảnh phân cực
   - Tính toán các tham số Stokes (I, Q, U, V)
   - Tạo bản đồ cường độ và góc phân cực
   - Tạo biểu đồ vector hiển thị hướng phân cực
   - Lưu kết quả dưới dạng hình ảnh và tệp FITS mới

#### Cấu trúc tệp mong đợi
Dữ liệu có thể tải từ đây: https://drive.google.com/drive/folders/1OTJtV5GIIWs21TsoNHPQ2TMubLmitLXK?usp=drive_link
```
thu_muc_du_lieu/
├── Moon3-0004-0.fit    # Phân cực 0°
├── Moon3-0004-45.fit   # Phân cực 45°
├── Moon3-0004-90.fit   # Phân cực 90°
└── Moon3-0004-135.fit  # Phân cực 135°
```

#### Kết quả đầu ra
Script sẽ tạo thư mục `polarization_output` chứa:
- Biểu đồ phân tích phân cực
- Tệp FITS của các tham số Stokes
- Biểu đồ vector hiển thị hướng phân cực

### Troubleshooting / Khắc phục sự cố

#### Common Issues / Vấn đề thường gặp:

**English:**
- If you get import errors, make sure all packages are installed: `pip install -r requirement.txt`
- Ensure your FITS files are readable and contain valid image data
- Check that you have at least 2-4 FITS files in the selected folder

**Tiếng Việt:**
- Nếu gặp lỗi import, hãy đảm bảo tất cả gói đã được cài đặt: `pip install -r requirement.txt`
- Đảm bảo các tệp FITS có thể đọc được và chứa dữ liệu hình ảnh hợp lệ
- Kiểm tra rằng bạn có ít nhất 2-4 tệp FITS trong thư mục đã chọn

### Contact / Liên hệ
For questions or issues, please check the code documentation or create an issue.
Để biết thêm thông tin hoặc báo cáo vấn đề, vui lòng kiểm tra tài liệu code hoặc tạo issue.

---

**Special thanks to Mr. Tien Dong from Quy Nhon Observatory for providing the code.**
**Xin cảm ơn anh Tiến Đồng từ Đài Thiên văn Quy Nhơn đã cung cấp mã nguồn.**

