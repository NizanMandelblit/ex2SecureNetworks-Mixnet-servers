# nizan mandelblit, 313485468, fullname 2, id 2
import socket, os, datetime, random, sys
import hashlib





def main():
    print("hi from mix")
    Y = "sk" + sys.argv[1] + ".pem"
    port= sys.argv[2]

    skfile = open(Y, "r")
    skfile.close()

    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen()  # Now wait for client connection.
    while True:
        c, addr = s.accept()  # Establish connection with client.
        print('Got connection from', addr)
        print(c.recv(1024))
        c.close()  # Close the connection

if __name__ == '__main__':
    main()
