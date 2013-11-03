from fitg.conn import Conn
from fitg.database import Database
from fitg.parser import Parser

class Server(object):
    """
    This is the main server object, representing a server to which
    clients connect.

    This server makes a database and populates it using the parser.

    """

    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.conn = None
        self.database = Database()

    def parse_data(self):
        """
        This will call the parser which parses information from the
        provided data files.

        TODO: Write the parser, hand it the data files, have the
        database ready to be filled.

        """
        parser = Parser()
        return parser.parse()

    def make_database(self):
        """
        This will get an empty database with the proper schema using the
        database class. It then initializes it with the data returned
        from the parse.

        """
        database = Database()
        database.init(self.parse_data())

    def start(self):
        """
        This starts the server by making the database and listening for
        commands/queries from the conn class. It also must be able to
        push new information to a client. The architecture of this
        back-and-forth communication may be in place already by
        Justin.

        """
        self.make_database()
        self.conn.listen(self.host, self.port)
