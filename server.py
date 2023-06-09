import socket
import os

# Create a socket object
proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port of the proxy server
HOST = 'server ip address'
PORT = 8888

# Bind the socket object to the host and port
proxy_server.bind((HOST, PORT))

# Listen for incoming connections
proxy_server.listen()

# Define the cache folder name
CACHE_FOLDER = 'cache'

# Create the cache folder if it doesn't exist
if not os.path.exists(CACHE_FOLDER):
    os.mkdir(CACHE_FOLDER)

print(f"Proxy server is listening on {HOST}:{PORT}")

while True:
    # Wait for a client to connect
    client_socket, client_address = proxy_server.accept()
    print(f"Received connection from {client_address}")

    # Receive the request from the client
    request = client_socket.recv(4096).decode()
    print(f"Received request from client:\n{request}")

    # Get the URL from the request
    url = request.split()[1]

    # Extract the domain from the URL
    domain = url.split('/')[2]

    # Create a cache file name using the domain name
    filename = os.path.join(CACHE_FOLDER, f"{domain}.cache")

    # Check if the response is in the cache
    if os.path.exists(filename):
        print(f"Cache hit for {url}")
        with open(filename, 'rb') as f:
            response = f.read()
    else:
        # Send the request to the server
        print(f"Cache miss for {url}")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((url.split('/')[2], 80))
        server_socket.sendall(request.encode())

        # Receive the response from the server
        response = server_socket.recv(4096)

        # Save the response to the cache
        try:
            with open(filename, 'wb') as f:
                f.write(response)
                print(f"Saved response to cache file {filename}")
        except Exception as e:
            print(f"Error writing to cache file {filename}: {e}")

    # Send the response to the client
    client_socket.sendall(response)

    # Close the sockets
    client_socket.close()
    server_socket.close()