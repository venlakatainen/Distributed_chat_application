import socket
import threading
import json
import os
import logging
from message import Message
from screen import Screen


screen = Screen()

# function to receive data
def receive_data(s: socket.socket, address: str) -> None:
    # message from server
    if address[1] == 11112:
        logging.info("data coming from the server")
        
        # load data
        received_msg = s.recv(1024).decode()
        jsonobj = json.loads(received_msg)
        group_name = jsonobj["group"]
        members = jsonobj["members"]

        # send ack
        s.sendall(json.dumps({"cmd":"ack"}).encode())
        
        if "status" in jsonobj.keys():
            screen.print(Message(jsonobj["message"], "Server"))
            return
        # update group members
        handle_groups(group_name, members)
    else:
        # receive message
        received = s.recv(1024).decode()
        jsonobj = json.loads(received)
        msg = Message.from_json(jsonobj)
        
        # send ack
        s.sendall({"cmd":"ack"}.encode())

        screen.print(msg)
            

# function to send messages
def send_message(s: socket.socket, message: Message) -> None:
    # encode message taken from the input
    msg_to_send = json.dumps(message.get_json()).encode('utf-8')
    s.sendall(msg_to_send)


# function to handle coming connections
def handle_connections(s: socket.socket) -> None:
    while True:
        # coming connection
        coming_socket, coming_address = s.accept()
        logging.info(f"Connection from: {coming_address}")
    
        # Start a thread to handle the incoming connection
        receive_thread = threading.Thread(target=receive_data, args=([coming_socket, coming_address]))
        receive_thread.start()


def handle_groups (group_name: str, member_info: list) -> None:
    # read group information from file or create file if it does not exists
    with open(file_name, "r") as group_file:
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


def get_groups(my_ip, my_port) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind socket to certain ip + port
    server_socket.bind((my_ip, my_port+2))
    try:
        server_socket.connect(('127.0.0.1', 11111))
    except ConnectionRefusedError:
        screen.print(Message("Server currently not available", "System"))
        logging.info("server not available because of ConnectionRefusedError")
        return 
    except OSError:
        screen.print(Message("Server currently not available", "System"))
        logging.info("server not available because of OSError")
        server_socket.close()
        return
    msg_to_send = json.dumps({"cmd":"list"}).encode('utf-8')
    server_socket.sendall(msg_to_send)
    from_server = json.loads(server_socket.recv(1024).decode())
    server_socket.sendall(json.dumps({"cmd":"ack"}).encode())
    with open(file_name, "w") as group_file:
        group_file.write(json.dumps(from_server))

# function to handle connection to the server
def handle_server_connection() -> None:
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
    
    screen.print(Message("Type /join [group], /leave [group] or /list groups", "System"))
    args = input().split()

    msg_json_dict = {}
    #message = input("Enter message: ")
    # encode message
    if (args[0] == "/join" or args[0] == "/leave") and len(args) == 2:
        msg_json_dict["cmd"] = args[0].lstrip("/")
        msg_json_dict["group"] = args[1]
    elif args[0] == "/list" and len(args) == 1:
        msg_json_dict["cmd"] = args[0].lstrip("/")
    else:
        screen.print(Message("Invalid command", "System", group="None"))
        return

    msg_to_send = json.dumps(msg_json_dict).encode('utf-8')
    # send message to the server
    server_socket.sendall(msg_to_send)
    # receive group info from the server
    
    from_server = json.loads(server_socket.recv(1024).decode())
    server_socket.sendall(json.dumps({"cmd":"ack"}).encode())
    # print group info

    # group name
    if args[0] == "/join":
        group_to_join = args[1]
        if from_server["status"] == "failure":
            screen.print(Message(f"You are already in group {group_to_join}", "System"))
        
        else:    
            # update group information
            handle_groups(group_to_join, from_server)
            screen.print(Message(f"You have joined group {group_to_join}", "System"))
    elif args[0] == "/leave":
        if from_server["status"] == "success":
            group_to_leave = args[1]
            
            if leave_from_group(group_to_leave) == False:
                logging.info("Leaving not successful")
                screen.print(Message("Leaving not successful", "System"))
            else:    
                screen.print(Message(f"You left from group {group_to_leave}", "System"))
                logging.info("Leaving done")
        else:
            screen.print(Message("Leaving not successful", "System"))
    elif args[0] == "/list":
        with open(file_name, "w") as group_file:
            group_file.write(json.dumps(from_server))
        screen.print(Message(f"Groups that you are in:", "System"))
        for group in from_server.keys():
            screen.print(Message(f"{group}: {from_server[group]}", "System"))

    else:
        screen.print(Message("Invalid command", "System"))
    

def leave_from_group (group_name) -> bool:
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
def sockets_for_group_members(mem_of_group: list, msg: str) -> None:
    # create sockets for all group members
    for i in range(len(mem_of_group)):
        peer_address = mem_of_group[i][0]
        peer_port = int(mem_of_group[i][1])
        screen.print(peer_port)
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            peer_socket.bind((own_ip, own_port-2))
            peer_socket.connect((peer_address,peer_port))
            send_message(peer_socket, msg)
            
        except ConnectionRefusedError:
            screen.print(Message(f"{mem_of_group[i]} not available.", "System"))
            continue
 
    logging.info("group info sent")
    
    
