import socket
host = '127.0.0.1'
port = 1234
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host,port))
client_socket.sendall('test'.encode())
data = client_socket.recv(1024)
print('Received', repr(data.decode()))
client_socket.close()