from socket import *
import threading
import os
import constant

import builtins
import socket as stdlib_socket

socket = getattr(builtins, 'socket', stdlib_socket)



class MyServer:
   
        
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self):
        print(f"Server started on http://{constant.IP_SERVER}:{constant.PORT}")
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((constant.IP_SERVER, constant.PORT))
        self.server_socket.listen()
        while True:
            client_connection, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client_request, args=(client_connection, client_address))
            client_thread.start()
    
        

    def handle_client_request(self, client_connection,client_socket):
        #request_data = client_socket.recv(1024)
        #request_text = request_data.decode('utf-8')
        #request_lines = request_text.split('\r\n')
        #request_line_parts = request_lines[0].split(' ')
        data = client_connection.recv(1024)
        request = str(data.decode('utf-8'))
        request_method = request.split(' ')[0]
        request_path = request.split(' ')[1]
        

        #method = request_line_parts[0]
        #path = request_line_parts[1]


        if request_method == 'GET':
            if request_path == '/' :
                html_content=self.get_html_content('/')
                response = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + bytes(str(len(html_content)), 'utf-8') + b"\r\n\r\n" + html_content
                client_connection.sendall(response)    
            #response_body = '<h1>Hello, world!</h1>'
            #response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {}\r\nConnection: close\r\n\r\n'.format(len(response_body)).encode('utf-8')
            #response = response_headers + response_body.encode('utf-8')
        else:
            response_body = '<h1>Method not allowed</h1>'
            response_headers = 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\nContent-Length: {}\r\nConnection: close\r\n\r\n'.format(len(response_body)).encode('utf-8')
            response = response_headers + response_body.encode('utf-8')

        client_socket.sendall(response)
        client_socket.close()

    def get_html_content(self, request_path):
        # Obtener el nombre del archivo solicitado
        if request_path == "/":
            file_name = "index.html"
        else:
            file_name = request_path.lstrip("/")

        # Construir la ruta completa del archivo
        file_path = os.path.join(os.path.dirname(__file__), "documentRootFolder", file_name)

        # Leer el contenido HTML del archivo
        try:
            with open(file_path, "rb") as f:
                html_content = f.read()
        except:
            html_content = b"<h1>Archivo no encontrado</h1>"

        return html_content
'''class MyHTTPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        request = self.data.decode('utf-8')
        request_method = request.split(' ')[0]
        request_path = request.split(' ')[1]
        
        if request_method == 'GET':
            if request_path == '/':
               
            elif request_path == '/about':
                html_content = get_html_content('about.html')
                response = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + bytes(str(len(html_content)), 'utf-8') + b"\r\n\r\n" + html_content
                self.request.sendall(response)
            else:
                html_content = b"<html><body><h1>404 Not Found</h1></body></html>"
                response = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: " + bytes(str(len(html_content)), 'utf-8') + b"\r\n\r\n" + html_content
                self.request.sendall(response)
   '''    

server = MyServer()
server.start()
