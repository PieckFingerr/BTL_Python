from btl.models.User import User
import json


class UserManager:
    def __init__(self, json_path="btl\\data\\users.json"):
        self.json_path = json_path
        self.users = []
        self.load_users()

    def load_users(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                users_data = json.load(file)

                self.users = []
                for user_data in users_data:
                    user = User(
                        user_id=user_data.get("user_id"),
                        username=user_data.get("username"),
                        password=user_data.get("password"),
                        email=user_data.get("email")
                    )
                    self.users.append(user)
        except FileNotFoundError:
            print(f"Không tìm thấy file: {self.json_path}")
        except json.JSONDecodeError:
            print(f"Lỗi khi đọc file: {self.json_path}")

        def save_users(self):
            """Lưu danh sách người dùng vào file JSON"""
            try:
                users_data = []
                for user in self.users:
                    user_dict = {
                        "user_id": user.user_id,
                        "username": user.username,
                        "password": user.password,
                        "email": user.email
                    }
                    users_data.append(user_dict)
                    
                with open(self.json_path, "w", encoding="utf-8") as file:
                    json.dump(users_data, file, indent=4, ensure_ascii=False)
                return True
            except Exception as e:
                print(f"Lỗi khi lưu file: {e}")
                return False
            
    def get_all_users_id(self):
        """Lấy danh sách tất cả user_id"""
        return [user.user_id for user in self.users]

    def get_user_by_id(self, user_id):
        """Lấy thông tin người dùng theo ID"""
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def get_current_username(self, user_id):
        """Lấy tên người dùng hiện tại theo ID"""
        user = self.get_user_by_id(user_id)
        if user:
            return user.username
        return None

    def change_password(self, user_id, current_password, new_password):
        """Thay đổi mật khẩu người dùng"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False, "Không tìm thấy người dùng"
            
        if user.password != current_password:
            return False, "Mật khẩu hiện tại không đúng"
            
        user.password = new_password
        success = self.save_users()
        if success:
            return True, "Đổi mật khẩu thành công"
        else:
            return False, "Lỗi khi lưu thay đổi"

    def change_username(self, user_id, new_username):
        """Thay đổi tên người dùng"""
        # Kiểm tra xem tên đã tồn tại chưa
        for user in self.users:
            if user.username == new_username and user.user_id != user_id:
                return False, "Tên người dùng đã tồn tại"
        
        user = self.get_user_by_id(user_id)
        if not user:
            return False, "Không tìm thấy người dùng"
            
        user.username = new_username
        success = self.save_users()
        if success:
            return True, "Đổi tên người dùng thành công"
        else:
            return False, "Lỗi khi lưu thay đổi"
            
    def change_email(self, user_id, new_email):
        """Thay đổi email người dùng"""
        # Kiểm tra xem email đã tồn tại chưa
        for user in self.users:
            if user.email == new_email and user.user_id != user_id:
                return False, "Email đã được sử dụng"
        
        user = self.get_user_by_id(user_id)
        if not user:
            return False, "Không tìm thấy người dùng"
            
        user.email = new_email
        success = self.save_users()
        if success:
            return True, "Đổi email thành công"
        else:
            return False, "Lỗi khi lưu thay đổi"