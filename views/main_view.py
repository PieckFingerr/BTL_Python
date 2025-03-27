import customtkinter as ctk
import json
import os
from PIL import Image, ImageTk
from tkinter import messagebox
import requests
from io import BytesIO

from btl.controllers.game_controller import GameController


from btl.views.user_profile_view import ProfileFrame

ctk.set_appearance_mode("dark")  # Chế độ tối
ctk.set_default_color_theme("blue")  # Chủ đề màu

class MainApp(ctk.CTk):
    def __init__(self, current_user):
        super().__init__()

        # Lưu thông tin user hiện tại
        self.current_user = current_user

        # Sử dụng user_id khi cần
        if self.current_user and "user_id" in self.current_user:
            self.user_id = self.current_user["user_id"]

        print("User ID:", self.user_id)

        # Định nghĩa biến game để hiển thị
        self.games_controller = GameController()

        # cache cho ảnh đã tải
        self.image_cache = {}

        
        # Cấu hình cửa sổ chính
        self.title("WLD Game Store")
        self.geometry("1200x700")

        # Dữ liệu games lấy từ file json
        self.games_data = []
        self.loadtk()
        
        # Tạo layout chính
        self.create_main_layout()
    
    def create_main_layout(self):
        # Tạo khung chính
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tạo sidebar bên trái
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
        # Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="WLD Game Store", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Các mục trong sidebar
        self.home_button = ctk.CTkButton(
            self.sidebar_frame, text="Home", 
            command=self.show_home_page
        )
        self.home_button.grid(row=1, column=0, padx=20, pady=10)
        
        # Profile button
        self.profile_button = ctk.CTkButton(
            self.sidebar_frame, text="Your Profile",
            command=self.show_profile_page
        )
        self.profile_button.grid(row=3, column=0, padx=20, pady=10)
        
        # Wishlist và Library buttons
        self.wishlist_button = ctk.CTkButton(
            self.sidebar_frame, text="Wishlist",
            command=self.show_wishlist
        )
        self.wishlist_button.grid(row=4, column=0, padx=20, pady=10)
        
        self.library_button = ctk.CTkButton(
            self.sidebar_frame, text="My Library",
            command=self.show_library
        )
        self.library_button.grid(row=5, column=0, padx=20, pady=10)
        
        # Main content area
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Configure main content area
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        # Main content title
        self.content_title = ctk.CTkLabel(
            self.header_frame, text="New and trending",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.content_title.grid(row=0, column=0, sticky="w")
        
        self.content_subtitle = ctk.CTkLabel(
            self.header_frame, text="Based on player counts and release date",
            font=ctk.CTkFont(size=14)
        )
        self.content_subtitle.grid(row=1, column=0, sticky="w")

        # Search bar
        self.search_frame = ctk.CTkFrame(self.header_frame)
        self.search_frame.grid(row=3, column=0, sticky="w", pady=(10, 0))
        
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search:")
        self.search_label.grid(row=0, column=0, padx=(10, 5))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, width=300, placeholder_text="Search by name...")
        self.search_entry.grid(row=0, column=1, padx=5)
        
        self.search_button = ctk.CTkButton(
            self.search_frame, text="Search", width=100,
              command=self.search_games_method
        )
        self.search_button.grid(row=0, column=2, padx=5)

        # Display options
        self.display_frame = ctk.CTkFrame(self.header_frame)
        self.display_frame.grid(row=2, column=1, sticky="e")
        
        self.display_label = ctk.CTkLabel(self.display_frame, text="Display options:")
        self.display_label.grid(row=0, column=0, padx=5)
        
        self.grid_view_button = ctk.CTkButton(
            self.display_frame, text="□□\n□□", width=40, height=40,
            command=lambda: self.change_view("grid")
        )
        self.grid_view_button.grid(row=0, column=1, padx=5)
        
        self.list_view_button = ctk.CTkButton(
            self.display_frame, text="≡\n≡", width=40, height=40,
            command=lambda: self.change_view("list")
        )
        self.list_view_button.grid(row=0, column=2, padx=5)
        
        # Game listings container (scrollable)
        self.games_container = ctk.CTkScrollableFrame(self.main_frame)
        self.games_container.grid(row=1, column=0, sticky="nsew")
        self.games_container.grid_columnconfigure(0, weight=1)
        self.games_container.grid_columnconfigure(1, weight=1)
        self.games_container.grid_columnconfigure(2, weight=1)
        
        # Display games in grid view
        self.current_view = "grid"
        self.display_games()
    
    def display_games(self):
        # Clear current games
        for widget in self.games_container.winfo_children():
            widget.destroy()

        self.games_data = self.games_controller.get_all_games()

        # Display games based on current view
        if self.current_view == "grid":
            # Hiển thị dạng lưới (3 cột)
            for i, game in enumerate(self.games_data):
                row = i // 3
                col = i % 3

                # Game card
                game_frame = ctk.CTkFrame(self.games_container)
                game_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                # Game image từ URL
                image_label = ctk.CTkLabel(
                    game_frame, text="", 
                    width=300, height=180,
                    fg_color="#333333",
                )
                image_label.grid(row=0, column=0, padx=5, pady=5)

                # Thử tải ảnh từ URL
                if hasattr(game, "image") and game.image:
                    image = self.load_image_from_url(game.image)
                    if image:
                        image_label.configure(image=image)
                        # Lưu tham chiếu đến ảnh để tránh bị garbage collect
                        image_label.image = image
                
                # Game title
                title_label = ctk.CTkLabel(
                    game_frame, text=game.game_name,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    wraplength=280
                )
                title_label.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="w")

                # Add to lib
                library_button = ctk.CTkButton(
                    game_frame, text="Add to library", 
                    command=lambda g=game: self.add_to_library(g)
                )
                library_button.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="w")

                # Add to wishlist
                wishlist_button = ctk.CTkButton(
                    game_frame, text="Add to wishlist", 
                    command=lambda g=game: self.add_to_wishlist(g)
                )
                wishlist_button.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="w")

        else:
            # Hiển thị dạng danh sách (1 cột)
            for i, game in enumerate(self.games_data):
                # Game row
                game_frame = ctk.CTkFrame(self.games_container)
                game_frame.grid(row=i, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
                game_frame.grid_columnconfigure(1, weight=1)

                # Game image từ URL
                image_label = ctk.CTkLabel(
                    game_frame, text="", 
                    width=300, height=180,
                    fg_color="#333333",
                )
                image_label.grid(row=0, column=0, padx=5, pady=5)

                # Thử tải ảnh từ URL
                if hasattr(game, "image") and game.image:
                    image = self.load_image_from_url(game.image)
                    if image:
                        image_label.configure(image=image)
                        # Lưu tham chiếu đến ảnh để tránh bị garbage collect
                        image_label.image = image
                
                # # Game image placeholder
                # image_label = ctk.CTkLabel(
                #     game_frame, text="", 
                #     width=160, height=90,
                #     fg_color="#333333"
                # )
                # image_label.grid(row=0, column=0, padx=10, pady=10, rowspan=3)
                
                # Game title
                title_label = ctk.CTkLabel(
                    game_frame, text=game.game_name,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    anchor="w"
                )
                title_label.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

                # Add to lib
                library_button = ctk.CTkButton(
                    game_frame, text="Add to library", 
                    command=lambda g=game: self.add_to_library(g)
                )
                library_button.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="w")

                # Add to wishlist
                wishlist_button = ctk.CTkButton(
                    game_frame, text="Add to wishlist", 
                    command=lambda g=game: self.add_to_wishlist(g)
                )
                wishlist_button.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="w")

    def display_filtered_games(self, filtered_games):
        # Clear current games
        for widget in self.games_container.winfo_children():
            widget.destroy()

        # Display games based on current view
        if self.current_view == "grid":
            # Hiển thị dạng lưới (3 cột)
            for i, game in enumerate(filtered_games):
                row = i // 3
                col = i % 3

                # Game card
                game_frame = ctk.CTkFrame(self.games_container)
                game_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                # Game image từ URL
                image_label = ctk.CTkLabel(
                    game_frame, text="", 
                    width=300, height=180,
                    fg_color="#333333",
                )
                image_label.grid(row=0, column=0, padx=5, pady=5)

                # Thử tải ảnh từ URL
                if hasattr(game, "image") and game.image:
                    image = self.load_image_from_url(game.image)
                    if image:
                        image_label.configure(image=image)
                        # Lưu tham chiếu đến ảnh để tránh bị garbage collect
                        image_label.image = image
                
                # Game title
                title_label = ctk.CTkLabel(
                    game_frame, text=game.game_name,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    wraplength=280
                )
                title_label.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="w")

                # Add to lib
                library_button = ctk.CTkButton(
                    game_frame, text="Add to library", 
                    command=lambda g=game: self.add_to_wishlist(g)
                )
                library_button.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="w")

                # Add to wishlist
                wishlist_button = ctk.CTkButton(
                    game_frame, text="Add to wishlist", 
                    command=lambda g=game: self.add_to_wishlist(g)
                )
                wishlist_button.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="w")

        else:
            # Hiển thị dạng danh sách (1 cột)
            for i, game in enumerate(self.filter_games):
                # Game row
                game_frame = ctk.CTkFrame(self.games_container)
                game_frame.grid(row=i, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
                game_frame.grid_columnconfigure(1, weight=1)

                # Game image từ URL
                image_label = ctk.CTkLabel(
                    game_frame, text="", 
                    width=300, height=180,
                    fg_color="#333333",
                )
                image_label.grid(row=0, column=0, padx=5, pady=5)

                # Thử tải ảnh từ URL
                if hasattr(game, "image") and game.image:
                    image = self.load_image_from_url(game.image)
                    if image:
                        image_label.configure(image=image)
                        # Lưu tham chiếu đến ảnh để tránh bị garbage collect
                        image_label.image = image
                
                # # Game image placeholder
                # image_label = ctk.CTkLabel(
                #     game_frame, text="", 
                #     width=160, height=90,
                #     fg_color="#333333"
                # )
                # image_label.grid(row=0, column=0, padx=10, pady=10, rowspan=3)
                
                # Game title
                title_label = ctk.CTkLabel(
                    game_frame, text=game.game_name,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    anchor="w"
                )
                title_label.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

                # Add to lib
                library_button = ctk.CTkButton(
                    game_frame, text="Add to library", 
                    command=lambda g=game: self.add_to_wishlist(g)
                )
                library_button.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="w")

                # Add to wishlist
                wishlist_button = ctk.CTkButton(
                    game_frame, text="Add to wishlist", 
                    command=lambda g=game: self.add_to_wishlist(g)
                )
                wishlist_button.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="w")

    def change_view(self, view_type):
        self.current_view = view_type
        self.display_games()
    
    def sort_games(self, option):
        # Placeholder for sorting logic
        if option == "Name":
            self.games_data.sort(key=lambda x: x["title"])
        elif option == "Popularity":
            self.games_data.sort(key=lambda x: x["player_count"], reverse=True)
        # Các tùy chọn sắp xếp khác có thể được thêm vào sau
        
        self.display_games()
    
    def filter_games(self, filter_type):
        # Placeholder for filtering logic
        messagebox.showinfo("Lọc game", f"Lọc theo: {filter_type}")
        # TODO: Thực hiện lọc dữ liệu game
    
    def add_to_wishlist(self, game):
        messagebox.showinfo("Wishlist", f"Đã thêm {game['title']} vào danh sách yêu thích")
    
    def show_home_page(self):
        for widget in self.games_container.winfo_children():
            widget.destroy()
        
        # Update the title
        self.content_title.configure(text="Home")
        self.content_subtitle.configure(text="Games you might like")

        
        self.display_games()
    
    def show_wishlist(self):
        self.content_title.configure(text="Your Wishlist")
        self.content_subtitle.configure(text="Games you've saved for later")
    
    def show_library(self):
        self.content_title.configure(text="Your Library")
        self.content_subtitle.configure(text="Your purchased games")

    def show_profile_page(self):
        # Clear current content
        for widget in self.games_container.winfo_children():
            widget.destroy()
        
        # In ra giá trị current_user để kiểm tra
        print("Current User:", self.current_user)
        print("Type of current_user:", type(self.current_user))
        
        # Update the title
        self.content_title.configure(text="Your Profile")
        self.content_subtitle.configure(text="Manage your account settings")
        
        # Thử in từng phần của current_user
        if self.current_user:
            for key, value in self.current_user.items():
                print(f"{key}: {value}")
        
        # Thử truyền theo nhiều cách
        try:
            # Cách 1
            profile_frame = ProfileFrame(self.games_container, current_user=self.current_user)
            profile_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
        except Exception as e:
            print("Lỗi khi tạo ProfileFrame:", e)

    # Tải ảnh lên view bằng url        
    def load_image_from_url(self, url, width=300, height=180):
        # Kiểm tra cache trước
        cache_key = f"{url}_{width}_{height}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        try:
            # Tải ảnh từ URL
            response = requests.get(url)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            
            # Chuyển đổi dữ liệu nhận được thành ảnh PIL
            image = Image.open(BytesIO(response.content))
            
            # Resize ảnh để vừa với kích thước hiển thị
            image = image.resize((width, height), Image.LANCZOS)
            
            # Chuyển đổi ảnh PIL thành định dạng CTkImage
            ctk_image = ImageTk.PhotoImage(image)
            
            # Lưu vào cache
            self.image_cache[cache_key] = ctk_image
            return ctk_image
        except Exception as e:
            print(f"Không thể tải ảnh từ URL {url}: {e}")
            return None


    def search_games_method(self):
        search_term = self.search_entry.get()

        filtered_games = search_games(search_term)

        # Clear current games
        for widget in self.games_container.winfo_children():
            widget.destroy()

        # Update title to reflect search
        self.content_title.configure(text=f"Search Results for '{search_term}'")
        self.content_subtitle.configure(text=f"{len(filtered_games)} games found")
        
        # Store the filtered games
        self.games_data = filtered_games
        
        # Display the filtered games
        self.display_filtered_games(filtered_games)


# Tìm game theo tên trên thanh search bar và hiển thị ra view
def search_games(game_name):
    game_controller = GameController()
    return game_controller.get_games_by_name(game_name)
