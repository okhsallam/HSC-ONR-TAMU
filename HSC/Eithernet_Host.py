import socket

# Set the IP address and port for the server
# HOST = '10.125.213.255'  # Replace with the actual IP address of the Jetson Nano

HOST = '172.17.0.1'
HOST = '192.168.1.112'

PORT = 12345


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# Accept a connection from the client
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

# Receive data from the client
data = client_socket.recv(1024).decode('utf-8')
print(f"Received data: {data}")

# Close the connection
client_socket.close()
server_socket.close()

