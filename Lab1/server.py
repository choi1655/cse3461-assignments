# File: server.py
# Author: John Choi choi.1655@osu.edu
# Version: Feb 7th 2022
# CSE3461 Lab 1

# import socket module 
from socket import * 
import sys # In order to terminate the program 
 
serverSocket = socket(AF_INET, SOCK_STREAM) 
#Prepare a server socket 
#Fill in start
#Fill in end 
while True: 
    #Establish the connection 
    print('Ready to serve...') 
    connectionSocket, addr =  None, None #Fill in start              #Fill in end           
    try: 
        message =  None #Fill in start          #Fill in end                
        filename = message.split()[1]                  
        f = open(filename[1:])                         
        outputdata = None #Fill in start       #Fill in end                    
        #Send one HTTP header line into socket 
        #Fill in start 
        #Fill in end                 
        #Send the content of the requested file to the client 
        for i in range(0, len(outputdata)):            
            connectionSocket.send(outputdata[i].encode()) 
        connectionSocket.send("\r\n".encode()) 
         
        connectionSocket.close() 
    except IOError:
        break
        #Send response message for file not found 
        #Fill in start         
        #Fill in end 
        #Close client socket 
        #Fill in start 
        #Fill in end             

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data