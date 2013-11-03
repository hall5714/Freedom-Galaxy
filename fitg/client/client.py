import fitg.client.interface as interface
from fitg.conn import Conn
from fitg.game import GameEngine
from fitg.menus import MainMenu

class Client(object):
    """
    This is the main client object representing a client connecting to a server.
    """
    def __init__(self, args):
        self.interface = getattr(interface, args.interface.upper())()
        self.game = None
        self.conn = None

    def connect_to_server(self, host=None, port=None):
        """
        Here we connect to a server using host and port (the Conn class
        will use defaults if passed None), and save the connection.

        TODO: This needs to be wrapped with a context manager and deal
        with exceptions properly

        """
        self.conn = Conn(host, port)

    def create_game(self, scenario, host="localhost", port=None):
        """
        Here we create a new game with a scenario string representing
        which sub-game of FITG we intend to play. The GameEngine will
        be able to look up the initial environment, game conditions,
        player resources etc. that it needs to pre-populate with by
        querying the database.

        We need to make a server, connect to it, have it make a game,
        and join it.

        TODO: Spawn a server process. For now we start it manually.

        """
        self.connect_to_server(host, port)
        self.conn.new_game(scenario)
        self.join_game(self.conn)

    def join_game(self, conn=None, host=None, port=None):
        """
        Here we must assume that a server has been created, so we connect
        to it. We may have been sent an already established
        connection.

        """
        if conn is None:
            self.connect_to_server(host, port)
        scenario = self.conn.which_scenario()
        self.game = GameEngine(scenario)

    def start(self):
        """
        Here we start actually interacting with the user by displaying the
        main menu, which returns an action as a method on client (say,
        create_game()). Anything that interacts with the user (the
        main menu, options menu, game display), is passed the
        interface that this client is using.

        There's a huge todo list here, since we need to be able to
        jump out the game and into a menu. I would guess we could do
        that with an in_game flag for GameEngine that gets unset if
        the user pauses (ESC).

        """
        main_menu = MainMenu(self.interface)
        action = main_menu.display()
        getattr(self, action)()
