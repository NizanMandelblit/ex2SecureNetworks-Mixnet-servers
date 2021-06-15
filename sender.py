# nizan mandelblit, 313485468, fullname 2, id 2
import socket, os, datetime, random, sys
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
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


def Enc(salt,password,messege):
    password = str.encode(password)
    salt = str.encode(salt)
    kdf = PBKDF2HMAC(hashes.SHA256(),32,salt,100000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    token = f.encrypt(str.encode(messege))
    print(token)
    print(f.decrypt(token))
    return token



def main():
    print("hi from sender")
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
        c=Enc(messegeToSend.salt,messegeToSend.password,messegeToSend.message)
        msg=str.encode(messegeToSend.dest_ip) + str.encode(messegeToSend.dest_port) + c
        print(msg)



if __name__ == '__main__':
    main()
