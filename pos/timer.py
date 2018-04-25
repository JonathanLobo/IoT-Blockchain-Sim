import socket
import sys
import struct
import time

start = 0
ip = "192.168.1.154"
port = 8000

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (ip, port)
print('connecting to %s port %s' % server_address)
connection = sock.connect(server_address)


def send_msg(sock, msg):
	# Prefix each message with a 4-byte length (network byte order)
	msg = struct.pack('>I', len(msg)) + msg
	sock.sendall(msg)

def recv_msg(sock):
	# Read message length and unpack it into an integer
	raw_msglen = recvall(sock, 4)
	if not raw_msglen:
		return None
	msglen = struct.unpack('>I', raw_msglen)[0]
	# Read the message data
	return recvall(sock, msglen)

def recvall(sock, n):
	# Helper function to recv n bytes or return None if EOF is hit
	data = b''
	while len(data) < n:
		packet = sock.recv(n - len(data))
		if not packet:
			return None
		data += packet
	return data

start = time.time()
while True:

	end = time.time()
	dif = end-start

	if(dif>5):
		start = time.time()
		send_msg(sock, "SENDMSG".encode())
		print("10")



