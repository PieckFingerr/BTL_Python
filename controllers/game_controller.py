from btl.models.Game_manager import GameManager

class GameController:
    def __init__(self):
        self.game_manager = GameManager()

    def get_all_games(self):
        """Lấy tất cả game để hiển thị ra view"""
        return self.game_manager.get_all_games()
    
    def get_game_by_id(self, game_id):
        """Lấy thông tin chi tiết của một game để hiển thị ra view"""
        return self.game_manager.get_game_by_id(game_id)
    
    def search_games_by_genre(self, genre):
        """Tìm kiếm games theo thể loại"""
        return self.game_manager.get_games_by_genre(genre)
    
    def search_games_by_developer(self, developer):
        """Tìm kiếm games theo nhà phát triển"""
        return self.game_manager.get_games_by_developer(developer)
    
    def get_games_by_name(self, game_name):
        """Tìm kiếm games theo tên game"""
        return self.game_manager.get_games_by_name(game_name)