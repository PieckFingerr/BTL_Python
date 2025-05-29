class Game:
    def __init__(self, game_id, game_name, image):
        self.game_id = game_id
        self.game_name = game_name
        self.image = image

    def to_dict(self):
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
            "image": self.image
        }