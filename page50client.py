import socket
import datetime
import random

SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"

def setup_socket():
	"""
    Creates new listening socket and returns it
    Receives: -
    Returns: the socket object
    """
	conn = socket.socket()
	try:
		conn.connect((SERVER_IP, SERVER_PORT))
	except OSError:
		print("Try again later")
		exit()
	return conn


def recv_msg(conn):
	decodedMsg = conn.recv(1024).decode()
	return decodedMsg


def send_msg(conn, msg):
	encodedMsg = msg.encode()
	print("\nSent message")
	conn.send(encodedMsg)



def exit_request(conn):
	conn.close()
	print("Connection closed")


def main():
	conn = setup_socket()

	while True:
		msg = input("""Menu:\n
					------ \n
					 Get time \t\t -t-\n
					 Get server name \t\t -n-\n
					 Ger random number \t\t -r-\n
					 \tEXIT \t\t -e-\n
					 Your input: \n""")
		if msg == "t":
			send_msg(conn, "TIME")
			msgRcv = recv_msg(conn)
			print(msgRcv)
		if msg == "n":
			send_msg(conn, "WHORU")
			msgRcv = recv_msg(conn)
			print(msgRcv)
		if msg == "r":
			send_msg(conn, "RAND")
			msgRcv = recv_msg(conn)
			print(msgRcv)
		if msg == "e":
			send_msg(conn, "EXIT")
			exit_request(conn)
			break


if __name__ == "__main__":
	main()

