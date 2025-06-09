import requests
import json

class RawgController:
    def __init__(self):
        self.api_key = "e6b57cc327e8460f87256e19a99862d0"  # API Key
        self.base_url = "https://api.rawg.io/api"

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

                games.append({
                    "game_id": game_id,
                    "game_name": game.get("name", ""),
                    "image": game.get("background_image", ""),
                })
                
            # Lưu vào file JSON
            with open("btl\\data\\games.json", "w", encoding="utf-8") as file:
                json.dump(games, file, indent=4, ensure_ascii=False)

            return games, "Lay dữ liệu thành công từ API"

        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi gọi API: {e}")
            return []