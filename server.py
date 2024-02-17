import socket
import threading

clients = set()

# function receive data from the client socket
def connect_socket(conn):
    while True:
        # receive data from the socket
        received_data = conn.recv(1024).decode()
        print(received_data)
    
    

# function to send data 
def send_message(conn):
    while True:
        # take input and enocde
        message_to_send = input().encode()
        # send message
        conn.sendall(message_to_send)



# function to handle coming connections
def handle_connections(s):
    while True:
        coming_socket, coming_address = s.accept()
        print("Connection from: ", coming_address)
        
        # Start a thread to handle the incoming connection
        receive_thread = threading.Thread(target=connect_socket, args=([coming_socket]))
        receive_thread.start()

        send_thread = threading.Thread(target = send_message, args = ([coming_socket]))
        send_thread.start()



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
    
