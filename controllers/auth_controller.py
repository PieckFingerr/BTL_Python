from tkinter import messagebox
import json
import os

USERS_FILE = "btl\\data\\users.json"

def load_users():
    """Đọc danh sách users từ file JSON, đảm bảo dữ liệu là danh sách []"""
    if not os.path.exists(USERS_FILE):
        return []  # Trả về danh sách rỗng nếu file không tồn tại

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            users = json.load(file)
            if not isinstance(users, list):  # Nếu không phải list, reset thành []
                users = []
            return users
    except (json.JSONDecodeError, FileNotFoundError):
        return []  # Nếu file lỗi hoặc không đọc được, trả về danh sách rỗng

def save_users(users):
    """Ghi danh sách users vào file JSON"""
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

# 🟢 Xử lý đăng nhập
def handle_login(username, password, app):
    if not username or not password:
        messagebox.showerror("Error", "Username and password are required!")
        return False

    users = load_users()

    # Kiểm tra thông tin đăng nhập
    for user in users:
        if user["username"] == username and user["password"] == password:
            messagebox.showinfo("Success", "Login successful!")
            
            return user

    messagebox.showerror("Error", "Invalid username or password!")
    return False

# 🟢 Xử lý đăng ký
def handle_register(username, password, email, conf_password, switch_to_login):
    """Xử lý đăng ký user mới"""
    if not username or not password or not email or not conf_password:
        messagebox.showerror("Error", "Please fill in all fields")
        return False

    if password != conf_password:
        messagebox.showerror("Error", "Passwords do not match")
        return False

    users = load_users()

    # Kiểm tra username hoặc email đã tồn tại chưa
    for user in users:
        if user["username"] == username:
            messagebox.showerror("Error", "Username already exists")
            return False
        if user["email"] == email:
            messagebox.showerror("Error", "Email already exists")
            return False

    # Tạo user mới
    new_user = {
        "user_id": len(users) + 1,  # ID tự động tăng
        "username": username,
        "password": password,  
        "email": email
    }

    # Thêm user mới vào danh sách
    users.append(new_user)

    # Lưu lại vào file
    save_users(users)

    messagebox.showinfo("Success", "Registration successful. You can now login.")
    switch_to_login()  # Chuyển về màn hình đăng nhập
    return True
