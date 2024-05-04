import socket

# Define server IP address and port
server_ip = '192.168.1.100'  # Replace with your Raspberry Pi's IP address
server_port = 1234

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
client_socket.connect((server_ip, server_port))

try:
    # Send data to the server
    message = "Hello from the client!"
    client_socket.sendall(message.encode())

finally:
    # Clean up the connection
    client_socket.close()
