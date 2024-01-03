from scapy.all import *
VALID_LEN = 17


def valid_MAC(address):
	rc = True

	add_split = address.split(":")
	valid_split = all(len(byte) == 2 for byte in add_split)

	if len(address) != VALID_LEN or not valid_split:
		rc = False

	return rc

while True:
	user_MAC = input("Enter MAC address: \n")

	# loop
	if user_MAC == "exit":
		break
	if valid_MAC(user_MAC):
		print(f"""MAC Address: '{user_MAC}' is valid \n"""
		      Vendor ID: {user_MAC[:8]}""")
	else:
		print(f"""MAC Address: '{user_MAC}' is invalid \n""")


