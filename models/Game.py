class Game:
    def __init__(self, game_id, game_name, description, release_date, rating, genre, devs, image):
        self.game_id = game_id
        self.game_name = game_name
        self.description = description
        self.release_date = release_date
        self.rating = rating
        self.genre = genre
        self.devs = devs
        self.image = image

    def to_dict(self):
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
            "description": self.description,
            "release_date": self.release_date,
            "rating": self.rating,
            "genre": self.genre,
            "devs": self.devs,
            "image": self.image
        }