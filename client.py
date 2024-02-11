import socket
import threading


# function to receive data
def receive_data(s):
    while True:
        # receive message
        received_msg = s.recv(1024).decode()
        # print message
        print(received_msg)


# function to receive messages
def send_message(s):
    while True:
        # encode message taken from the input
        message = input("Enter message: ")
        msg_to_send = message.encode('utf-8')
        # send message
        s.sendall(msg_to_send)

# function to handle coming connections
def handle_connections(s):
    while True:
        coming_socket, coming_address = s.accept()
        print("Connection from: ", coming_address)
        
        # Start a thread to handle the incoming connection
        receive_thread = threading.Thread(target=receive_data, args=([coming_socket]))
        receive_thread.start()




if __name__ == '__main__':
    
    print("#####################################")
    print("#           WELCOME!                #")
    print("#####################################")

    own_ip = input("Enter your own IP: ")
    own_port = int(input("Enter your port: "))

    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set IP address and port to the socket
    s.bind((own_ip, own_port))
    # listen connections from other peers
    s.listen(5)

    print("Peer listening on {}:{}".format(own_ip, own_port))

    # start thread to handle incoming connections
    connection_handle_thread = threading.Thread(target=handle_connections, args=([s]))
    connection_handle_thread.start()

    # Connect to another peer
    peer_address = input("Enter IP address of the friend: ")
    peer_port = int(input("Enter port of the friend: "))

    # Connect to the other peer
    print("Connection establishment started...")
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.connect((peer_address, peer_port))
    print("Connected to: ", peer_address)

    # create thread to send messages
    send_message_thread = threading.Thread(target = send_message, args = ([peer_socket]))
    # start thread
    send_message_thread.start()

    
