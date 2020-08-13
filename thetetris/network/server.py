#!/usr/bin/env python3

import socket

import constants


class Server:

    def __init__(self, req_code):
        # Global variable
        self.BUFFER_SIZE = constants.BUFFER_SIZE
        self.server_address = constants.server_ip
        self.playing = True
        self.req_code = req_code
        self.conn = None
        self.neg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Validate arguments
        try:
            int(self.req_code)
        except ValueError:
            print("req_code must be an integer")
            exit()

        # Bind with port number 54241 (or any forwarded port)
        self.neg_socket.bind((self.server_address, constants.r_port))

    def server_negotiation(self):

        # Accept connection with a client and get the code
        conn, _ = self.neg_socket.accept()
        self.conn = conn
        code = self.conn.recv(self.BUFFER_SIZE)

        # Confirm code is int
        try:
            code = code.decode("utf-8")
            code = int(code)
        except:
            print("code from client must be an integer")
            return False

        # Verify if the client code is acceptable
        if self.req_code == code:
            # Accept the request
            self.conn.send("0".encode("utf-8"))
            return True

        # Client failed to provide correct code
        else:
            self.conn.send("1".encode("utf-8"))
            self.conn.close()
        return False

    def server_transaction(self, msg):
        """
        server_negotiation: socket.socket -> None

        server_negotiation retrieves a string from a verified client
        to reverse the string and send it back to the client.
        """

        opponent_grid = self.conn.recv(self.BUFFER_SIZE)

        # Check if the client replied
        if not opponent_grid:
            print("connection lost")
            self.playing = False
            return

        self.conn.send(msg)

        return opponent_grid


def start_server(grid, queue):

    o = Server(constants.req_code)

    while True:
        # Wait for a client to connect
        print("wait for a client to connect")
        o.neg_socket.listen(1)

        # Perform the negotiation step
        established = o.server_negotiation()

        # Exit here if server needs to shut down after incorrect req_code

        if not established:
            print("req_code is incorrect")
            continue

        print("connection established")
        while o.playing:
            # Perform the transaction step
            queue.put(list(o.server_transaction(grid)))

        o.conn.close()
        o.playing = True  # Reset the playing value


# if __name__ == "__main__":
#     o = Server(13)
#     try:
#         start_server(o, bytearray([0] * 10))
#     except KeyboardInterrupt:
#         o.neg_socket.close()
