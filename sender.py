# nizan mandelblit, 313485468, eldad horvitz, 314964438
import socket, sys
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import threading


class messegeSender:
    def __init__(self, message, path, round, password, salt, dest_ip, dest_port):
        self.message = message
        self.path = path
        self.round = round
        self.password = password
        self.salt = salt
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.l = None

# sendToMix server
def sendToMix(l, ipTargetMixServer, portTargetMixServer):
    s = socket.socket()  # Create a socket object
    s.connect((ipTargetMixServer, int(portTargetMixServer)))
    s.sendall(l)
    s.close()  # Close the socket when done

# symmetric encryption function
def Enc(salt, password, messege):
    password = str.encode(password)
    salt = str.encode(salt)
    kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 100000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    token = f.encrypt(str.encode(messege))
    return token


def main():
    timer=[]
    messegeSenderArray = []
    X = "messages" + sys.argv[1] + ".txt"
    ips = open("ips.txt", "r")
    ipPorts = []
    # get lines from ips.txt
    for line in ips.readlines():
        ipPorts.append(line)
    ips.close()
    messges = open(X, "r")
    # get lines from messages.txt and create messegeSender
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
    for messegeToSend in messegeSenderArray:
        # encrypt message
        c = Enc(messegeToSend.salt, messegeToSend.password, messegeToSend.message)

        msg = socket.inet_aton(messegeToSend.dest_ip) + int(messegeToSend.dest_port).to_bytes(2, 'big') + c
        servers = messegeToSend.path.split(",")
        servers.reverse()
        for i in range(len(servers)):
            # create the key
            with open("pk" + servers[i] + ".pem", "rb") as key_file:
                public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
                # encryption
                l = public_key.encrypt(msg, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                         algorithm=hashes.SHA256(), label=None))
                address = ipPorts[int(servers[i])-1].split()
                ipTargetMixServer = address[0]
                portTargetMixServer = address[1]
                # concat the ip and address
                msg = socket.inet_aton(ipTargetMixServer) + int(portTargetMixServer).to_bytes(2, 'big') + l
        timer.append(threading.Timer(int(messegeToSend.round) * 60,
                               sendToMix, args=[l, ipTargetMixServer, portTargetMixServer]))
    # start timers
    for t in timer:
        t.start()


if __name__ == '__main__':
    main()
