from btl.models.Game import Game
import json

class GameController:
    def __init__(self, json_path="btl\\data\\games.json"):
        self.json_path = json_path
        self.games = []
        self.load_games()

    def load_games(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                games_data = json.load(file)
                
                self.games = []
                for game_data in games_data:
                    game = Game(
                        game_id = game_data.get("game_id"),
                        game_name = game_data.get("game_name"),
                        image = game_data.get("image", "")
                    )
                    self.games.append(game)
        except FileNotFoundError:
            print(f"Không tìm thấy file: {self.json_path}")
        except json.JSONDecodeError:
            print(f"Lỗi khi đọc file: {self.json_path}")

    def get_all_games(self):
        return self.games
    
    def get_game_by_id(self, game_id):
        for game in self.games:
            if game.game_id == game_id:
                return game
        return None
    
    # Tìm kiếm games theo tên dù chỉ đúng 1 từ hay cả tên game 
    def get_games_by_name(self, game_name):
        return [game for game in self.games if game_name in game.game_name]
    
    def get_games_by_genre(self, genre):
        return [game for game in self.games if genre in game.genre]
    
    def get_games_by_developer(self, developer):
        return [game for game in self.games if developer in game.devs]
    
    def add_game(self, new_game):
        # Đọc dữ liệu gốc từ file nếu cần
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                games_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            games_data = []

        # Kiểm tra trùng lặp game_id
        for game_data in games_data:
            if game_data.get("game_id") == new_game.game_id:
                print("Game ID already exists!")
                return False

        # Tạo dict từ Game object mới
        new_game_dict = {
            "game_id": new_game.game_id,
            "game_name": new_game.game_name,
            "image": new_game.image
        }

        # Thêm game mới vào danh sách
        games_data.append(new_game_dict)

        # Ghi dữ liệu vào file JSON
        with open(self.json_path, "w", encoding="utf-8") as file:
            json.dump(games_data, file, indent=4, ensure_ascii=False)

        # Cập nhật self.games
        self.games.append(new_game)
        print("Game added successfully!")
        return True



            
