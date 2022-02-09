# File: server.py
# Author: John Choi choi.1655@osu.edu
# Version: Feb 9th 2022
# CSE3461 Lab 1

# import socket module
from socket import *
import atexit  # to close the server socket before terminating

def get_header():
    return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

def get_404():
    return """
    <html>
  <body>
    404 Not Found
  </body>
</html>
"""

def exiting(serverSocket):
    print('Closing server socket')
    serverSocket.close()  # close the server socket before terminating server


serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a server socket
#Fill in start
HOST = '127.0.0.1'
PORT = 65432
serverSocket.bind((HOST, PORT))
serverSocket.listen()

atexit.register(exiting, serverSocket)
#Fill in end
while True:
    #Establish the connection
    print('Ready to serve...')
    #Fill in start
    connectionSocket, addr = serverSocket.accept()
    #Fill in end
    try:
        #Fill in start
        message = connectionSocket.recv(1024)
        #Fill in end
        filename = message.split()[1]
        f = open(filename[1:])
        #Fill in start
        outputdata = [f.read()]
        print(outputdata)
        #Fill in end
        #Send one HTTP header line into socket
        #Fill in start
        outputdata.insert(0, get_header())
        #Fill in end
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError as e:
        print(e)
        #Send response message for file not found
        #Fill in start
        connectionSocket.send(f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n{get_404()}'.encode())
        #Fill in end
        #Close client socket
        #Fill in start
        connectionSocket.close()
        #Fill in end
