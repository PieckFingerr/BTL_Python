import requests
import json

class RawgController:
    def __init__(self):
        self.api_key = "e6b57cc327e8460f87256e19a99862d0"  # API Key
        self.base_url = "https://api.rawg.io/api"

    def get_game_details(self, game_id):
        """Lấy thông tin chi tiết của game bao gồm developers"""
        url = f"{self.base_url}/games/{game_id}?key={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi lấy thông tin chi tiết game {game_id}: {e}")
            return {}

    def get_games(self, page=1, page_size=40):
        url = f"{self.base_url}/games?key={self.api_key}&page={page}&page_size={page_size}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            
            data = response.json()
            games_list = data.get("results", [])
            
            games = []
            for game in games_list:
                game_id = game.get("id")
                
                # Lấy thông tin chi tiết bao gồm developers
                game_details = self.get_game_details(game_id)
                
                # Xử lý thể loại để chỉ lấy tên
                genres = [genre["name"] for genre in game.get("genres", ", ")]
                
                # Xử lý developers để chỉ lấy tên
                developers = [dev["name"] for dev in game_details.get("developers", ", ")]
                
                games.append({
                    "game_id": game_id,
                    "game_name": game.get("name", ""),
                    "image": game.get("background_image", ""),
                })
                
            # Lưu vào file JSON
            with open("btl\\data\\games.json", "w", encoding="utf-8") as file:
                json.dump(games, file, indent=4, ensure_ascii=False)

            return games

        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi gọi API: {e}")
            return []