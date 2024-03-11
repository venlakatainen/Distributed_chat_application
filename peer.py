import socket
import threading
import sys
from datetime import datetime
import pickle
import json
import os
import logging


# function to receive data
def receive_data(s, address):
    
    # message from server
    if address[1] == 11112:
        logging.info("data coming from the server")
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

        print(f"{time} {socket_name} : {received_msg}")
            
    



# function to send messages
def send_message(s, message):
    
    # encode message taken from the input
    msg_to_send = message.encode('utf-8')

    s.sendall(msg_to_send)

    


# function to handle coming connections
def handle_connections(s):
    
    while True:
        # coming connection
        coming_socket, coming_address = s.accept()
        logging.info(f"Connection from: {coming_address}")
        #print(f"Connection from: {coming_address}")
    
        # Start a thread to handle the incoming connection
        receive_thread = threading.Thread(target=receive_data, args=([coming_socket, coming_address]))
        receive_thread.start()



# handle groups
def handle_groups (group_name, member_info):

    # read group information from file or create file if it does not exists
    with open(file_name) as group_file:
        data = json.load(group_file)

    groups = data
    
    # check if group already exists
    if group_name in groups.keys():
        logging.info("found group from file")
        groups[group_name] = member_info
     
    # if the group not exists, create group and add members to group
    else:
        groups[group_name] = member_info

    # update group information to the file
    group_file = open(file_name, "w")
    data = json.dump(groups, group_file)
    group_file.close()
    
    logging.info("group handling done")

    


# function to handle connection to the server
        
def handle_server_connection():

    # create socket for server connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind socket to certain ip + port
    server_socket.bind((own_ip, own_port+2))
    # connect to the server
    try:
        server_socket.connect(('127.0.0.1', 11111))
    
    except ConnectionRefusedError:
        print("Server currently not available")
        logging.info("server not available because of ConnectionRefusedError")
        return 
    except OSError:
        print("Server currently not available")
        logging.info("server not available because of OSError")
        server_socket.close()
        return
    
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
    #print(f"{time} : {from_server}") 

    # group name
    if "/join" in message:
        message = message.replace(" ", "")
        group_to_join = message.replace("/join","")

        if from_server == "already in group":
            print(f"You are already in group {group_to_join}")
        
        else:    
            # update group information
            handle_groups(group_to_join, from_server)
            print(f"You have joined group {group_to_join}")

    elif "/leave" in message:
        if "/leavingdone" == from_server:
            message = message.replace(" ", "")
            group_to_leave = message.replace("/leave","")
            
            if leave_from_group(group_to_leave) == False:
                logging.info("Leaving not successful")
                print("Leaving not succeded")
            else:    
                print(f"You left from group {group_to_leave}")
                logging.info("Leaving done")
        
        else:
            print(from_server)




def leave_from_group (group_name):

    # read group information from file
    with open(file_name) as group_file:
        data = json.load(group_file)

    groups = data

    # check if group exists
    if group_name in groups.keys():
       groups.pop(group_name)
     
    else:
        logging.info("pop false")
        return False

    
    # update group information to the file
    group_file = open(file_name, "w")
    data = json.dump(groups, group_file)
    group_file.close()
    
    

# create sockets for group message    
def sockets_for_group_members(mem_of_group, msg):
    
    # create sockets for all group members
    for i in range(len(mem_of_group)):
        peer_address = mem_of_group[i][0]
        peer_port = int(mem_of_group[i][1])
        print(peer_port)
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            peer_socket.bind((own_ip, own_port-2))
            peer_socket.connect((peer_address,peer_port))
            send_message(peer_socket, msg)
            
        except ConnectionRefusedError:
            print(f"{mem_of_group[i]} not available.")
            continue

        
    logging.info("group info sent")
    
    



if __name__ == '__main__':
    
    print("#####################################")
    print("#           WELCOME!                #")
    print("#####################################")

    

    own_ip = input("Enter your own IP: ")
    own_port = int(input("Enter your port: "))
    
    # create filename to save group information
    file_name = own_ip + str(own_port) + ".txt"

    log_file = "info" + own_ip + str(own_port) + ".log"
    logging.basicConfig(filename=log_file,level=logging.INFO)
    logging.basicConfig(filemode='w')

    if os.path.exists(file_name) == False:
        group_file = open(file_name, "x")
        group_file.close()

    if os.stat(file_name).st_size == 0:
        groups = {}

        group_file = open(file_name, "w")
        json.dump(groups, group_file)
        group_file.close()


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
        
        select = input("Join/leave group, select 1 \n send group message, select 2 \n Send private message, select 3 \n Quit, select 4 \n-> ")
        
        # handle group joining / leaving
        
        if (select == "1"):
            print("selected 1")
            handle_server_connection()
        
        
        # group message
        if (select == "2"):
            
            group_to_send_message = input("Enter group name: ")
            message = input("Enter message: ")

            with open(file_name) as group_file:
                data = json.load(group_file)

            groups = data

            if group_to_send_message in groups.keys():
                members = groups[group_to_send_message]
                sockets_for_group_members(members, message)
            
            else:
                print("Group not found")

        # private message
        if (select == "3"):

            peer_address = input("Enter IP address of the friend: ")
            peer_port = int(input("Enter port of the friend: "))
            message = input("Enter message: ")

            try:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.bind((own_ip, own_port-1))
                peer_socket.connect((peer_address, peer_port))
                send_message(peer_socket,message)
                
                
            except ConnectionRefusedError:
                print(f" Port {peer_port} not available.")
                continue
        
        if (select == "4"):
            os._exit(0)