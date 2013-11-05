from __future__ import print_function

import utils
import logging
import json
import time
import snakemq.link
import snakemq.packeter
import snakemq.messaging
import snakemq.message
import threading
import logging
import uuid
import inspect

logging.basicConfig()

#@utils.borg
class EventQueue(threading.Thread):
    """An event queue.
    :todo: stuff
    """

    def __init__(self, client_name, callback=lambda *a: a):
        """Prepares the callback method and logger.
        """
        threading.Thread.__init__(self)
        self.callback = callback
        self.client_name = str(client_name)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.info("Initializing the EventQueue as " + self.client_name + " in thread " + self.name)
        self._setup_link()

    def _setup_link(self):
        """Prepares the SnakeMQ communication
        """
        self.link = snakemq.link.Link()
        packeter = snakemq.packeter.Packeter(self.link)
        self.messaging = snakemq.messaging.Messaging(self.client_name, "", packeter)
        self.messaging.on_message_recv.add(self.callback)

    def disconnect(self):
        """Disconnects from the Server.
        """
        self.link.stop()

    def listen(self, port):
        """Prepares the listener. 

        Prepares to listen on localhost:``port``. Does not establish connection until
        EventQueue.start() is called.

        :param port: The port to listen on.
        :type name: int.
        """
        self.logger.info("Starting to listen on localhost:" + str(port))
        self.link.add_listener(("", port))

    def connect(self, host, port):
        """Prepares the connector. 

        Prepares to connect to a listener on ``host``:``port``. Does not establish connection until
        EventQueue.start() is called.

        :param host: The host IP address to connect to.
        :type host: int.
        :param port: The port to connect to.
        :type port: int.
        """
        self.logger.info("Attempting to connect to " + host + ":" + str(port))
        self.link.add_connector((host, port))

    def run(self):
        """Executes the listener and connector. 

        Executues the main loop. Called internally when EventQueue.start() is called.
        """
        self.logger.info("Beggining the main loop")
        self.link.loop();

    def message(self, message, receipient):
        """Sends a message.

        JSON encodes a Python data type into JSON and sends it via SnakeMQ

        :param message: The message to send.
        :type message: mixed.
        :param receipient: The unique id to send the message to.
        :type receipient: str.
        """
        json_message = bytes(json.dumps(message))
        encoded_message = snakemq.message.Message(json_message, ttl=600)
        self.messaging.send_message(receipient, encoded_message)


class Action:
    """Server handler for client actions
    """
    allowed_actions = ['move']

    def __init__(self, host, port, callback):
        """Initializes an action class.

        Initializes the EventQueue on ``host``:``port``. Upon a response from the receipient of a message, 
        ``callback`` is called with the following attributes:

        :param host: The host IP address to connect to.
        :type host: int.
        :param port: The port to connect to.
        :type port: int.
        :param callback: A function which is called on response from the server.
        """
        self.queue = EventQueue(uuid.uuid4(), callback)
        self.queue.connect(host, port)
        self.queue.start()

    def __getattr__(self, name, **kwargs):
        """Class attribute overrider.

        Called when a method or attribute that doesn't exist is called.

        :param name: The method that was called.
        :type name: str.
        :param **kwargs: The dictionary of arguments called with the functino.
        :type **kwargs: dict.
        """

        def function(**kwargs):
            """Class function overrider.

            Called when a method that doesn't exist is called on the class. Allowed method over riding
            for the Action class.

            :param **kwargs: The dictionary of arguments called with the functino.
            :type **kwargs: dict.
            """
            if name in self.allowed_actions:
                self.action = dict(kwargs)
                self.action['action'] = name
                self.send()
            else:
                raise AttributeError("Action object has no attribute %r" % (name))
        return function

    def send(self):
        """Sends a message via EventQueue.
        """
        self.queue.message(self.action, "Backend")

    def disconnect(self):
        """Disconnects from the EventQueue.
        """
        self.queue.disconnect()


class ActionHandler:
    """Server handler for client actions
    """

    def handler(self, conn, ident, message):
        """Callback handler for the backend.

        :param conn: The connection being used.
        :type conn: mixed.
        :param ident: The unique ID of the message sender.
        :type ident: str.
        :param message: The json-encoded message being sent.
        :type message: str.
        """
        self.message = json.loads(message.data)
        try:
            method = getattr(self, message.data.action)
            method(**message.data)
        except AttributeError:
            #print(self.message['action']);
            pass

    def move(**kwargs):
        # using fitg.backend.orm.Stack
        # stack = new Stack(kwargs['stack_id'])
        # do other stuff...
        pass

    def respond():
        # will use this to respond back to messages
        pass



if __name__ == "__main__":

    handler = ActionHandler()

    listener = EventQueue("Backend", handler.handler)
    listener.listen(4000)
    listener.start()

    action = Action('localhost', 4000, lambda *a: print("Client Message received."))
    action.move(stack_id=1, location_id=1)

    time.sleep(2)

    action.disconnect()
    listener.disconnect()