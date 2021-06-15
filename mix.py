# nizan mandelblit, 313485468, eldad horvitz, 314964438
import socket, os, datetime, random, sys
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization




def main():
    print("hi from mix")
    # load sk
    key = "sk" + sys.argv[1] + ".pem"
    skfile = open(key, "rb")
    private_key = serialization.load_pem_private_key(skfile.read(), password=None)
    # get ciphertext
    ciphertext = b"hh"
    # decrypt the ciphertext
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

if __name__ == '__main__':
    main()
