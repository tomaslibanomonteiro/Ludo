# Python program to implement client side of chat room.
import socket
import select
import sys
import time

#wifi from home
#DEFAULT_IP_ADDRESS = "192.168.1.252"

#hotspot Ricardo ifconfig -a
DEFAULT_IP_ADDRESS = "192.168.43.73"

DEFAULT_PORT_NUMBER = 8081
SLEEP_TIME = 0.2 #seconds to wait until recv

START_NEM_GAME = "0"
ADD_PLAYER = "0"
COLOUR = "0"

MASTER_NAME = 'MASTER'
NAME2 = 'HUMAN PLAYER X'
NAME3 = 'HUMAN PLAYER Y'
NAME4 = 'HUMAN PLAYER Z'

PC_TYPE = "0"
HUMAN_TYPE = "1"

#create game with 4 players, 3 human 1 pc
MESSAGE_LIST = [START_NEM_GAME, MASTER_NAME, COLOUR, 
                        HUMAN_TYPE, NAME2, COLOUR,
                        ADD_PLAYER, PC_TYPE,
                        ADD_PLAYER, HUMAN_TYPE, NAME4]
                        
"""
def myrecv(server):
    while True: 
        server.settimeout(2)

        try:
            msg = server.recv(2048).decode()
            if not msg:
                print("server disconnected")
                exit()
        except: 
            print("exception")
            break
    server.clearTimeout()

    return msg
"""
"""
def myrecv(socket):
    start_time = time.time()
    seconds = 2
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        msg = socket.recv(2048).decode()
        if not msg:
            print("server disconnected")
            exit()
        else:
            print(msg)
        if elapsed_time > seconds:
            print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
            break
"""
def myrecv(server):
    time.sleep(SLEEP_TIME)
    msg = server.recv(2048).decode()
    if not msg:
        print("server disconnected")
        exit()
    print(msg)

def mysend(server, msg):
    print("<You>"+msg)
    msg = msg + '\n'
    msg = msg.encode()
    check = server.send(msg)
    if check == 0:
        print("server disconnected")
        exit()

def main():

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

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((IP_address, Port))
    
    for msg in MESSAGE_LIST:
        myrecv(server)
        mysend(server, msg)


    while True:

        # maintains a list of possible input streams
        sockets_list = [sys.stdin, server]

        """ There are two possible input situations. Either the
        user wants to give manual input to send to other people,
        or the server is sending a message to be printed on the
        screen. Select returns from sockets_list, the stream that
        is reader for input. So for example, if the server wants
        to send a message, then the if condition will hold true
        below.If the user wants to send a message, the else
        condition will evaluate as true"""
        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048).decode()
                if not message:
                    print("server disconnected")
                    exit()
                else:
                    print (message)
            else:
                message = sys.stdin.readline()
                server.send(message.encode())
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()
    server.close()

main()
