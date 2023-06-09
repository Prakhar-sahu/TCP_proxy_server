from socket import *
import webbrowser

if _name_ == '_main_':
    proxyHost = 'server ip address' 
    proxyPort = 8888 

    while True:
        url = input("Enter the URL to fetch: ")
        
        # Create a TCP socket and connect to the proxy server
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((proxyHost, proxyPort))

        # Send the request to the proxy server
        request = "GET " + url + " HTTP/1.1\r\n"
        request += "Host: " + url.split('/')[1] + "\r\n"
        request += "Connection: close\r\n\r\n"
        clientSocket.sendall(request.encode())

        # Receive the response from the proxy server and print it
        response = b''
        while True:
            data = clientSocket.recv(4096)
            if not data:
                break
            response += data

        print(response.decode())

        # Open the URL in the default web browser
        webbrowser.open(url)

        # Close the socket
        clientSocket.close()