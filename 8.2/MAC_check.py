from scapy.all import *
VALID_LEN = 17

mac_addresses = [
    "11:22:33:44:55:66",   # Valid address
    "FF:FF:FF:FF:FF:FF",   # Valid address
    "34:31:21cd:12:AB",    # Valid address
    "11:22:33:44:55:66:77", # Invalid address
    "11-22-33-44-55-66",   # Invalid address for this script
    "11:22:33:44:55",      # Invalid address
    "22:33:44:55:661H"     # Invalid address
]  


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


