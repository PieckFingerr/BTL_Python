import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import os

# Cấu hình cho CustomTkinter
ctk.set_appearance_mode("dark")  # Chế độ: "dark" hoặc "light"
ctk.set_default_color_theme("blue")  # Chủ đề màu: "blue", "green", "dark-blue"

class AuthApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Cấu hình cửa sổ
        self.title("Game Store Management System")
        self.geometry("800x500")
        self.resizable(True, True)
        
        # Căn giữa cửa sổ trên màn hình
        self.center_window()
        
        # Frame chính
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)
        
        # Tiêu đề
        self.label_title = ctk.CTkLabel(self.main_frame, text="Welcome to the WLD Game Store",
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.pack(pady=(20, 30))
        
        # Tạo frame chứa form đăng nhập/đăng ký
        self.auth_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, width=500, height=500)
        self.auth_frame.pack(pady=10, padx=10)
        self.auth_frame.pack_propagate(False)  # Giữ kích thước cố định
        
        # Hiển thị form đăng nhập mặc định
        self.show_login()
        
        # Tạo thư mục lưu dữ liệu người dùng nếu chưa tồn tại
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/users.json"):
            with open("data/users.json", "w") as f:
                json.dump({}, f)
    
    def center_window(self):
        """Căn giữa cửa sổ trên màn hình."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def clear_auth_frame(self):
        """Xóa tất cả widgets trong auth_frame."""
        for widget in self.auth_frame.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Hiển thị form đăng nhập."""
        self.clear_auth_frame()
        
        # Tiêu đề đăng nhập
        login_label = ctk.CTkLabel(self.auth_frame, text="Login", font=ctk.CTkFont(size=20, weight="bold"))
        login_label.pack(pady=(20, 15))
        
        # Username
        username_label = ctk.CTkLabel(self.auth_frame, text="Username")
        username_label.pack(anchor="w", padx=50, pady=(10, 0))
        self.username_entry = ctk.CTkEntry(self.auth_frame, width=300, placeholder_text="Enter your username")
        self.username_entry.pack(pady=(0, 10), padx=50)
        
        # Password
        password_label = ctk.CTkLabel(self.auth_frame, text="Password")
        password_label.pack(anchor="w", padx=50, pady=(10, 0))
        self.password_entry = ctk.CTkEntry(self.auth_frame, width=300, placeholder_text="Enter your password", show="•")
        self.password_entry.pack(pady=(0, 20), padx=50)
        
        # Remember me checkbox
        self.remember_var = tk.BooleanVar()
        remember_checkbox = ctk.CTkCheckBox(self.auth_frame, text="Remember me", variable=self.remember_var)
        remember_checkbox.pack(pady=(0, 15), padx=50, anchor="w")
        
        # Login button
        login_button = ctk.CTkButton(self.auth_frame, text="Login", width=300, 
                                    command=self.handle_login)
        login_button.pack(pady=(10, 20), padx=50)
        
        # Register link
        register_button = ctk.CTkButton(self.auth_frame, text="Don't have an account? Register", 
                                       fg_color="transparent", hover=False, 
                                       command=self.show_register)
        register_button.pack(pady=(5, 10))
    
    def show_register(self):
        """Hiển thị form đăng ký."""
        self.clear_auth_frame()
        
        # Tiêu đề đăng ký
        register_label = ctk.CTkLabel(self.auth_frame, text="Register", font=ctk.CTkFont(size=20, weight="bold"))
        register_label.pack(pady=(20, 15))
        
        # Username
        username_label = ctk.CTkLabel(self.auth_frame, text="Username")
        username_label.pack(anchor="w", padx=50, pady=(10, 0))
        self.reg_username_entry = ctk.CTkEntry(self.auth_frame, width=300, placeholder_text="Create a username")
        self.reg_username_entry.pack(pady=(0, 10), padx=50)

        # Email
        email_label = ctk.CTkLabel(self.auth_frame, text="Email")
        email_label.pack(anchor="w", padx=50, pady=(10, 0))
        self.email_entry = ctk.CTkEntry(self.auth_frame, width=300, placeholder_text="Enter your email")
        self.email_entry.pack(pady=(0, 10), padx=50)
        
        # Password
        password_label = ctk.CTkLabel(self.auth_frame, text="Password")
        password_label.pack(anchor="w", padx=50, pady=(10, 0))
        self.reg_password_entry = ctk.CTkEntry(self.auth_frame, width=300, placeholder_text="Create a password", show="•")
        self.reg_password_entry.pack(pady=(0, 10), padx=50)
        
        # Confirm Password
        conf_password_label = ctk.CTkLabel(self.auth_frame, text="Confirm Password")
        conf_password_label.pack(anchor="w", padx=50, pady=(10, 0))
        self.reg_conf_password_entry = ctk.CTkEntry(self.auth_frame, width=300, 
                                                placeholder_text="Confirm your password", show="•")
        self.reg_conf_password_entry.pack(pady=(0, 20), padx=50)
        
        # Register button
        register_button = ctk.CTkButton(self.auth_frame, text="Register", width=300, 
                                       command=self.handle_register)
        register_button.pack(pady=(10, 20), padx=50)
        
        # Login link
        login_button = ctk.CTkButton(self.auth_frame, text="Already have an account? Login", 
                                   fg_color="transparent", hover=False, 
                                   command=self.show_login)
        login_button.pack(pady=(5, 10))
    
    def handle_login(self):
        """Xử lý đăng nhập."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Kiểm tra thông tin đăng nhập
        with open("data/users.json", "r") as f:
            users = json.load(f)
        
        if username in users and users[username]["password"] == password:
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            # TODO: Chuyển đến màn hình chính của ứng dụng
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def handle_register(self):
        """Xử lý đăng ký."""
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        email = self.reg_conf_password_entry.get()
        conf_password = self.reg_conf_password_entry.get()
        
        if not username or not password or not conf_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != conf_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Kiểm tra username hoặc email đã tồn tại chưa
        with open("data/users.json", "r") as f:
            users = json.load(f)
        
        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return
        
        if email in users:
            messagebox.showerror("Error", "Email already exists")
            return
        
        # Lưu người dùng mới
        users[username] = {"password": password}
        with open("data/users.json", "w") as f:
            json.dump(users, f)
        
        messagebox.showinfo("Success", "Registration successful. You can now login.")
        self.show_login()

