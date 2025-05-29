import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
import requests
from io import BytesIO
from btl.models.Game import Game


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
        self.user_id = current_user.get("user_id") if current_user else None
        print("User ID:", self.user_id)

        # Khởi tạo các controller và cache
        self.games_controller = GameController()
        self.lib_controller = LibController()
        self.wishlist_controller = WishlistController()
        self.image_cache = {}
        
        # Cấu hình cửa sổ chính
        self.title("WLD Game Store")
        self.geometry("1200x700")

        # Dữ liệu games lấy từ file json
        self.games_data = []
        self.current_view = "grid"  # Default view
        
        # Tạo layout chính
        self.setup_main_layout()
    
    def setup_main_layout(self):
        """Tạo layout chính cho ứng dụng"""
        # Cấu hình grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tạo sidebar
        self.create_sidebar()
        
        # Tạo vùng nội dung chính
        self.create_main_content_area()
        
        # Hiển thị games
        self.display_games()
    
    def create_sidebar(self):
        """Tạo sidebar với các nút điều hướng"""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
        # Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="WLD Game Store", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Các nút điều hướng
        self.home_button = self.create_nav_button("Home", self.show_home_page, 1)
        self.profile_button = self.create_nav_button("Your Profile", self.show_profile_page, 3)
        self.wishlist_button = self.create_nav_button("Wishlist", self.show_wishlist, 4)
        self.library_button = self.create_nav_button("My Library", self.show_library, 5)
    
    def create_nav_button(self, text, command, row):
        """Hàm trợ giúp tạo nút điều hướng"""
        button = ctk.CTkButton(
            self.sidebar_frame, text=text, 
            command=command
        )
        button.grid(row=row, column=0, padx=20, pady=10)
        return button
    
    def create_main_content_area(self):
        """Tạo vùng nội dung chính"""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header frame
        self.create_header_frame()
        
        # Game listings container (scrollable)
        self.games_container = ctk.CTkScrollableFrame(self.main_frame)
        self.games_container.grid(row=1, column=0, sticky="nsew")
        for i in range(3):  # 3 columns in grid view
            self.games_container.grid_columnconfigure(i, weight=1)
    
    def create_header_frame(self):
        """Tạo phần header với tiêu đề và thanh tìm kiếm"""
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        # Title và subtitle
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

        # Thanh tìm kiếm
        self.create_search_bar()

        # Tùy chọn hiển thị (Grid/List view)
        self.create_display_options()

        # Thêm game nếu là Admin
        if self.current_user and self.current_user.get("is_admin") == True:
            self.add_game_btn = ctk.CTkButton(
                self.header_frame, text="+", width=40, height=40,
                font=ctk.CTkFont(size=24, weight="bold"),
                command=self.open_add_game_window
            )
            self.add_game_btn.grid(row=0, column=1, padx=(10, 0), sticky="e")
        
    
    def create_search_bar(self):
        """Tạo thanh tìm kiếm"""
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
    
    def create_display_options(self):
        """Tạo các nút tùy chọn hiển thị (Grid/List)"""
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
    
    def load_image_from_url(self, url, width=300, height=180):
        """Tải và cache ảnh từ URL"""
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
    
    def create_game_card(self, parent, game, is_grid_view=True, is_library=False, is_wishlist=False):
        """Tạo card hiển thị thông tin game"""
        if is_grid_view:
            # Grid view card
            game_frame = ctk.CTkFrame(parent)
            
            # Game image
            image_label = ctk.CTkLabel(
                game_frame, text="", 
                width=300, height=180,
                fg_color="#333333",
            )
            image_label.grid(row=0, column=0, padx=5, pady=5)

            # Load image if available
            if hasattr(game, "image") and game.image:
                image = self.load_image_from_url(game.image)
                if image:
                    image_label.configure(image=image)
                    image_label.image = image  # Keep reference
            
            # Game title
            title_label = ctk.CTkLabel(
                game_frame, text=game.game_name,
                font=ctk.CTkFont(size=16, weight="bold"),
                wraplength=280
            )
            title_label.grid(row=1, column=0, padx=5, pady=(5, 5), sticky="w")
            
            # Add buttons based on context
            row = 2
            if is_library:
                # Play button for library
                play_button = ctk.CTkButton(
                    game_frame, text="Play", 
                    command=lambda g=game: self.play_game(g)
                )
                play_button.grid(row=row, column=0, padx=5, pady=(0, 5), sticky="w")
                row += 1
                
                # Remove from library button
                remove_button = ctk.CTkButton(
                    game_frame, text="Remove from library", 
                    command=lambda g_id=game.game_id: self.remove_from_library(g_id)
                )
                remove_button.grid(row=row, column=0, padx=5, pady=(0, 5), sticky="w")
            elif is_wishlist:
                # Remove from wishlist button
                remove_button = ctk.CTkButton(
                    game_frame, text="Remove from Wishlist", 
                    command=lambda g_id=game.game_id: self.remove_from_wishlist(g_id)
                )
                remove_button.grid(row=row, column=0, padx=5, pady=(0, 5), sticky="w")
            else:
                # Add to library button for main view
                library_button = ctk.CTkButton(
                    game_frame, text="Add to library", 
                    command=lambda g=game: self.add_to_library(g)
                )
                library_button.grid(row=row, column=0, padx=5, pady=(0, 5), sticky="w")
                row += 1
                
                # Add to wishlist button
                wishlist_button = ctk.CTkButton(
                    game_frame, text="Add to wishlist", 
                    command=lambda g=game: self.add_to_wishlist(g)
                )
                wishlist_button.grid(row=row, column=0, padx=5, pady=(0, 5), sticky="w")
        else:
            # List view card
            game_frame = ctk.CTkFrame(parent)
            game_frame.grid_columnconfigure(1, weight=1)
            
            # Game image
            image_label = ctk.CTkLabel(
                game_frame, text="", 
                width=300, height=180,
                fg_color="#333333",
            )
            image_label.grid(row=0, column=0, padx=5, pady=5, rowspan=2)
            
            # Load image if available
            if hasattr(game, "image") and game.image:
                image = self.load_image_from_url(game.image)
                if image:
                    image_label.configure(image=image)
                    image_label.image = image  # Keep reference
            
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
            
            # Add buttons based on context
            if is_library:
                # Play button for library
                play_button = ctk.CTkButton(
                    buttons_frame, text="Play", 
                    command=lambda g=game: self.play_game(g)
                )
                play_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                
                # Remove from library button
                remove_button = ctk.CTkButton(
                    buttons_frame, text="Remove from library", 
                    command=lambda g_id=game.game_id: self.remove_from_library(g_id)
                )
                remove_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")
            elif is_wishlist:
                # Remove from wishlist button
                remove_button = ctk.CTkButton(
                    buttons_frame, text="Remove from Wishlist", 
                    command=lambda g_id=game.game_id: self.remove_from_wishlist(g_id)
                )
                remove_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            else:
                # Add to library button for main view
                library_button = ctk.CTkButton(
                    buttons_frame, text="Add to library", 
                    command=lambda g=game: self.add_to_library(g)
                )
                library_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                
                # Add to wishlist button
                wishlist_button = ctk.CTkButton(
                    buttons_frame, text="Add to wishlist", 
                    command=lambda g=game: self.add_to_wishlist(g)
                )
                wishlist_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        return game_frame
    
    def display_games(self, games=None, is_library=False, is_wishlist=False):
        """Hiển thị danh sách games (có thể là tất cả, thư viện, wishlist, hoặc kết quả tìm kiếm)"""
        # Clear current games
        for widget in self.games_container.winfo_children():
            widget.destroy()
        
        # Nếu không cung cấp danh sách, lấy tất cả games
        if games is None:
            self.games_data = self.games_controller.get_all_games()
            games = self.games_data
        
        # Nếu không có games nào, hiển thị thông báo
        if not games:
            message = "No games found."
            if is_library:
                message = "Your library is empty. Add games to see them here."
            elif is_wishlist:
                message = "Your wishlist is empty. Add games to see them here."
                
            empty_label = ctk.CTkLabel(
                self.games_container, 
                text=message,
                font=ctk.CTkFont(size=16)
            )
            empty_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
            return
        
        # Display games based on current view
        if self.current_view == "grid":
            # Hiển thị dạng lưới (3 cột)
            for i, game in enumerate(games):
                row = i // 3
                col = i % 3
                
                # Create game card
                game_frame = self.create_game_card(
                    self.games_container, game, 
                    is_grid_view=True, 
                    is_library=is_library,
                    is_wishlist=is_wishlist
                )
                game_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        else:
            # Hiển thị dạng danh sách (1 cột)
            for i, game in enumerate(games):
                # Create game card
                game_frame = self.create_game_card(
                    self.games_container, game, 
                    is_grid_view=False,
                    is_library=is_library,
                    is_wishlist=is_wishlist
                )
                game_frame.grid(row=i, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    
    def change_view(self, view_type):
        """Thay đổi kiểu hiển thị (grid/list)"""
        self.current_view = view_type
        
        # Cập nhật lại view hiện tại với dữ liệu hiện có
        if self.content_title.cget("text") == "Your Library":
            self.show_library()
        elif self.content_title.cget("text") == "Your Wishlist":
            self.show_wishlist()
        elif "Search Results" in self.content_title.cget("text"):
            self.display_games(self.games_data)
        else:
            self.display_games()
    
    def add_to_library(self, game):
        """Thêm game vào thư viện"""
        try:
            result = self.lib_controller.add_lib(self.user_id, game.game_id)
            
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
        """Thêm game vào wishlist"""
        try:
            result = self.wishlist_controller.add_wishlist(self.user_id, game.game_id)
            
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
        """Hiển thị trang chủ"""
        # Update the title
        self.content_title.configure(text="Home")
        self.content_subtitle.configure(text="Games you might like")
        
        # Reset sidebar button highlight
        self.reset_sidebar_highlight()
        self.home_button.configure(fg_color=("#2E5984", "#144870"))  # Highlight home button
        
        # Display all games
        self.display_games()
    
    def show_wishlist(self):
        """Hiển thị trang wishlist"""
        # Update the title
        self.content_title.configure(text="Your Wishlist")
        self.content_subtitle.configure(text="Your games collection")
        
        # Reset sidebar button highlight
        self.reset_sidebar_highlight()
        self.wishlist_button.configure(fg_color=("#2E5984", "#144870"))  # Highlight wishlist button
        
        # Get user's wishlist
        user_wl = self.wishlist_controller.get_wishlist_by_user_id(self.user_id)
        
        # Get the game objects for each wishlist item
        wl_games = []
        if user_wl and "product_id" in user_wl and user_wl["product_id"]:
            for game_id in user_wl["product_id"]:
                game = self.games_controller.get_game_by_id(game_id)
                if game:
                    wl_games.append(game)
        
        # Display wishlist games
        self.display_games(wl_games, is_wishlist=True)
    
    def show_library(self):
        """Hiển thị trang thư viện"""
        # Update the title
        self.content_title.configure(text="Your Library")
        self.content_subtitle.configure(text="Your games collection")
        
        # Reset sidebar button highlight
        self.reset_sidebar_highlight()
        self.library_button.configure(fg_color=("#2E5984", "#144870"))  # Highlight library button
        
        # Get user's library
        user_lib = self.lib_controller.get_lib_by_user_id(self.user_id)
        
        # Get the game objects for each library item
        library_games = []
        if user_lib and "product_id" in user_lib and user_lib["product_id"]:
            for game_id in user_lib["product_id"]:
                game = self.games_controller.get_game_by_id(game_id)
                if game:
                    library_games.append(game)
        
        # Display library games
        self.display_games(library_games, is_library=True)
    
    def play_game(self, game):
        """Chơi game từ thư viện"""
        messagebox.showinfo("Play Game", f"Starting {game.game_name}...")
        # Add actual game launch logic here if needed

    def remove_from_library(self, game_id):
        """Xóa game khỏi thư viện"""
        try:
            success = self.lib_controller.delete_lib_by_product_id(self.user_id, game_id)
            
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
        """Xóa game khỏi wishlist"""
        try:
            success = self.wishlist_controller.delete_wishlist_by_product_id(self.user_id, game_id)
            
            if success:
                messagebox.showinfo("Success", "Game removed from your wishlist")
                # Refresh the wishlist view
                self.show_wishlist()
            else:
                messagebox.showerror("Error", "Failed to remove game from your wishlist")
        except Exception as e:
            print(f"Error removing game from wishlist: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
       
    def show_profile_page(self):
        """Hiển thị trang hồ sơ người dùng"""
        # Clear current content
        for widget in self.games_container.winfo_children():
            widget.destroy()
        
        # Update the title
        self.content_title.configure(text="Your Profile")
        self.content_subtitle.configure(text="Manage your account settings")
        
        # Reset sidebar button highlight
        self.reset_sidebar_highlight()
        self.profile_button.configure(fg_color=("#2E5984", "#144870"))  # Highlight profile button
        
        # Create profile frame
        try:
            profile_frame = ProfileFrame(self.games_container, current_user=self.current_user)
            profile_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
        except Exception as e:
            print("Lỗi khi tạo ProfileFrame:", e)
            messagebox.showerror("Error", f"Could not load profile: {str(e)}")

    def search_games_method(self):
        """Tìm kiếm game theo tên"""
        search_term = self.search_entry.get()
        if not search_term:
            return
            
        filtered_games = self.games_controller.get_games_by_name(search_term)

        # Update title to reflect search
        self.content_title.configure(text=f"Search Results for '{search_term}'")
        self.content_subtitle.configure(text=f"{len(filtered_games)} games found")
        
        # Store the filtered games
        self.games_data = filtered_games
        
        # Display the filtered games
        self.display_games(filtered_games)
    
    def reset_sidebar_highlight(self):
        """Reset highlight của tất cả các nút sidebar"""
        default_color = ("#3B8ED0", "#1F6AA5")
        self.home_button.configure(fg_color=default_color)
        self.profile_button.configure(fg_color=default_color)
        self.wishlist_button.configure(fg_color=default_color)
        self.library_button.configure(fg_color=default_color)

    def open_add_game_window(self):
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Add Game")
        self.add_window.geometry("350x320")
        self.add_window.grab_set()

        # Image selection
        self.new_game_img_path = None
        self.tk_img_preview = None
        self.img_label = ctk.CTkLabel(self.add_window, text="No image selected")
        self.img_label.pack(pady=10)
        self.img_btn = ctk.CTkButton(self.add_window, text="Choose Image", command=self.choose_game_image)
        self.img_btn.pack()

        # Game name entry
        self.name_entry = ctk.CTkEntry(self.add_window, placeholder_text="Game Name")
        self.name_entry.pack(pady=10)

        # Game id entry
        self.id_entry = ctk.CTkEntry(self.add_window, placeholder_text="Game ID")
        self.id_entry.pack(pady=10)

        # Add/Cancel buttons
        btn_frame = ctk.CTkFrame(self.add_window)
        btn_frame.pack(pady=20)
        add_btn = ctk.CTkButton(btn_frame, text="Add", command=self.add_game_confirm)
        add_btn.grid(row=0, column=0, padx=10)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=self.add_window.destroy)
        cancel_btn.grid(row=0, column=1, padx=10)

    def choose_game_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.new_game_img_path = file_path
            img = Image.open(file_path).resize((80, 80))
            self.tk_img_preview = ImageTk.PhotoImage(img)
            self.img_label.configure(image=self.tk_img_preview, text="")

    def add_game_confirm(self):
        name = self.name_entry.get()
        game_id_str = self.id_entry.get()
        img_path = self.new_game_img_path

        # Kiểm tra dữ liệu nhập
        if not name or not game_id_str:
            messagebox.showerror("Error", "Please provide both game ID and name.")
            return

        try:
            game_id = int(game_id_str)
        except ValueError:
            messagebox.showerror("Error", "Game ID must be a number.")
            return

        if not img_path:
            messagebox.showerror("Error", "Please provide an image.")
            return

        # Tạo đối tượng Game mới
        new_game = Game(
            game_id=game_id,
            game_name=name,
            image=img_path
        )

        # Sử dụng controller để thêm game
        success = self.games_controller.add_game(new_game)
        if success:
            messagebox.showinfo("Success", "Game added successfully!")
            self.add_window.destroy()
            self.display_games()  # Cập nhật giao diện
        else:
            messagebox.showerror("Error", "Game ID already exists!")

