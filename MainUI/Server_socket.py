import socket;

Server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
Server_socket.bind(('127.0.0.1',9999))
Server_socket.listen()

client_socket, addr = Server_socket.accept()
while True:
    data = client_socket.recv(1024)
    if data != '\0':
        print(data)
    else:
        pass
        

client_socket.close()
Server_socket.close()