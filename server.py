import socket
import threading
import json 
from datetime import datetime
import pickle

groups = {}


# function receive data from the client socket
def receive_data(conn, address):

    # receive message
    
    received_msg = conn.recv(1024).decode()

    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if received_msg != "":
        # print message and address who send the message
        print(f"{time} {address} : {received_msg}")


    # if message contains /join, the peer wants to join group
    if "/join" in received_msg:
        received_msg.replace(" ", "")
        group_to_join = received_msg.replace("/join","")
        # add peer to the group
        group_info = join_group(group_to_join, address[0], str(int(address[1])-2))
        print(group_info)
        data=pickle.dumps(group_info)
        # send group members back to the peer
        conn.sendall(data)
        update_group_members(group_to_join, group_info)
            
    

# function to handle joining groups -> add peer to the group  
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

    # update group information to the file
    with open('groups_server.txt', 'w') as convert_file: 
        convert_file.write(json.dumps(groups))

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
        print(peer_port)
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            peer_socket.bind((server_ip, server_port+1))
            peer_socket.connect((peer_address,peer_port))
            send_message(name_of_the_group, mem_of_group, peer_socket)
            
        except ConnectionRefusedError:
            print(f"{mem_of_group[i]} not available.")
            continue

        
    print("group info sent")



# send message to group 
def send_message(group_name, group_members, group_member_socket):
    
    
    message = (group_name, group_members)
    data=pickle.dumps(message)
    print(data)
    # encode message taken from the input
    #msg_to_send = message.encode('utf-8')

    # send data to sockets 
    group_member_socket.sendall(data)
   
       
        

if __name__ == '__main__':
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set IP address and port to the socket
    server_ip = '127.0.0.1'
    server_port = 11111
    s.bind((server_ip, server_port))
    # listen connections from clients
    s.listen(5)

    while True:
        coming_socket, coming_address = s.accept()
        print("Connection from: ", coming_address)

        # handle coming client connections
        coming_connection = threading.Thread(target=receive_data, args=([coming_socket, coming_address]))
        coming_connection.start()

    
    
