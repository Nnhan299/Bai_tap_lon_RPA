# Web Bất Động Sản

Script tự động thu thập dữ liệu bất động sản từ trang alonhadat.com.vn.

## Tính năng

- Tự động tìm kiếm bất động sản với các tiêu chí ngẫu nhiên
- Thu thập thông tin chi tiết từng bài đăng
- Lưu dữ liệu vào file CSV với các trường:
  - Tiêu đề
  - Mô tả
  - Địa chỉ
  - Diện tích
  - Giá
- Chạy tự động theo lịch (mỗi ngày lúc 6:00)

## Yêu cầu

- Python 3.x
- Các thư viện Python (được liệt kê trong file requirements.txt):
  - selenium==4.18.1
  - pandas==2.2.1
  - schedule==1.2.1
  - webdriver-manager==4.0.1

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

2. Cài đặt Chrome WebDriver:
- Tải Chrome WebDriver phù hợp với phiên bản Chrome của bạn từ: https://sites.google.com/chromium.org/driver/
- Đặt file chromedriver.exe vào thư mục chứa script hoặc thêm đường dẫn vào PATH

## Cách sử dụng

1. Chạy script:
```bash
python web_bat_dong_san.py
```

2. Script sẽ:
- Tự động mở trình duyệt Chrome
- Thực hiện tìm kiếm với tiêu chí ngẫu nhiên
- Thu thập thông tin từ các bài đăng
- Lưu dữ liệu vào file `alonhadat_data.csv`
- Chạy lại mỗi ngày lúc 6:00

## Cấu trúc dữ liệu

File CSV đầu ra chứa các cột:
- Tiêu đề: Tiêu đề bài đăng
- Mô tả: Mô tả chi tiết bất động sản
- Địa chỉ: Vị trí bất động sản
- Diện tích: Diện tích bất động sản
- Giá: Giá bất động sản

## Lưu ý

- Script sử dụng Selenium để tự động hóa trình duyệt
- Có cơ chế xử lý lỗi và tự động khôi phục
- Thời gian chờ giữa các thao tác được thiết lập để tránh bị chặn
- Dữ liệu được lưu vào file CSV với encoding UTF-8 để hiển thị đúng tiếng Việt 