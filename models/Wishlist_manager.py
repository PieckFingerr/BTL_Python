from btl.models.Lib_item import Lib
import json
import os

class Wishlist_manager:
    def __init__(self):
        self.wishlist_file = "btl/data/wishlist.json"
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.wishlist_file), exist_ok=True)
        self.load_wishlist_data()
    
    def load_wishlist_data(self):
        try:
            with open(self.wishlist_file, 'r') as file:
                self.wishlist_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize with empty array if file doesn't exist or is invalid
            self.wishlist_data = []
            # Create the file with empty data
            self.save_wishlist_data()
    
    def save_wishlist_data(self):
        with open(self.wishlist_file, 'w') as file:
            json.dump(self.wishlist_data, file, indent=2)
    
    def get_wishlist_by_user_id(self, user_id):
        # Find library entry for the user
        for entry in self.wishlist_data:
            if entry["user_id"] == user_id:
                return entry
        return None  # No library found for this user
    
    def add_wishlist(self, user_id, game_id):
        # Load the latest data
        self.load_wishlist_data()
        
        # Find user's library entry
        user_wishlist = self.get_wishlist_by_user_id(user_id)
        
        if user_wishlist:
            # User already has a library entry
            if "product_id" not in user_wishlist:
                # Initialize product_id as a list if it doesn't exist
                user_wishlist["product_id"] = []
            
            # Check if game is already in library
            if game_id not in user_wishlist["product_id"]:
                # Add the game to the list
                user_wishlist["product_id"].append(game_id)
                self.save_wishlist_data()
                return True
            return False  # Game already in library
        else:
            # Create new library entry for user
            new_entry = {
                "user_id": user_id,
                "product_id": [game_id]
            }
            self.wishlist_data.append(new_entry)
            self.save_wishlist_data()
            return True
    
    def delete_wishlist_by_product_id(self, user_id, game_id):
        # Load the latest data
        self.load_wishlist_data()
        
        # Find user's library entry
        user_wishlist = self.get_wishlist_by_user_id(user_id)
        
        if user_wishlist and "product_id" in user_wishlist and game_id in user_wishlist["product_id"]:
            # Remove the game from the list
            user_wishlist["product_id"].remove(game_id)
            self.save_wishlist_data()
            return True
        return False  # Game not in library or user not found