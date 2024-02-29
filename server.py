import socket
import threading
import json 
from datetime import datetime
import pickle



# function receive data from the client socket
def receive_data(conn, address):
    while True:
        # receive message
        received_msg = conn.recv(1024).decode()
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if received_msg == "":
            continue

        # print message and address who send the message
        print(f"{time} {address[0]} : {received_msg}")

        # if message contains /join, the peer wants to join group
        if "/join" in received_msg:
            received_msg.replace(" ", "")
            group_to_join = received_msg.replace("/join","")
            
            group_info = join_group(group_to_join, address[0], address[1])
            print(group_info)
            data=pickle.dumps(group_info)
            # send group members back to the peer
            conn.send(data)
            
    
    
        
           
    

# function to handle joining groups   
def join_group (group_name, socket_ip, socket_port):

    # read group information from file
    with open('groups_server.txt') as group_file: 
        data = group_file.read() 
    
    # reconstructing the data as a dictionary 
    # if file already has info    
    if data != "":    
        groups = json.loads(data)
    # create dictionary if file is empty
    else:
        groups = {}

    # check if group already exists
    if group_name in groups:
        # add the new member to the group
        members = groups[group_name]
        members.append((socket_ip, socket_port))
        groups[group_name] = members
     
    # if the group not exists, create group and add member to group
    else:
        groups[group_name] = [(socket_ip, socket_port)]

    temp_groups = groups

    # update group information to the file
    with open('groups_server.txt', 'w') as convert_file: 
        convert_file.write(json.dumps(groups))

    # send group information for the peer that joined and other group members.
    group_members = temp_groups[group_name]
    # return group members of the group that peer wanted to join
    return group_members 
    
    
def update_group_members (groups, group_name):
    peers_list = groups[group_name]
    # list for sockets
    sockets = []
    # create sockets for all group members
    for i in range(len(peers_list)):
        peer_address = peers_list[i][0]
        peer_port = peers_list[i][1]
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_address, peer_port))
        except ConnectionRefusedError:
            print(f" Port {peer_port} not available.")
            continue

        sockets.append(peer_socket)
    
    if len(sockets) > 0:
        send_message_to_group(group_name, peers_list, sockets)


# send message to group 
def send_message_to_group (group_name, group_members, group_member_sockets):
    
    # add group name to the first of the member list
    group_members = group_members.insert(0,group_name)
    # pickle to send list 
    data=pickle.dumps(group_members)
    
    # send data to sockets 
    for i in range(len(group_member_sockets)):
        member_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        member_socket.connect(group_member_sockets[i])

        # send message
        member_socket.sendall(data)
       
        


# function to send data 
def send_message(conn):
    while True:
        # take input and enocde
        message_to_send = input().encode()
        # send message
        conn.sendall(message_to_send)



# function to handle coming connections
def handle_connections(socket_connection):
    while True:
        coming_socket, coming_address = socket_connection.accept()
        print("Connection from: ", coming_address)
        
        # Start a thread to handle the incoming connection
        receive_thread = threading.Thread(target=receive_data, args=([coming_socket, coming_address]))
        receive_thread.start()
        
        #send_thread = threading.Thread(target = send_message, args = ([coming_socket]))
        #send_thread.start()

     



if __name__ == '__main__':
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set IP address and port to the socket
    s.bind(('127.0.0.1', 11111))
    # listen connections from clients
    s.listen(4)

    # handle coming client connections
    coming_connection = threading.Thread(target=handle_connections, args=([s]))
    coming_connection.start()
    
