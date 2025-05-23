class Wishlist():
    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return f'<Lib {self.user_id} {self.product_id}>'
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'product_id': self.product_id
        }