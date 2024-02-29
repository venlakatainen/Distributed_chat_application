import socket
import threading
import sys
from datetime import datetime
import pickle


# function to receive data
def receive_data(s):
    #while True:
    # receive message
    received_msg = s.recv(1024).decode()
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    socket_name = s.getsockname()[0]
    
    # if message is quit, close the connection
    if (received_msg.lower() == "quit"):
        print(f"{time} {socket_name} left from the chat.")
        s.close()
        
    # print message and address who send the message
    #if received_msg == "":
    else:
        print(f"{time} {socket_name} : {received_msg}")    
        #print(s.getsockname()[0], ": ", received_msg)
        s.close()



# function to send messages
def send_message(s, sender_ip):
    #while True:
    # encode message taken from the input
    message = input("Enter message: ")
    msg_to_send = message.encode('utf-8')

    # show sent message to sender terminal as well
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{time} {sender_ip} : {message}")    

    for i in range(len(s)):
        # send message
        s[i].sendall(msg_to_send)
        if message.lower() == "quit":
            print(f"{time} {sender_ip} left from the chat.")
            s[i].close()
            
        s[i].close()



# function to handle coming connections
def handle_connections(s):
    
    while True:
        coming_socket, coming_address = s.accept()
        print(f"Connection from: {coming_address}")
        
        # Start a thread to handle the incoming connection
        receive_thread = threading.Thread(target=receive_data, args=([coming_socket]))
        receive_thread.start()


# function to handle connection to the server
def handle_server_connection(s):
    #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 11111))
    #while True:
    message = input("Enter message: ")
    msg_to_send = message.encode('utf-8')

    s.send(msg_to_send)
        
        #listen_server_thread = threading.Thread(target=handle_connections, args=([s]))
        #listen_server_thread.start()
            #server_socket.send("I am CLIENT\n".encode())
    from_server = pickle.loads(s.recv(1024))
    print(from_server)




# function to send group messages
"""
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
        
"""
    


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
    #me.listen(5)

    print("Peer listening on {}:{}\n\n".format(own_ip, own_port))

    # start thread to handle incoming connections
    #connection_handle_thread = threading.Thread(target=handle_connections, args=([me]))
    #connection_handle_thread.start()

    # start thread to handle connection to the server
    
    server_thread = threading.Thread(target=handle_server_connection, args=([me]))
    server_thread.start()
    

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
    #print("Private message selected. ")
    # handle private message transmission
    # Connect to another peer
    
    ######################## WORKING PART BELOW ######################################################
    """
    peer_address = "127.0.0.1" #input("Enter IP address of the friend: ")
    
    while True:
        #peer_port = int(input("Enter port of the friend: "))
        num_of_ports = int(input("Enter number of ports: "))
        ports = list(map(int, input("\nEnter the ports : ").strip().split()))[:num_of_ports]
        # Connect to the other peer
        print("Connection establishment started...")
        sockets = []
        for i in range(len(ports)):
            try:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.connect((peer_address, ports[i]))
            except ConnectionRefusedError:
                print(f" Port {ports[i]} not available.")
                continue

            sockets.append(peer_socket)
        
        print("Connected to: ", sockets)

        # create thread to send messages
        if len(sockets) > 0:
            send_message(sockets, own_ip)
        
        else:
            print("No available sockets added, message cannot be sent.")
        #send_message_thread = threading.Thread(target = send_message, args = ([peer_socket]))
        # start thread
        #send_message_thread.start()

    """
