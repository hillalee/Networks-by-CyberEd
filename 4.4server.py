import socket
import validators
import os

WEBSITE = "http://127.0.0.1:80"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 80
WEBROOT = r"C:\Networks\NetworksBook\ex44\webroot\webroot"
INDEX = "index.html"

TYPES = {
	"html": "text/html; charset=utf-8",
	"txt": "text/html; charset=utf-8",
	"jpg": "image/jpeg",
	"js": "text/javascript; charset=UTF-8",
	"css": "text/css"
}
MOVED = {
	r"{}\file1.txt".format(WEBROOT) : r"{}\file2.txt".format(WEBROOT)
}
FORBIDDEN = [r"{}\forbidden.txt".format(WEBROOT)]



def handle_client_message(conn: socket):
	msg = conn.recv(1024).decode()
	parsed = msg.split(r"\r\n")
	# check if msg is in correct form
	if not (parsed[0].startswith("GET") and parsed[0].endswith("HTTP/1.1")):
		status = 500
		errorMsg= r"HTTP/1.1 500 Internal Server Error\r\n"
		print(errorMsg)
		conn.send(errorMsg.encode())
		return

	#extract url, check if it exists
	url = parsed[0].split(" ")[1]
	if url == "/" or "\\":
		url += INDEX
	file = f"{WEBROOT}{url}"
	valid = os.path.isfile(file)

	#invalid file
	if not valid:
		status = 404
		errorMsg = r"HTTP/1.1 404 File Not Found\r\n"
		conn.send(errorMsg.encode())
		return

	#forbidden file
	if file in FORBIDDEN:
		status = 403
		errorMsg = r"HTTP/1.1 403 Forbidden \r\n"
		conn.send(errorMsg.encode())
		return

	#file moved temporarily
	if file in MOVED.keys():
		status = 302
		errorMsg = r"HTTP/1.1 302 Moved Temporarily to {} \r\n".format(MOVED[file])
		conn.send(errorMsg.encode())
		return

	#open file
	with open(file, "r") as f:
		fileData = f.read()
		packet = r'HTTP/1.1 200 OK\r\n'
		fileType = file.split(os.path.sep)[-1].split('.')[-1]

		# check if file type is supported
		if fileType not in TYPES.keys():
			status = 500
			errorMsg = r"HTTP/1.1 500 Internal Server Error\r\n"
			print(errorMsg)
			conn.send(errorMsg.encode())
			return

		#build msg according to HTTP protocol
		fileKey = TYPES[fileType]
		print("file type = {}".format(fileType))
		packet += 'Content-Type: {}\r\n'.format(fileKey)
		packet += 'Content-Length: {}\r\n'.format(len(fileContent))
		packet = bytes_packet.encode()
		packet += fileData

		return packet



def main():
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		conn.bind((SERVER_IP, SERVER_PORT))
	except OSError:
		print("Try again later")
		exit()

	print("Server is running")
	conn.listen()

	while True:
		(client_socket, client_address) = conn.accept()
		while True:
			handle_client_msg(client_socket)



if __name__ == '__main__':
    main()