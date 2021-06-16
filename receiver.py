# nizan mandelblit, 313485468, eldad horvitz, 314964438
import socket, os, datetime, random, sys
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from datetime import datetime


def main():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    password = sys.argv[1]
    salt = sys.argv[2]
    port = sys.argv[3]
    password = str.encode(password)
    salt = str.encode(salt)
    kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 100000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    # socket
    s = socket.socket()  # Create a socket object
    s.bind(("127.0.0.1", int(port)))  # Bind to the port
    s.listen()  # Now wait for client connection.
    while True:
        c, addr = s.accept()  # Establish connection with client.
        message = c.recv(1024)
        message=f.decrypt(str.encode(message.decode()))

        c.close()  # Close the connection
        print(str(message.decode()) + " " + current_time)


if __name__ == '__main__':
    main()
