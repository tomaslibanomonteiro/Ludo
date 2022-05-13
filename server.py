# Python program to implement server side of chat room.
import socket
import sys
'''Replace "thread" with "_thread" for python 3'''
from _thread import *

DEFAULT_IP_ADDRESS = "192.168.1.252"
DEFAULT_PORT_NUMBER = 8081
GAME_PASS = "1234"

class Player:
    def __init__(self, type, colour, name, conn):
        self.type = type
        self.colour = colour
        self.name = name
        self.conn = conn

#global variable with the list of players
Players = []
n_connected_players = 0
n_human_players = 0

def MakeGameConn(server):
    conn, addr = server.accept()
    msg = conn.recv(2048).decode()
    if msg != GAME_PASS:
        print('Intruder tried to connect before the game.')
        exit()
    return conn

def makeServer():
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
    server.listen(5)
    
    return server

def PlayerThread(conn, player):

    # sends a message to the client whose user object is conn
    conn.send('Welcome to this chatroom!'.encode())

    while True:
            try:
                message = conn.recv(2048).decode()
                if message:

                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    print("< Player ", player ,"> " + message)

                    # Calls broadcast function to send message to all
                    message_to_send = "< Player " + str(player) + "> " + message
                    broadcast(message_to_send, conn)

                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    print('a player exited the game')
                    exit()

            except:
                continue

# broadcast message sent by connection to the other clients
def broadcast(message, connection):
    for player in Players:
        if player.conn != connection:
            try:
                player.conn.send(message.encode())
            except:
                player.conn.close()
                print('a player exited the game')
                exit()

def SendRecv(send_msg, conn):
    msg_encoded = send_msg
    msg_encoded = msg_encoded.encode()
    conn.send(msg_encoded)
    msg = conn.recv(2048).decode()
    if not msg:
        print('a player exited the game')
        exit()
    return msg

def GetGameInfo(server):
    conn, addr = server.accept()
    # sends a message to the client whose user object is conn
    conn.send("\nWelcome to the Ludo Game! You are Player 1, the game Master.".encode())
    n_players = 0
    while n_players not in (2,3,4):
        msg_received = SendRecv("How many players in this game? (2-4)", conn)
        n_players = int(msg_received)

    n_human_players = 0
    while n_human_players not in range(1,n_players):
        msg_received = SendRecv("How many human players in this game? (1-",n_players,")", conn)
        n_human_players = int(msg_received)

    msg_received = SendRecv("Your name?", conn)
    name = msg_received

    colour = -1
    for i in range(n_players):
        while colour not in range(4):
            msg_received = SendRecv("How many human players in this game? (1-",n_players,")", conn)
            n_human_players = int(msg_received)
        if i < n_human_players:
            this_player = Player('human', colour, name, conn)
        Players.append()

def main():

    server = makeServer()

    GameConn = 0
    while not GameConn:
        GameConn = MakeGameConn(server)

    #connect to first player and get game info
    n_connected_players = 1
    conn = GetGameInfo()

    #start first player thread
    start_new_thread(PlayerThread,(conn,n_connected_players))	

    #receive and start other players threads
    while (n_human_players > n_connected_players):
        conn, addr = server.accept()
        n_connected_players+=1 
        start_new_thread(PlayerThread,(conn,n_connected_players))	
           
    input()

    while True:
        conn, addr = server.accept()

        """Maintains a list of clients for ease of broadcasting
        a message to all available people in the chatroom"""

        # prints the address of the user that just connected
        print(addr)
        #print(addr[0] + "/" + addr[1] + " connected" )

        # creates and individual thread for every user
        # that connects
        #start_new_thread(FirstClientThread,(conn,player))	

    conn.close()
    server.close()

main()
