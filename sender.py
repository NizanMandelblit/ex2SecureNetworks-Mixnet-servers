# nizan mandelblit, 313485468, fullname 2, id 2
import socket, os, datetime, random, sys
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class messegeSender:
    def __init__(self, message, path, round, password, salt, dest_ip, dest_port):
        self.message = message
        self.path = path
        self.round = round
        self.password = password
        self.salt = salt
        self.dest_ip = dest_ip
        self.dest_port = dest_port


def Enc(salt, password, messege):
    password = str.encode(password)
    salt = str.encode(salt)
    kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 100000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    print("key: ".encode()+ key)
    f = Fernet(key)
    token = f.encrypt(str.encode(messege))
    return token


def main():
    print("hi from sender")
    messegeSenderArray = []
    X = "messages" + sys.argv[1] + ".txt"
    ips=open("ips.txt","r")
    ipPorts=[]
    for line in ips.readlines():
        ipPorts.append(line)
    ips.close()
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
        messegeSenderArray.append(messegeSender(message, path, round, password, salt, dest_ip, dest_port))
        x = 2
    messges.close()
    messegeSenderArray.sort(key=lambda x: x.round,reverse=False)
    cntr=0
    for messegeToSend in messegeSenderArray:
        c = Enc(messegeToSend.salt, messegeToSend.password, messegeToSend.message)
        msg = socket.inet_aton(messegeToSend.dest_ip) + socket.inet_aton(messegeToSend.dest_port) + c
        l=None
        for path in messegeToSend.path.split(","):
            with open("pk" + path + ".pem", "rb") as key_file:
                public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
            if l==None:
                l = public_key.encrypt(msg, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                             algorithm=hashes.SHA256(), label=None))
            else:
                ipTargetMixServer = ipPorts[cntr].split()[0]
                portTargetMixServer = ipPorts[cntr].split()[1]
                if path=="1":
                    break
                cntr=cntr+1
                msg = socket.inet_aton(ipTargetMixServer) + socket.inet_aton(portTargetMixServer) + l
                l = public_key.encrypt(msg, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                             algorithm=hashes.SHA256(), label=None))

        s = socket.socket()  # Create a socket object
        s.connect((ipTargetMixServer, int(portTargetMixServer)))
        s.sendall(l)
        s.close()  # Close the socket when done
        print(msg)
        print(l)


if __name__ == '__main__':
    main()
