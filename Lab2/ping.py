"""File: ping.py
Author: John Choi choi.1655@osu.edu
Version: March 13, 2022

The Ohio State University CSE3461 Programming Lab 2.
"""
from socket import *
import os
import sys
import struct
import time
import select
import atexit

ICMP_ECHO_REQUEST = 8

def checksum(str):
    csum = 0
    countTo = (len(str) / 2) * 2

    count = 0
    while count < countTo:
        # thisVal = ord(str[count+1]) * 256 + ord(str[count])
        thisVal = str[count+1] * 256 + str[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(str):
        csum = csum + ord(str[len(str) - 1])
        csum = csum + str[len(str) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        #Fill in start
        # print(recPacket)
        # print(addr)

        #Fetch the ICMP header from the IP packet
        # ICMP header starts after bit 160 bits for 32 bit
        # one index represents one byte in recPacket

        starting_idx = 160 // 8
        ending_idx = (160 + 32 + 32) // 8

        raw_data = struct.unpack('bbHHh', recPacket[starting_idx: ending_idx])

        type_val = raw_data[0]
        code_val = raw_data[1]
        checksum_val = raw_data[2]
        id_val = raw_data[3]
        sequence_val = raw_data[4]

        # print(f'{type_val= }')
        # print(f'{code_val= }')
        # print(f'{checksum_val= }')
        # print(f'{id_val= }')
        # print(f'{sequence_val= }')


        #Fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return None
        else:
            timeLeft *= 1000 # convert from second to ms
            return f"{type_val=}, {code_val=}, {checksum_val=}, {id_val=}, {sequence_val=}, time={str(round(timeLeft, 3))}ms"

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
        #Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    #Both LISTS and TUPLES consist of a number of objects
    #which can be referenced by their position number within the object

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw

    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    # Send ping requests to a server separated by approximately one second
    counter = 0
    success = 0

    atexit.register(print_statistics, host, counter, success)
    while 1 :
        delay = doOnePing(dest, timeout)
        if delay is None:
            print('Request timed out.')
        else:
            print(f'Received from {dest}: icmp_seq={counter + 1}, {delay}')
            success += 1
            atexit.unregister(print_statistics)
            atexit.register(print_statistics, host, counter, success)
        time.sleep(1)# one second
        counter += 1
        atexit.unregister(print_statistics)
        atexit.register(print_statistics, host, counter, success)
    return delay

def print_statistics(destination, num_packets, received):
    num_packets += 1
    percentage = 100 - (received / num_packets * 100)
    print()
    print(f'--------- {destination} ping statistics ---------')
    print(f'{num_packets} packets transmitted, {received} packets received, {str(round(percentage, 1))}% packet loss')

ping("google.com")
