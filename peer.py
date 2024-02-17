import socket
import threading
import sys


# function to receive data
def receive_data(s):
    #while True:
    # receive message
    received_msg = s.recv(1024).decode()
    # if message is quite, close the connection
    if (received_msg.lower() == "quit"):
        print(s.getsockname()[0], "left from the chat.")
        s.close()
        
    # print message and address who send the message
    #if received_msg == "":
        
    print(s.getsockname()[0], ": ", received_msg)
    s.close()

# function to send (private) messages
def send_message(s):
    #while True:
    # encode message taken from the input
    message = input("Enter message: ")
    msg_to_send = message.encode('utf-8')
    # send message
    s.sendall(msg_to_send)
    if message.lower() == "quit":
        s.close()
        
    s.close()

# function to handle coming connections
def handle_connections(s):
    while True:
        coming_socket, coming_address = s.accept()
        print("Connection from: ", coming_address)
        
        # Start a thread to handle the incoming connection
        receive_thread = threading.Thread(target=receive_data, args=([coming_socket]))
        receive_thread.start()


# function to handle connection to the server
def handle_server_connection(s):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('127.0.0.1', 11111))
    server_socket.send("I am CLIENT\n".encode())
    from_server = server_socket.recv(1024).decode()
    print(from_server)



# function to send group messages
def send_group_message(group_members):    
    
    group_msg = input("Enter the message")

    for i in range(len(group_members)):
        member_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        member_socket.connect(group_members[i])

        msg_to_send = group_msg.encode('utf-8')
        # send message
        member_socket.sendall(msg_to_send)
        if group_msg.lower() == "quit":
            member_socket.close()
            break
        

    


if __name__ == '__main__':
    
    print("#####################################")
    print("#           WELCOME!                #")
    print("#####################################")

    own_ip = "127.0.0.1" #input("Enter your own IP: ")
    own_port = int(sys.argv[1]) #int(input("Enter your port: "))

    # create socket
    me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set IP address and port to the socket
    me.bind((own_ip, own_port))
    # listen connections from other peers
    me.listen(5)

    print("Peer listening on {}:{}\n\n".format(own_ip, own_port))

    # start thread to handle incoming connections
    connection_handle_thread = threading.Thread(target=handle_connections, args=([me]))
    connection_handle_thread.start()

    # start thread to handle connection to the server
    #server_thread = threading.Thread(target=handle_server_connection, args=([me]))
    #server_thread.start()

    # selection to group or private message
    #select = input("If you want to send group message - write 1 \n If you want to send private message - write 2")
    """
    if select == "1":
        friends = []
        print("Group message selected.")
        while True:
            print("Enter all the IPs of the friends and ports one by one")
            print("Write D when all the friends are added")
            group_peer_address = input("Enter IP address of the friend: ")
            
            if group_peer_address.upper() == "D":
                break
            
            group_peer_port = int(input("Enter port of the friend: "))

            # add IP and port to the friends
            friends.append((group_peer_address, group_peer_port))

        print("Group formed.")
        # send group message
        send_group_message(friends)

    """
    #if select == "2":
    print("Private message selected. ")
    # handle private message transmission
    # Connect to another peer
    peer_address = "127.0.0.1" #input("Enter IP address of the friend: ")
    
    while True:
        peer_port = int(input("Enter port of the friend: "))
        # Connect to the other peer
        print("Connection establishment started...")
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_address, peer_port))
        print("Connected to: ", peer_address)

        # create thread to send messages
        send_message(peer_socket)
        #send_message_thread = threading.Thread(target = send_message, args = ([peer_socket]))
        # start thread
        #send_message_thread.start()

    
