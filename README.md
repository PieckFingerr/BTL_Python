# BTL_Python

## Cấu trúc App

btl/
├── main.py         # Điểm khởi đầu của ứng dụng
├── models/         # Chứa các class định nghĩa dữ liệu
├── controllers/    # Xử lý logic nghiệp vụ
├── views/          # Giao diện người dùng (tkinter)
├── utils/          # Các tiện ích
└── data/           # Lưu trữ dữ liệu JSON

## models

Folder định nghĩa các class đối tượng, tức là giả sử app có người dùng (User) đi thì 1 file trong folder sẽ đặt là user.py, nó sẽ chứa các field, get, set, và các phương thức của đối tượng đó giống như add wish list, add to cart, search game,...

## controllers

có nhiệm vụ kết nối giữa folder models và views, giống như xử lý đăng nhập, đăng ký rồi đọc ghi dữ liệu JSON

## views 

Đơn giản là gọi giao diện từ tkinder ra thoi

## utils

Chứa các tiện ích hỗ trợ, các hàm thường dùng để xử lý việc gì đó mà hay xài,...

# Các models cần định nghĩa (dự kiến)

- User
- Admin
- Order
- Game

