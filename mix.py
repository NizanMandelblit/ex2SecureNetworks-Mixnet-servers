# nizan mandelblit, 313485468, eldad horvitz, 314964438

import socket
import sys
import struct

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def main():
    # create the sk
    Y = "sk" + sys.argv[1] + ".pem"
    port = sys.argv[2]
    with open(Y, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
    # open socket to listen
    s = socket.socket()  # Create a socket object
    s.bind(("127.0.0.1", int(port)))  # Bind to the port
    s.listen()  # Now wait for client connection.
    while True:
        c, addr = s.accept()  # Establish connection with client.
        # get and decrypt the message
        decryptedMsg = c.recv(8192)
        decryptedMsg = private_key.decrypt(decryptedMsg, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                      algorithm=hashes.SHA256(), label=None))
        # gets the ip and port of the next router ans send
        ipSend = socket.inet_ntoa(decryptedMsg[0:4])
        portSend = struct.unpack('>h', decryptedMsg[4:6])[0]
        send = socket.socket()  # Create a socket object
        send.connect((ipSend, portSend))
        send.sendall(decryptedMsg[6:])


if __name__ == '__main__':
    main()
