from btl.views.auth_view import AuthApp
from btl.controllers.rawg_controller import RawgController


if __name__ == "__main__":
    auth = AuthApp()
    auth.mainloop()

