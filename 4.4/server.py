import socket
import validators
import os
import re

IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 1
WEBSITE = "http://127.0.0.1:80"
WEBROOT = r"C:\Networks\NetworksBook\ex44\webroot\webroot"
INDEX = "\index.html"

TYPES = {
    "html": "text/html; charset=utf-8",
    "txt": "text/html; charset=utf-8",
    "jpg": "image/jpeg",
    "js": "text/javascript; charset=UTF-8",
    "css": "text/css"
}

REDIRECTION_DICTIONARY = {
    r"{}\file1.txt".format(WEBROOT): r"{}\file2.txt".format(WEBROOT)
}

STATUS = {
    "200": "OK",
    "404": "File Not Found",
    "403": "Forbidden",
    "302": "Moved Temporarily",
    "500": "Internal Server Error"
}
FORBIDDEN = [r"{}\forbidden.txt".format(WEBROOT)]
CALCULATE = f"{WEBROOT}/calculate-next"


def get_file_data(filename):
    with open(filename, "r") as file:
        fileData = file.read()
        return fileData


def handle_client_request(resource, client_socket):
	""" Check the required resource, generate proper HTTP response and send to client"""

	if resource == os.path.sep or resource == "/":
		url = f"{WEBROOT}{INDEX}"
	else:
		resource = re.sub(r'\/+', r'\\', resource)
		url = f"{WEBROOT}{resource}"

	#check if URL had been redirected, not available or other error code. For example:
	if url in REDIRECTION_DICTIONARY:
		statusKey = "302"
		errorMsg = f"HTTP/1.1 {statusKey} {url} Moved Temporarily to {REDIRECTION_DICTIONARY[url]} \r\n"
		client_socket.send(errorMsg.encode())
		return

	# extract requested file type from URL (html, jpg etc)
	filetype = url.split(os.path.sep)[-1].split(".")[-1]

	if filetype in TYPES:
		status = "200"
		http_header = f"HTTP/1.1 {status} {STATUS[status]}\r\n"
		http_header += f'Content-Type: {TYPES[filetype]}\r\n'
	else:
		# file not supported
		status = "403"
		errorMsg = f"HTTP/1.1 {status} {STATUS[status]}\r\n"
		client_socket.send(errorMsg.encode())
		return

	# read the data from the file
	if filetype == "jpg":
		with open(url, "rb") as file:
			fileData = file.read()
			http_header += f'Content-Length: {len(fileData)}\r\n\r\n'
			http_response = http_header.encode() + fileData
			client_socket.send(http_response)
	else:
		data = get_file_data(url)
		http_header += f'Content-Length: {len(data)}\r\n\r\n'
		http_response = http_header + data
		client_socket.send(http_response.encode())


def validate_http_request(request):
	"""
	Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
	"""
	valid = True
	parsed = request.split(r"\r\n")

	# check if msg is in correct form
	if not parsed[0].startswith('GET'):
		status = 500
		errorMsg = r"HTTP/1.1 500 Internal Server Error\r\n"
		print(errorMsg)
		valid = False
		return valid, errorMsg
	url = parsed[0].split(" ")[1]
	urlPath = url.replace(os.path.sep, '/')

	return valid, url


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        client_request = client_socket.recv(1024).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http or resource == "":
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    print("Server is running\n")
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
