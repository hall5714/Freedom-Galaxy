from argparse import ArgumentParser
from fitg.client import Client
from fitg.server import Server
from fitg.conn import Conn

main_parser = ArgumentParser(description = "Let's play some FITG")
main_parser.add_argument("-r", "--role", default = "client", choices =
                         ["client", "server"],
                         help = "Start a client or a server.")

client_parser = ArgumentParser(description = "Client")
client_parser.add_argument("-i", "--interface", default = "cli",
                          choices = ["cli", "gui"],
                          help = "Specifies which user interface to use.")

server_parser = ArgumentParser(description="Server options")
server_parser.add_argument("-h", "--host", default = "localhost",
                           help = "Specifies which host to connect to.")
server_parser.add_argument("-p", "--port", type = int, default = 3830,
                           help = "Specifies which port to connect to.")

def start_client(args):
    """
    The client class will hold an interface object for user
    interaction, and will present a main menu, from which a game can
    be started. It will have bi-directional communcation with the
    server through the Conn class.

    """
    client = Client(args)
    client.start()

def start_server(args):
    """
    The server class will hold the database representing the game
    state, and will have bi-directional communication with the clients
    through the Conn class.

    """
    server = Server(args)
    server.start()

if __name__ == "__main__":
    main_arguments = main_parser.parse_args()
    if main_arguments.role == "client":
        client_arguments = client_parser.parse_args()
        start_client(client_arguments)
    elif main_arguments.role == "server":
        # TODO: have client spawn a server process
        server_arguments = server_parser.parse_args()
        start_server(server_arguments)
