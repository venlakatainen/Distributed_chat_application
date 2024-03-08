import socket
import threading
import json 
from datetime import datetime
import pickle
import os
import logging




# function receive data from the client socket
def receive_data(conn, address):

    # receive message
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        received_msg = conn.recv(1024).decode()

    except ConnectionResetError:
        # if peer close the connection
        logging.info(f"{time} Peer closed the connection")
        return
    
    
    if received_msg != "":
        # print message and address who send the message
        logging.info(f"{time} {address} : {received_msg}")



    # if message contains /join, the peer wants to join group
    if "/join" in received_msg:
        received_msg = received_msg.replace(" ", "")
        group_to_join = received_msg.replace("/join","")
        # add peer to the group
        group_info = join_group(group_to_join, address[0], str(int(address[1])-2))
        if group_info == False:
            data=pickle.dumps("already in group")
            conn.sendall(data)
            
        else:    
            logging.info(group_info)
            print(group_info)
            data=pickle.dumps(group_info)
            # send group members back to the peer
            conn.sendall(data)
            update_group_members(group_to_join, group_info)
    
    elif "/leave" in received_msg:
        received_msg = received_msg.replace(" ", "")
        group_to_leave = received_msg.replace("/leave","")
        group_info = leave_from_group(group_to_leave, address[0], str(int(address[1])-2))
        
        if group_info == False:
            logging.info("Peer leaving not done")
            data=pickle.dumps("leaving not succesfull")
            conn.sendall(data)
            
        else:
            logging.info("Peer removed from the group")
            # send done mark to the peer
            data=pickle.dumps("/leavingdone")
            conn.sendall(data)
            update_group_members(group_to_leave, group_info)


# function to handle group leaving
def leave_from_group (group_name, socket_ip, socket_port):

    # read group information from file
    with open(server_file) as group_file:
        data = json.load(group_file)

    groups = data
    

    # check if group exists
    if group_name in groups.keys():
        # remove member from group if member in group
        members = groups[group_name]
        if [socket_ip, socket_port] in members:
            members.remove([socket_ip, socket_port])
            groups[group_name] = members
            # remove group if there is no members anymore
            if len(groups[group_name]) == 0:
                groups.pop(group_name)

    else:
        return False

    # update group information to the file
    group_file = open(server_file, "w")
    data = json.dump(groups, group_file)
    group_file.close()
    return members


# function to handle joining groups -> add peer to the group  
def join_group (group_name, socket_ip, socket_port):


    with open(server_file) as group_file:
        data = json.load(group_file)

    groups = data
    
    # check if group already exists
    if group_name in groups.keys():
        members = groups[group_name]
        # check if peer already in group
        print(members)
        if [socket_ip, socket_port] in members:
            return False
        
        else:
            # add the new member to the group
            members.append((socket_ip, socket_port))
            groups[group_name] = members
     
    # if the group not exists, create group and add member to group
    else:
        groups[group_name] = [(socket_ip, socket_port)]

    # update group information to the file

    group_file = open(server_file, "w")
    data = json.dump(groups, group_file)
    group_file.close()
    

    # send group information for the peer that joined and other group members.
    group_members = groups[group_name]
    # return group members of the group that peer wanted to join
    return group_members 
    

# create socket for all group members and send updated group information to the group members
def update_group_members (name_of_the_group, mem_of_group):
    
    # create sockets for all group members
    for i in range(len(mem_of_group)):
        peer_address = mem_of_group[i][0]
        peer_port = int(mem_of_group[i][1])
       
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            peer_socket.bind((server_ip, server_port+1))
            peer_socket.connect((peer_address,peer_port))
            send_message(name_of_the_group, mem_of_group, peer_socket)
            
        except ConnectionRefusedError:
            logging.info(f"{mem_of_group[i]} not available.")
            continue

        
    logging.info("group info sent")



# send message to group 
def send_message(group_name, group_members, group_member_socket):

    message = (group_name, group_members)
    data=pickle.dumps(message)
    logging.info(data)

    # send data to sockets 
    group_member_socket.sendall(data)
   
       
        

if __name__ == '__main__':
    # create socket
    logging.basicConfig(filename='info_server.log',level=logging.INFO)
    logging.basicConfig(filemode='w')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set IP address and port to the socket
    server_ip = '127.0.0.1'
    server_port = 11111
    server_file = 'groups_server.txt'

    print("SERVER STARTED")

    if os.stat(server_file).st_size == 0:
        groups = {}

        group_file = open(server_file, "w")
        json.dump(groups, group_file)
        group_file.close()

    s.bind((server_ip, server_port))
    # listen connections from clients
    s.listen(5)

    while True:
        coming_socket, coming_address = s.accept()
        print("Connection from: ", coming_address)
        logging.info(f"Connection from: {coming_address}")
        # handle coming client connections
        coming_connection = threading.Thread(target=receive_data, args=([coming_socket, coming_address]))
        coming_connection.start()

    
    
