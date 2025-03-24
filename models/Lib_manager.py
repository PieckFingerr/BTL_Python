from btl.models.Lib_item import Lib
from btl.models.Game import Game
import json
import datetime

class Lib_manager:
    def __init__(self, json_path="btl\\data\\lib.json"):
        self.json_path = json_path
        self.load_libs()

    def load_libs(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            print(f"Không tìm thấy file: {self.json_path}")
        except json.JSONDecodeError:
            print(f"Lỗi khi đọc file: {self.json_path}")