if __name__ == '__main__':
    while True:
        try:
            #screen.print(Message("Enter your own IP", "System"))
            #own_ip = input()
            own_ip = "127.0.0.1"
            screen.print(Message("Enter your own port", "System"))
            own_port = int(input())
        except ValueError:
            screen.print(Message("Port should be number", "System"))

        # create socket
        try:
            me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # set IP address and port to the socket
            me.bind((own_ip, own_port))
            # listen connections from other peers
            me.listen(5)
            screen.print(Message(f"Peer listening on {own_ip}:{own_port}", "System"))
            break
        except:
            screen.print(Message("Invalid IP or port was given", "System"))
        
    # create needed logs
    # create filename to save group information
    file_name = own_ip + str(own_port) + ".json"
    
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

    try:
        # get group information from the server
        get_groups(own_ip, own_port)
    except:
        screen.print(Message("Group server currently not available", "System"))
        logging.info("group server not available")

    # start thread to handle incoming connections
    connection_handle_thread = threading.Thread(target=handle_connections, args=([me]))
    connection_handle_thread.start()

    while True:
        
        select = input()
        if select == "":
            continue
        args = select.split(" ")
        
        # handle group joining / leaving
        if (args[0] == "/s"):
            screen.print(Message("Group management started.", "System"))
            handle_server_connection()
        
        # group message
        elif (args[0] == "/g"):
            group_to_send_message = args[1]
            #screen.print(Message("Enter group name", "System"))
            #group_to_send_message = input()

            message = " ".join(args[2:])
            #screen.print(Message("Enter message", "System"))
            #message = input()

            with open(file_name) as group_file:
                data = json.load(group_file)

            groups = data
            if group_to_send_message in groups.keys():
                members = groups[group_to_send_message]
                sockets_for_group_members(members, message)  
            else:
                screen.print(Message("Group not found", "System"))

        # private message
        elif (args[0] == "/p"):
            #screen.print(Message("Enter IP address of the friend", "System"))
            #peer_address = input()
            peer_address, peer_port = args[1].split(":")
            peer_port = int(peer_port)

            #try:
            #    screen.print(Message("Enter port of the friend", "System"))
            #    peer_port = int(input())
            #except ValueError:
            #    screen.print(Message("Port should be number", "System"))
            #    continue

            #screen.print(Message("Enter message", "System"))
            #text = input()
            #message = Message(text, f"{own_ip}:{own_port}")

            message = Message(" ".join(args[2:]), f"{own_ip}:{own_port}")

            try:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.bind((own_ip, own_port-1))
                peer_socket.connect((peer_address, peer_port))
                send_message(peer_socket,message)
                screen.print(message)
                
            except ConnectionRefusedError:
                screen.print(Message(f" Port {peer_port} not available.", "System"))
                continue

        elif (args[0] == "/a"):
            #screen.print(Message("Add friend alias", "System"), Message("Enter IP address of the friend", "System"))
            #friend_ip = input()
            
            #screen.print(Message("Enter port of the friend", "System"))
            #friend_port = input()

            #screen.print(Message("Enter alias", "System"))
            #alias = input()

            friend_ip, friend_port = args[1].split(":")
            friend_port = int(friend_port)

            alias = args[2]

            with open("peer_aliases.json", "w+") as alias_file:
                try:
                    aliases = json.load(alias_file)
                except json.decoder.JSONDecodeError:
                    aliases = {}
            
            aliases[alias] = (friend_ip, friend_port)
            with open("peer_aliases.json", "a+") as alias_file:
                alias_file.write(json.dumps(aliases))
            
            screen.print(Message(f"Alias {alias} added", "System"))

        elif (args[0] == "/pa"):
            #screen.print(Message("Enter alias", "System"))
            #alias = input()

            alias = args[1]

            try:
                with open("peer_aliases.json", "r") as alias_file:
                    aliases = json.load(alias_file)
                    peer_address = aliases[alias][0]
                    peer_port = int(aliases[alias][1])
            except KeyError:
                screen.print(Message("Alias not found", "System"))
                continue
            except FileNotFoundError:
                screen.print(Message("Alias file not found", "System"))
                continue
            
            #screen.print(Message("Enter message", "System"))
            #text = input()

            text = " ".join(args[2:])

            message = Message(text, f"{own_ip}:{own_port}")

            try:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.bind((own_ip, own_port-1))
                peer_socket.connect((peer_address, peer_port))
                send_message(peer_socket,message)
                screen.print(message)
                
            except ConnectionRefusedError:
                screen.print(Message(f" Port {peer_port} not available.", "System"))
                continue
        
        elif (args[0] == "/exit"):
            os._exit(0)

        elif (args[0] == "/help"):
            instructions = [
                "/s : Start group management",
                "/g [group_name] [message]: Send message to a group",
                "/p [ip:port] [message]: Send private message",
                "/a [ip:port] [alias]: Add alias",
                "/pa [alias] [message]: Send private message using alias",
                "/exit: Exit the program",
            ]
            [screen.print(Message(instruction, "System")) for instruction in instructions]

        else:
            screen.print(Message("Invalid command", "System"))
            screen.print(Message("Use /help for commands", "System"))
            continue