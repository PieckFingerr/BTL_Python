from btl.models.User_manager import UserManager
import json

class UserController:
    def __init__(self):
        self.user_manager = UserManager() 
    
    def change_password(self, user_id, current_password, new_password):
        return self.user_manager.change_password(user_id, current_password, new_password)
    
    def change_username(self, user_id, new_username):
        return self.user_manager.change_username(user_id, new_username)
    
    def change_email(self, user_id, new_email):
        return self.user_manager.change_email(user_id, new_email)
    
    def get_all_users_id(self):
        return self.user_manager.get_all_users_id()
    
    def get_user_by_id(self, user_id):
        return self.user_manager.get_user_by_id(user_id)
    
    def get_current_username(self, user_id):
        return self.user_manager.get_current_username(user_id)
    
    
