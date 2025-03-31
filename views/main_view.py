import customtkinter as ctk
import json
import os
from PIL import Image, ImageTk
from tkinter import messagebox
import requests
from io import BytesIO

from btl.controllers.game_controller import GameController
from btl.controllers.lib_controller import LibController
from btl.views.user_profile_view import ProfileFrame
from btl.controllers.wishlist_controller import WishlistController

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
    
    def add_to_library(self, game):
        try:
            # Get the game ID
            game_id = game.game_id
            
            # Use the LibController to add the game to the library
            lib_controller = LibController()
            result = lib_controller.add_lib(self.user_id, game_id)
            
            if result:
                messagebox.showinfo("Success", f"{game.game_name} added to your library")
                # Refresh the library view if we're currently on that page
                if self.content_title.cget("text") == "Your Library":
                    self.show_library()
            else:
                # Game is already in the library
                messagebox.showinfo("Info", f"{game.game_name} is already in your library")
        except Exception as e:
            print(f"Error adding game to library: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def add_to_wishlist(self, game):
        try:
            # Get the game ID
            game_id = game.game_id
            
            # Use the WishlistController to add the game to the wishlist
            wl_controller = WishlistController()
            result = wl_controller.add_wishlist(self.user_id, game_id)
            
            if result:
                messagebox.showinfo("Success", f"{game.game_name} added to your wishlist")
                # Refresh the wishlist view if we're currently on that page
                if self.content_title.cget("text") == "Your Wishlist":
                    self.show_wishlist()
            else:
                # Game is already in the wishlist
                messagebox.showinfo("Info", f"{game.game_name} is already in your wishlist")
        except Exception as e:
            print(f"Error adding game to wishlist: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def show_home_page(self):
        for widget in self.games_container.winfo_children():
            widget.destroy()
        
        # Update the title
        self.content_title.configure(text="Home")
        self.content_subtitle.configure(text="Games you might like")

        
        self.display_games()
    
    def show_wishlist(self):
        # Clear current content
        for widget in self.games_container.winfo_children():
            widget.destroy()
        
        # Update the title
        self.content_title.configure(text="Your Wishlist")
        self.content_subtitle.configure(text="Your games collection")
        
        # Get user's library
        wl_controller = WishlistController()
        user_wl = wl_controller.get_wishlist_by_user_id(self.user_id)
        
        # If library is empty or user doesn't have a library yet
        if not user_wl or "product_id" not in user_wl or not user_wl["product_id"]:
            empty_label = ctk.CTkLabel(
                self.games_container, 
                text="Your wishlist is empty. Add games to see them here.",
                font=ctk.CTkFont(size=16)
            )
            empty_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
            return
        
        # Get the game objects for each library item
        wl_games = []
        for game_id in user_wl["product_id"]:
            game = self.games_controller.get_game_by_id(game_id)
            if game:
                wl_games.append(game)
            
        # Display games based on current view
        if self.current_view == "grid":
            # Grid view (3 columns)
            for i, game in enumerate(wl_games):
                row = i // 3
                col = i % 3
                
                # Game card
                game_frame = ctk.CTkFrame(self.games_container)
                game_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                # Game image
                image_label = ctk.CTkLabel(
                    game_frame, text="", 
                    width=300, height=180,
                    fg_color="#333333",
                )
                image_label.grid(row=0, column=0, padx=5, pady=5)

                # Try to load image from URL
                if hasattr(game, "image") and game.image:
                    image = self.load_image_from_url(game.image)
                    if image:
                        image_label.configure(image=image)
                        # Keep reference to image to prevent garbage collection
                        image_label.image = image
                
                # Game title
                title_label = ctk.CTkLabel(
                    game_frame, text=game.game_name,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    wraplength=280
                )
                title_label.grid(row=1, column=0, padx=5, pady=(5, 5), sticky="w")
                
                # Remove from library button
                remove_button = ctk.CTkButton(
                    game_frame, text="Remove from Wishlist", 
                    command=lambda g_id=game.game_id: self.remove_from_wishlist(g_id)
                )
                remove_button.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="w")
        else:
            # List view (1 column)
            for i, game in enumerate(wl_games):
                # Game row
                game_frame = ctk.CTkFrame(self.games_container)
                game_frame.grid(row=i, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
                game_frame.grid_columnconfigure(1, weight=1)
                
                # Game image
                image_label = ctk.CTkLabel(
                    game_frame, text="", 
                    width=300, height=180,
                    fg_color="#333333",
                )
                image_label.grid(row=0, column=0, padx=5, pady=5)
                
                # Try to load image from URL
                if hasattr(game, "image") and game.image:
                    image = self.load_image_from_url(game.image)
                    if image:
                        image_label.configure(image=image)
                        # Keep reference to image to prevent garbage collection
                        image_label.image = image
                
                # Game title
                title_label = ctk.CTkLabel(
                    game_frame, text=game.game_name,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    anchor="w"
                )
                title_label.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
                
                # Buttons container
                buttons_frame = ctk.CTkFrame(game_frame, fg_color="transparent")
                buttons_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

                # Remove from library button
                remove_button = ctk.CTkButton(
                    buttons_frame, text="Remove from library", 
                    command=lambda g_id=game.game_id: self.remove_from_wishlist(g_id)
                )
                remove_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Highlight the library button in the sidebar
        self.home_button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Reset home button color
        self.profile_button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Reset profile button color
        self.wishlist_button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Reset wishlist button color
        self.library_button.configure(fg_color=("#2E5984", "#144870"))  # Highlight library button
    
    def show_library(self):
        # Clear current content
        for widget in self.games_container.winfo_children():
            widget.destroy()
        
        # Update the title
        self.content_title.configure(text="Your Library")
        self.content_subtitle.configure(text="Your games collection")
        
        # Get user's library
        lib_controller = LibController()
        user_lib = lib_controller.get_lib_by_user_id(self.user_id)
        
        # If library is empty or user doesn't have a library yet
        if not user_lib or "product_id" not in user_lib or not user_lib["product_id"]:
            empty_label = ctk.CTkLabel(
                self.games_container, 
                text="Your library is empty. Add games to see them here.",
                font=ctk.CTkFont(size=16)
            )
            empty_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
            return
        
        # Get the game objects for each library item
        library_games = []
        for game_id in user_lib["product_id"]:
            game = self.games_controller.get_game_by_id(game_id)
            if game:
                library_games.append(game)
            
        # Display games based on current view
        if self.current_view == "grid":
            # Grid view (3 columns)
            for i, game in enumerate(library_games):
                row = i // 3
                col = i % 3
                
                # Game card
                game_frame = ctk.CTkFrame(self.games_container)
                game_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                # Game image
                image_label = ctk.CTkLabel(
                    game_frame, text="", 
                    width=300, height=180,
                    fg_color="#333333",
                )
                image_label.grid(row=0, column=0, padx=5, pady=5)

                # Try to load image from URL
                if hasattr(game, "image") and game.image:
                    image = self.load_image_from_url(game.image)
                    if image:
                        image_label.configure(image=image)
                        # Keep reference to image to prevent garbage collection
                        image_label.image = image
                
                # Game title
                title_label = ctk.CTkLabel(
                    game_frame, text=game.game_name,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    wraplength=280
                )
                title_label.grid(row=1, column=0, padx=5, pady=(5, 5), sticky="w")

                # Play game button
                play_button = ctk.CTkButton(
                    game_frame, text="Play", 
                    command=lambda g=game: self.play_game(g)
                )
                play_button.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="w")
                
                # Remove from library button
                remove_button = ctk.CTkButton(
                    game_frame, text="Remove from library", 
                    command=lambda g_id=game.game_id: self.remove_from_library(g_id)
                )
                remove_button.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="w")
        else:
            # List view (1 column)
            for i, game in enumerate(library_games):
                # Game row
                game_frame = ctk.CTkFrame(self.games_container)
                game_frame.grid(row=i, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
                game_frame.grid_columnconfigure(1, weight=1)
                
                # Game image
                image_label = ctk.CTkLabel(
                    game_frame, text="", 
                    width=300, height=180,
                    fg_color="#333333",
                )
                image_label.grid(row=0, column=0, padx=5, pady=5)
                
                # Try to load image from URL
                if hasattr(game, "image") and game.image:
                    image = self.load_image_from_url(game.image)
                    if image:
                        image_label.configure(image=image)
                        # Keep reference to image to prevent garbage collection
                        image_label.image = image
                
                # Game title
                title_label = ctk.CTkLabel(
                    game_frame, text=game.game_name,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    anchor="w"
                )
                title_label.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
                
                # Buttons container
                buttons_frame = ctk.CTkFrame(game_frame, fg_color="transparent")
                buttons_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

                # Play game button
                play_button = ctk.CTkButton(
                    buttons_frame, text="Play", 
                    command=lambda g=game: self.play_game(g)
                )

                # Remove from library button
                remove_button = ctk.CTkButton(
                    buttons_frame, text="Remove from library", 
                    command=lambda g_id=game.game_id: self.remove_from_library(g_id)
                )
                remove_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Highlight the library button in the sidebar
        self.home_button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Reset home button color
        self.profile_button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Reset profile button color
        self.wishlist_button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Reset wishlist button color
        self.library_button.configure(fg_color=("#2E5984", "#144870"))  # Highlight library button

    def play_game(self, game):
        messagebox.showinfo("Play Game", f"Starting {game.game_name}...")
        # Add actual game launch logic here if needed

    def remove_from_library(self, game_id):
        try:
            # Use the LibController to remove the game from the library
            lib_controller = LibController()
            success = lib_controller.delete_lib_by_product_id(self.user_id, game_id)
            
            if success:
                messagebox.showinfo("Success", "Game removed from your library")
                # Refresh the library view
                self.show_library()
            else:
                messagebox.showerror("Error", "Failed to remove game from your library")
        except Exception as e:
            print(f"Error removing game from library: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
       
    def remove_from_wishlist(self, game_id):
        try:
            # Use the LibController to remove the game from the library
            wl_controller = WishlistController()
            success = wl_controller.delete_wishlist_by_product_id(self.user_id, game_id)
            
            if success:
                messagebox.showinfo("Success", "Game removed from your Wishlist")
                # Refresh the library view
                self.show_library()
            else:
                messagebox.showerror("Error", "Failed to remove game from your Wishlist")
        except Exception as e:
            print(f"Error removing game from Wishlist: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
       
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
        # Check cache first
        cache_key = f"{url}_{width}_{height}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        try:
            # Load image from URL
            response = requests.get(url)
            response.raise_for_status()
            
            # Convert data to PIL image
            image = Image.open(BytesIO(response.content))
            
            # Resize image to fit display size
            image = image.resize((width, height), Image.LANCZOS)
            
            # Convert PIL image to CTkImage format
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(width, height))
            
            # Save to cache
            self.image_cache[cache_key] = ctk_image
            return ctk_image
        except Exception as e:
            print(f"Cannot load image from URL {url}: {e}")
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

