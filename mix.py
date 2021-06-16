# nizan mandelblit, 313485468, eldad horvitz, 314964438
import socket, os, datetime, random, sys
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def main():
    print("hi from mix")
    Y = "sk" + sys.argv[1] + ".pem"
    port = sys.argv[2]
    with open(Y, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

    s = socket.socket()  # Create a socket object
    s.bind(("127.0.0.1", int(port)))  # Bind to the port
    s.listen()  # Now wait for client connection.
    while True:
        c, addr = s.accept()  # Establish connection with client.
        print('Got connection from', addr)
        decryptedMsg = private_key.decrypt(c.recv(1024), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                      algorithm=hashes.SHA256(), label=None))
        socket.inet_ntoa(decryptedMsg[0:4])


        print(decryptedMsg)
        c.close()  # Close the connection


if __name__ == '__main__':
    main()
