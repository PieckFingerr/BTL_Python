from btl.models.Game import Game
from btl.models.User import User

class Lib(Game):
    def __init__(self, game_id, game_name, description, release_date, rating, genre, devs, image, user_id):
        super().__init__(game_id, game_name, description, release_date, rating, genre, devs, image)
        self.user_id = user_id

    def to_dict(self):
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
            "description": self.description,
            "release_date": self.release_date,
            "rating": self.rating,
            "genre": self.genre,
            "devs": self.devs,
            "image": self.image,
            "user_id": self.user_id
        }