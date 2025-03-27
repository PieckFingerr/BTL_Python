import customtkinter as ctk
from tkinter import messagebox

from btl.controllers.user_controller import UserController

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        self.current_user = current_user

        # Safely get user_id with a default value

        # Sử dụng user_id khi cần
        if self.current_user and "user_id" in self.current_user:
            self.user_id = self.current_user["user_id"]

        if self.current_user and "password" in self.current_user:
            self.password = self.current_user["password"]

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Profile header section
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        # User profile icon
        self.profile_icon = ctk.CTkLabel(
            self.header_frame,
            text="👤",
            font=ctk.CTkFont(size=48)
        )
        self.profile_icon.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        # Username label
        username_text = "Guest" if self.current_user is None else self.current_user["username"]
        self.username_label = ctk.CTkLabel(
            self.header_frame,
            text=username_text,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.username_label.grid(row=1, column=0, padx=20, pady=(5, 20))
        
        # Profile options section
        self.options_frame = ctk.CTkFrame(self, corner_radius=10)
        self.options_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.options_frame.grid_columnconfigure(0, weight=1)
        
        # Profile option buttons
        self.change_username_button = ctk.CTkButton(
            self.options_frame,
            text="Change Username",
            height=40,
            corner_radius=8,
            command=self.change_username
        )
        self.change_username_button.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.change_password_button = ctk.CTkButton(
            self.options_frame,
            text="Change Password",
            height=40,
            corner_radius=8,
            command=self.change_password
        )
        self.change_password_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Divider
        self.divider = ctk.CTkFrame(self.options_frame, height=2, fg_color="gray70")
        self.divider.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
    # Placeholder methods for the button commands
    def change_username(self):
        # Create a dialog to change username
        dialog = ctk.CTkToplevel(self)
        dialog.title("Change Username")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make dialog modal
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Dialog content
        frame = ctk.CTkFrame(dialog, corner_radius=0)
        frame.pack(fill="both", expand=True)
        
        # Username entry
        label = ctk.CTkLabel(frame, text="New Username:")
        label.pack(pady=(20, 5))
        
        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def save_username():
            new_username = entry.get()
            
            if not new_username:
                messagebox.showerror("Error", "Username is required!")
                return
                
            # Here you would update the username in your database
            change_username(self, new_username)
            self.current_user["username"] = new_username
            # For now, we'll just show a success message
            messagebox.showinfo("Success", "Username updated successfully!")
            dialog.destroy()
        
        save_button = ctk.CTkButton(button_frame, text="Save", command=save_username)
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side="left", padx=10)
    
    def change_password(self):
        # Create a dialog to change password
        dialog = ctk.CTkToplevel(self)
        dialog.title("Change Password")
        dialog.geometry("400x280")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make dialog modal
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Dialog content
        frame = ctk.CTkFrame(dialog, corner_radius=0)
        frame.pack(fill="both", expand=True)
        
        # Password entries
        current_label = ctk.CTkLabel(frame, text="Current Password:")
        current_label.pack(pady=(20, 5))
        
        current_entry = ctk.CTkEntry(frame, width=300, show="*")
        current_entry.pack(pady=5)
        
        new_label = ctk.CTkLabel(frame, text="New Password:")
        new_label.pack(pady=(10, 5))
        
        new_entry = ctk.CTkEntry(frame, width=300, show="*")
        new_entry.pack(pady=5)
        
        confirm_label = ctk.CTkLabel(frame, text="Confirm New Password:")
        confirm_label.pack(pady=(10, 5))
        
        confirm_entry = ctk.CTkEntry(frame, width=300, show="*")
        confirm_entry.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def save_password():
            current = current_entry.get()
            new = new_entry.get()
            confirm = confirm_entry.get()

            if not current or not new or not confirm:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            if new != confirm:
                messagebox.showerror("Error", "New passwords do not match!")
                return
                
            # Here you would verify the current password and update in your database
            change_password(self.user_id, self.password, new)
            # For now, we'll just show a success message
            messagebox.showinfo("Success", "Password updated successfully!")
            dialog.destroy()
        
        save_button = ctk.CTkButton(button_frame, text="Save", command=save_password)
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side="left", padx=10)
    
def change_username(user_id, new_username):
    user_controller = UserController()
    return user_controller.change_username(user_id, new_username)

def change_password(user_id, current_password, new_password):
    user_controller = UserController()
    return user_controller.change_password(user_id, current_password, new_password)


