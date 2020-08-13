#!/usr/bin/env python3

import socket

import constants


class Client:

    def __init__(self, server_address, r_port, req_code):
        # Global Variable
        self.BUFFER_SIZE = constants.BUFFER_SIZE
        self.server_address = server_address
        self.r_port = r_port
        self.req_code = req_code
        self.neg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keepPlaying = True

        # Validate
        try:
            int(self.req_code)  # just check if req_code is int
        except ValueError:
            print("n_port and req_code must be integers")
            exit()

    def client_negotiation(self):
        """
        client_negotiation: str, int, int -> int

        client_negotiation asks the server for a port to talk to using UDP.
        If the verification is successful, it returns the port number.
        If the verification is unsuccessful, it returns 0.
        """

        # Check if the server is up
        try:
            self.neg_socket.connect((self.server_address, self.r_port))
        except socket.error as e:
            if e.errno == 111:
                print("Cannot connect to the server.")
                print("Make sure the server is running and you entered"
                      + " correct server address and n_port.")
                self.neg_socket.close()
                exit()

        # Send the request code for verification and get the response
        code = str(self.req_code)
        self.neg_socket.send(code.encode("utf-8"))
        resp = self.neg_socket.recv(self.BUFFER_SIZE)
        resp = int(resp.decode("utf-8"))

        # If the request code is incorrect
        if resp == 1:
            print("req code not roccet")

        return resp

    def client_transaction(self, msg):
        """
        client_transaction: str, int, str -> None

        client_transaction sends the string to be reversed
        and get the reversed string from the server using UDP.
        It also prints the retrieved reversed string.
        """

        self.neg_socket.send(msg)
        resp = self.neg_socket.recv(self.BUFFER_SIZE)

        return resp


def connect_client(grid, queue):
    o = Client(constants.server_ip, constants.r_port, constants.req_code)

    # Negotiation step
    resp = o.client_negotiation()
    if resp != 0:
        # Authentication failed
        print("authentication failed")
        exit()

    # Transaction step
    while o.keepPlaying:
        queue.put(list(o.client_transaction(grid)))
    # o.neg_socket.shutdown(socket.SHUT_RDWR)
    o.neg_socket.close()


# if __name__ == "__main__":
#     connect_client(bytearray([0] * 10))
