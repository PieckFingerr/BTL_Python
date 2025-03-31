from btl.models.Wishlist_manager import Wishlist_manager
from btl.models.User_manager import UserManager

class WishlistController:
    def __init__(self):
        self.wishlist_manager = Wishlist_manager()
        self.user_manager = UserManager()

    def get_wishlist_by_user_id(self, user_id):
        """Lấy danh sách sản phẩm của người dùng theo ID"""
        return self.wishlist_manager.get_wishlist_by_user_id(user_id)
    
    def delete_wishlist_by_product_id(self, user_id, product_id):
        return self.wishlist_manager.delete_wishlist_by_product_id(user_id, product_id)
    
    def add_wishlist(self, user_id, product_id):
        return self.wishlist_manager.add_wishlist(user_id, product_id)