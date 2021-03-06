# Python program to implement client side of chat room.
import socket
import select
import sys
import time
from SetIPandPort.setIPandPort import setIPandPort

SLEEP_TIME = 0.01 #seconds to wait until recv

GAME_PASS = "pass"
ADD_PLAYER = "0"
START_GAME_NOW = "1"

COLOUR = "0"

MASTER_NAME = 'MASTER'

PC_TYPE = "0"
HUMAN_TYPE = "1"

#create game with 4 players, 3 human 1 pc
MESSAGE_LIST1 = [GAME_PASS, MASTER_NAME, COLOUR, 
                        HUMAN_TYPE, COLOUR,
                        ADD_PLAYER, PC_TYPE,
                        ADD_PLAYER, HUMAN_TYPE]

#create game with 3 players, 1 human 2 pc
MESSAGE_LIST2 =  [GAME_PASS, MASTER_NAME, COLOUR, 
                        PC_TYPE,
                        ADD_PLAYER, PC_TYPE,
                        START_GAME_NOW]      

#create game with 2 players, 1 human 1 pc
MESSAGE_LIST3 =  [GAME_PASS, MASTER_NAME, COLOUR, 
                        PC_TYPE,
                        START_GAME_NOW]
                              

#create game with 3 players, 1 human 2 pc and play it until the end
MESSAGE_LIST_LONG = MESSAGE_LIST3
for i in range(100):
    MESSAGE_LIST3.append("\n")
    MESSAGE_LIST3.append("1")

#set which of the above message lists will be sent
MESSAGE_LIST = MESSAGE_LIST_LONG

def myrecv(server):
    time.sleep(SLEEP_TIME)
    try:
        msg = server.recv(10000).decode()
        if not msg:
            print("server disconnected")
            exit()
    except:
        #print("server disconnected")
        exit()
    print(msg)

def mysend(server, msg):
    print("<You>"+msg)
    if msg != '\n':
        msg = msg + '\n'
    msg = msg.encode()
    check = server.send(msg)
    if check == 0:
        print("server disconnected")
        exit()

def main():

    DEFAULT_IP_ADDRESS, DEFAULT_PORT_NUMBER = setIPandPort()

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
                message = socks.recv(10000).decode()
                if not message:
                    print("server disconnected")
                    exit()
                else:
                    print (message)
                    sys.stdin.flush()
            else:
                message = sys.stdin.readline()
                server.send(message.encode())
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()
    server.close()

main()
