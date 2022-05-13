# Python program to implement client side of chat room.
import socket
import select
import sys

#wifi from home
#DEFAULT_IP_ADDRESS = "192.168.1.252"

#hotspot Ricardo ifconfig -a
DEFAULT_IP_ADDRESS = "192.168.43.73"
DEFAULT_PORT_NUMBER = 8081

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
