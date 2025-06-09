from btl.views.auth_view import AuthApp
from btl.controllers.rawg_controller import RawgController




if __name__ == "__main__":
    # Start the application
    app = AuthApp()
    app.mainloop()

    # Initialize the RawgController to fetch game data
    rawg_controller = RawgController()
    rawg_controller.get_games()


