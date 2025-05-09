import os
import json


class LibController:
    def __init__(self):
        self.lib_file = "btl/data/lib.json"
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.lib_file), exist_ok=True)
        self.load_lib_data()

    
    def load_lib_data(self):
        try:
            with open(self.lib_file, 'r') as file:
                self.lib_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize with empty array if file doesn't exist or is invalid
            self.lib_data = []
            # Create the file with empty data
            self.save_lib_data()
    
    def save_lib_data(self):
        with open(self.lib_file, 'w') as file:
            json.dump(self.lib_data, file, indent=2)
    
    def get_lib_by_user_id(self, user_id):
        # Find library entry for the user
        for entry in self.lib_data:
            if entry["user_id"] == user_id:
                return entry
        return None  # No library found for this user
    
    def add_lib(self, user_id, game_id):
        # Load the latest data
        self.load_lib_data()
        
        # Find user's library entry
        user_lib = self.get_lib_by_user_id(user_id)
        
        if user_lib:
            # User already has a library entry
            if "product_id" not in user_lib:
                # Initialize product_id as a list if it doesn't exist
                user_lib["product_id"] = []
            
            # Check if game is already in library
            if game_id not in user_lib["product_id"]:
                # Add the game to the list
                user_lib["product_id"].append(game_id)
                self.save_lib_data()
                return True
            return False  # Game already in library
        else:
            # Create new library entry for user
            new_entry = {
                "user_id": user_id,
                "product_id": [game_id]
            }
            self.lib_data.append(new_entry)
            self.save_lib_data()
            return True
    
    def delete_lib_by_product_id(self, user_id, game_id):
        # Load the latest data
        self.load_lib_data()
        
        # Find user's library entry
        user_lib = self.get_lib_by_user_id(user_id)
        
        if user_lib and "product_id" in user_lib and game_id in user_lib["product_id"]:
            # Remove the game from the list
            user_lib["product_id"].remove(game_id)
            self.save_lib_data()
            return True
        return False  # Game not in library or user not found