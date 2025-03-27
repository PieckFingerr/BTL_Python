import json
from btl.models.Game import Game

class GameManager:
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
                        description = game_data.get("description"),
                        release_date = game_data.get("release_date"),
                        rating = game_data.get("rating", 0.0),
                        genre = game_data.get("genre", []),
                        devs = game_data.get("devs", []),
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