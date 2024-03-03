import socket
import threading
import sys
from datetime import datetime
import pickle
import json


# function to receive data
def receive_data(s, address):
    
    # message from server
    if address[1] == 11112:
        # load data
        received_msg = pickle.loads(s.recv(1024))
        # send ack
        s.sendall("ack".encode())
        # update group members
        handle_groups(received_msg[0], received_msg[1])
    
    else:
        # receive message
        received_msg = s.recv(1024).decode()
        # send ack
        s.sendall("ack".encode())
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        socket_name = s.getsockname()[0]
        
        # if message is quit, close the connection
        if (received_msg.lower() == "quit"):
            print(f"{time} {socket_name} left from the chat.")
           
            
        else:
            print(f"{time} {socket_name} : {received_msg}")
            
    



# function to send messages
def send_message(s, sender_ip, message):
    
    # encode message taken from the input
    msg_to_send = message.encode('utf-8')

    # show sent message to sender terminal as well
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{time} {sender_ip} : {message}")    
    s.sendall(msg_to_send)

    


# function to handle coming connections
def handle_connections(s):
    
    while True:
        # coming connection
        coming_socket, coming_address = s.accept()
        print(f"Connection from: {coming_address}")
    
        # Start a thread to handle the incoming connection
        receive_thread = threading.Thread(target=receive_data, args=([coming_socket, coming_address]))
        receive_thread.start()




# handle groups
def handle_groups (group_name, member_info):

    # create file name based on ip and port
    file_name = own_ip + str(own_port) + ".txt"
    
    # read group information from file or create file if it does not exists
    with open(file_name, "a+") as group_information: 
        data = group_information.read() 
    
    # reconstructing the data as a dictionary 
    # if file already has info    
    if data != "":    
        groups = json.loads(data)
    # create dictionary if file is empty
    else:
        groups = {}

    # check if group already exists
    if group_name in groups:
        # update group members
        groups[group_name] = member_info
     
    # if the group not exists, create group and add members to group
    else:
        groups[group_name] = member_info

    # update group information to the file
    with open(file_name, 'w') as convert_file: 
        convert_file.write(json.dumps(groups))

    


# function to handle connection to the server
        
def handle_server_connection():

    # create socket for server connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind socket to certain ip + port
    server_socket.bind((own_ip, own_port+2))
    # connect to the server
    server_socket.connect(('127.0.0.1', 11111))
    # enter join / leave message
    message = input("Enter message: ")
    # encode message
    msg_to_send = message.encode('utf-8')
    # send message to the server
    server_socket.sendall(msg_to_send)
    # receive group info from the server
    from_server = pickle.loads(server_socket.recv(1024))
    server_socket.sendall("ack".encode())
    # print group info
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{time} : {from_server}") 

    # group name
    message.replace(" ", "")
    group_to_join = message.replace("/join","")

    # update group information
    handle_groups(group_to_join, from_server)


    



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

    while True:
        
        select = input("Join/leave group, select 1 \n send message, select 2 \n -> ")
        
        # handle group joining / leaving
        
        if (select == "1"):
            print("selected 1")
            handle_server_connection()
        
        
        # handle message sending to other peers

        if (select == "2"):
            
            peer_address = "127.0.0.1" #input("Enter IP address of the friend: ")
  
            #peer_port = int(input("Enter port of the friend: "))
            num_of_ports = int(input("Enter number of ports: "))
            ports = list(map(int, input("\nEnter the ports : ").strip().split()))[:num_of_ports]
            message = input("Enter message: ")
            # Connect to the other peer
            print("Connection establishment started...")
            
            for i in range(len(ports)):
                
                try:
                    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    peer_socket.bind((own_ip, own_port+1))
                    peer_socket.connect((peer_address, ports[i]))
                    send_message(peer_socket,own_ip,message)
                    
                
                except ConnectionRefusedError:
                    print(f" Port {ports[i]} not available.")
                    continue
