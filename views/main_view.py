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
    def __init__(self):
        super().__init__()

        # Định nghĩa biến game để hiển thị
        self.games_controller = GameController()

        # cache cho ảnh đã tải
        self.image_cache = {}

        
        # Cấu hình cửa sổ chính
        self.title("WLD Game Store")
        self.geometry("1200x700")
        
        # Tạo biến để lưu trữ xem user hiện tại là ai
        self.current_user = None

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
        
        self.reviews_button = ctk.CTkButton(
            self.sidebar_frame, text="Reviews",
            command=self.show_reviews_page
        )
        self.reviews_button.grid(row=2, column=0, padx=20, pady=10)
        
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
        
        # New Releases section
        self.releases_label = ctk.CTkLabel(
            self.sidebar_frame, text="New Releases",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.releases_label.grid(row=8, column=0, padx=20, pady=(20, 10), sticky="w")
        
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
        
        # Sort options
        self.sort_frame = ctk.CTkFrame(self.header_frame)
        self.sort_frame.grid(row=2, column=0, sticky="w", pady=(10, 0))
        
        self.sort_label = ctk.CTkLabel(self.sort_frame, text="Order by:")
        self.sort_label.grid(row=0, column=0, padx=(10, 5))
        
        self.sort_options = ["Relevance", "Date added", "Name", "Release date", "Popularity", "Rating"]
        self.sort_dropdown = ctk.CTkOptionMenu(
            self.sort_frame, values=self.sort_options,
            command=self.sort_games
        )
        self.sort_dropdown.grid(row=0, column=1, padx=5)
        self.sort_dropdown.set("Relevance")

        # Search bar
        self.search_frame = ctk.CTkFrame(self.header_frame)
        self.search_frame.grid(row=3, column=0, sticky="w", pady=(10, 0))
        
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search:")
        self.search_label.grid(row=0, column=0, padx=(10, 5))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, width=300, placeholder_text="Search by name...")
        self.search_entry.grid(row=0, column=1, padx=5)
        # self.search_entry.bind("<Return>", self.search_games)
        
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
    
    def play_game(self, game):
        messagebox.showinfo("Chơi game", f"Bắt đầu chơi: {game['title']}")
    
    def add_to_wishlist(self, game):
        messagebox.showinfo("Wishlist", f"Đã thêm {game['title']} vào danh sách yêu thích")
    
    def show_home_page(self):
        self.content_title.configure(text="New and trending")
        self.content_subtitle.configure(text="Based on player counts and release date")
    
    def show_reviews_page(self):
        self.content_title.configure(text="Reviews")
        self.content_subtitle.configure(text="Game reviews from our community")
    
    def show_wishlist(self):
        self.content_title.configure(text="Your Wishlist")
        self.content_subtitle.configure(text="Games you've saved for later")
    
    def show_library(self):
        self.content_title.configure(text="Your Library")
        self.content_subtitle.configure(text="Your purchased games")
    
    def show_people(self):
        self.content_title.configure(text="People You Follow")
        self.content_subtitle.configure(text="See what your friends are playing")
    
    def show_calendar(self):
        self.content_title.configure(text="Release Calendar")
        self.content_subtitle.configure(text="Upcoming game releases")

    def show_profile_page(self):
        # Clear current content
        for widget in self.games_container.winfo_children():
            widget.destroy()
        
        # Update the title
        self.content_title.configure(text="Your Profile")
        self.content_subtitle.configure(text="Manage your account settings")
        
        # Create and display the profile frame
        profile_frame = ProfileFrame(self.games_container, current_user=self.current_user)
        profile_frame.pack(fill="both", expand=True, padx=20, pady=20)
        

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
