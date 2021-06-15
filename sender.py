# nizan mandelblit, 313485468, eldad horvitz, 314964438
import socket, os, datetime, random, sys
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class messegeSender:
    def __init__(self, message, path, round, password, salt, dest_ip, dest_port):
        self.message = message
        self.path = path
        self.round = round
        self.password = password
        self.salt = salt
        self.dest_ip = dest_ip
        self.dest_port = dest_port


def main():
    print("hi from sender")
    #get data from messages file
    messegeSenderArray=[]
    X = "messages" + sys.argv[1] + ".txt"
    messges = open(X, "r")
    for line in messges.readlines():
        feature = line.split(" ")
        message = feature[0]
        path = feature[1]
        round = feature[2]
        password = feature[3]
        salt = feature[4]
        dest_ip = feature[5]
        dest_port = feature[6]
        messegeSenderArray.append(messegeSender(message,path,round,password,salt,dest_ip,dest_port))
        x = 2
    messges.close()

    #get data from messages file
    messegeSenderArray=[]
    X = "messages" + sys.argv[1] + ".txt"
    messges = open(X, "r")
    for line in messges.readlines():
        feature = line.split(" ")
        message = feature[0]
        path = feature[1]
        round = feature[2]
        password = feature[3]
        salt = feature[4]
        dest_ip = feature[5]
        dest_port = feature[6]
        messegeSenderArray.append(messegeSender(message,path,round,password,salt,dest_ip,dest_port))
        x = 2
    messges.close()
    for messegeToSend in messegeSenderArray:
        s = socket.socket()  # Create a socket object
        s.connect((messegeToSend.dest_ip, 12345))
        s.sendall('Here I am!'.encode())
        s.close()  # Close the socket when done
    # load PKs
    servers = path.split(",")
    servers.reverse()
    message=b"hlukkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkh!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    for server in servers:
        key = "sk" + server + ".pem"
        skfile = open(key, "rb")
        public_key = serialization.load_pem_public_key(skfile.read())
        ciphertext = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )


if __name__ == '__main__':
    main()
