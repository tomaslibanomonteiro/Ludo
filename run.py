#!/usr/bin/env python3

from ludo.cli import CLIGame
import socket
import sys
'''Replace "thread" with "_thread" for python 3'''
from _thread import *

DEFAULT_IP_ADDRESS = "192.168.1.252"
DEFAULT_PORT_NUMBER = 8081

def makeServer(listen):
    """The first argument AF_INET is the address domain of the
    socket. This is used when we have an Internet Domain with
    any two hosts The second argument is the type of socket.
    SOCK_STREAM means that data or characters are read in
    a continuous flow."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3:
        print("Going to defaults: IP address -> " + DEFAULT_IP_ADDRESS + ", port number -> " + str(DEFAULT_PORT_NUMBER))
        print("If you want other options, run: script, IP address, port number")
        IP_address = DEFAULT_IP_ADDRESS
        Port = DEFAULT_PORT_NUMBER
    else:
        # takes the first argument from command prompt as IP address and second as Port Number
        IP_address = str(sys.argv[1])
        Port = int(sys.argv[2])

    #binds the server to an entered IP address and at the specified port number. client must be aware of these parameters
    server.bind((IP_address, Port))

    #listens for 100 active connections. This number can be increased as per convenience.
    server.listen(listen)
    
    return server

def main():

    server = makeServer(5)

    #connect with player 1
    master_conn, addr = server.accept()
    print('Master Player Connected')

    CLIGame().start(master_conn, server)

main()
