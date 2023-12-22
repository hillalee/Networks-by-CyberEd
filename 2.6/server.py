import socket
import datetime
import random


SERVER_NAME = "SuperAwesomeServer"
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"

MAX_RAND = 10
MIN_RAND = 1

def setup_socket():
	"""
    Creates new listening socket and returns it
    Receives: -
    Returns: the socket object
    """
	conn = socket.socket()
	try:
		conn.bind((SERVER_IP, SERVER_PORT))
	except OSError:
		print("Try again later")
		exit()
	conn.listen()
	return conn

def parse_recv_msg(conn):
	decodedMsg = conn.recv(2).decode()
	length = int(decodedMsg[:2])
	msg = conn.recv(length).decode()
	return length, msg

def send_time(conn):
	currentTime = datetime.datetime.now()
	msg = "Current Hour is: {}".format(currentTime)
	conn.send(msg.encode())
	print(msg)

def send_name(conn):
	msg = "Server name is: {}".format(SERVER_NAME)
	conn.send(msg.encode())
	print(msg)

def send_rand(conn):
	randNum = random.randint(MIN_RAND, MAX_RAND)
	msg = "Random number from {} to {}: {}".format(MIN_RAND, MAX_RAND, randNum)
	conn.send(msg.encode())
	print(msg)

def exit_request(conn):
	print("Client closed")
	conn.close()


def main():
	conn = setup_socket()
	(client_socket, client_address) = conn.accept()
	print("Client connected")
	while True:
		length, msg = parse_recv_msg(client_socket)

		if msg == "TIME":
			send_time(client_socket)
		if msg == "WHORU":
			send_name(client_socket)
		if msg == "RAND":
			send_rand(client_socket)
		if msg == "EXIT":
			exit_request(client_socket)
			conn.close()
			break




if __name__ == "__main__":
	main()
