import socket
import threading

# function receive data from the client socket
def connect_socket(conn):
    while True:
        # receive data from the socket
        received_data = conn.recv(1024).decode()
        if not received_data:
            break
        # print received, decoded, data 
        else:
            print(received_data)
    
    conn.close()

# function to send data 
def send_message(conn):
    while True:
        # take input and enocde
        message_to_send = input().encode()
        # send message
        conn.sendall(message_to_send)



if __name__ == '__main__':
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set IP address and port to the socket
    s.bind(('', 11111))
    # listen connections from clients
    s.listen()
    # when client connects, accept the connection
    (client_conn, client_addr) = s.accept() 
    print("Connection from: ", client_addr)
    # create thread for connection process
    thread1 = threading.Thread(target = connect_socket, args = ([client_conn]))
    # create thread for message sending process
    thread2 = threading.Thread(target = send_message, args = ([client_conn]))
    #start both threads
    thread1.start()
    thread2.start()
    # end both threads
    thread1.join()
    thread2.join()

