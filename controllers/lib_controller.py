from btl.models.Lib_manager import Lib_manager
from btl.models.User_manager import UserManager

class LibController:
    def __init__(self):
        self.lib_manager = Lib_manager()
        self.user_manager = UserManager()

    def get_lib_by_user_id(self, user_id):
        """Lấy danh sách sản phẩm của người dùng theo ID"""
        return self.lib_manager.get_lib_by_user_id(user_id)
    
    def delete_lib_by_product_id(self, user_id, product_id):
        return self.lib_manager.delete_lib_by_product_id(user_id, product_id)
    
    def add_lib(self, user_id, product_id):
        return self.lib_manager.add_lib(user_id, product_id)