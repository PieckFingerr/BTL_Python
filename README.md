# BTL_Python

## Cấu trúc App

btl/

├── main.py # Điểm khởi đầu của ứng dụng

├── models/ # Chứa các class định nghĩa dữ liệu

├── controllers/ # Xử lý logic nghiệp vụ

├── views/ # Giao diện người dùng (tkinter)

├── utils/ # Các tiện ích

└── data/ # Lưu trữ dữ liệu JSON

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

# Cách xài github

## Tạo tài khoản trước đi

Tạo tài khoản xong thì nhắn toi tên để toi thêm vào repo

## Clone về máy

Toi thêm vào rồi thì các ông vào vscode, vào terminal bấm

```bash
git clone https://github.com/PieckFingerr/BTL_Python.git
```

rồi vào thư mục trên

```bash
cd btl
```

rồi kiểm tra xem đã vào đúng chưa

```bash
git remote -v
```

nó hiện như vậy là đúng rồi này

```bash
origin  https://github.com/PieckFingerr/BTL_Python.git (fetch)
origin  https://github.com/PieckFingerr/BTL_Python.git (push)
```

## Code xong thì commit và push lên

QUAN TRỌNG

- Luôn pull code mới nhất, nghĩa là trước khi viết code thì phải pull về để tránh xung đột

Đầu tiên là chuyển qua nhánh main trước

```bash
git checkout main
```

rồi pull code về

```bash
git pull origin main --allow-unrelated-histories # Nhớ phải pull code trước
```

code xong rồi thì push lên

```bash
git add .
git commit -m"Viết chú thích đã làm gì vào đây"
git push origin main
```

# Chạy code

```bash
python main.py
```

