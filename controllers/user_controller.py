from btl.models.User_manager import UserManager
import json

from btl.models.User_manager import UserManager
# Compare this snippet from btl/controllers/user_controller.py:
class UserController:
    def __init__(self):
        self.user_manager = UserManager()

    
    def change_password(self, user_id, current_password, new_password):
            return self.user_manager.change_password(user_id, current_password, new_password)
        
    def change_username(self, user_id, new_username):
            return self.user_manager.change_username(user_id, new_username)
        
    def get_current_username(self, user_id):
            return self.user_manager.get_current_username(user_id)
        
    
