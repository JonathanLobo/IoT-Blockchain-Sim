import socket
import sys
import struct
import time
import hashlib



from Block import Block
from BlockChain import BlockChain

start = 0
ip = "192.168.1.154"
port = 8000

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

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (ip, port)
print('connecting to %s port %s' % server_address)
connection = sock.connect(server_address)

bc = ""

mine = True
myDataToMine = -1

while True:
	if(start == 0):
		message = 'new'
		send_msg(sock,message.encode())
		start = 1
		#sock.sendall(message.encode())
	if(start == 1):
		start = 2
		
		data = recv_msg(sock).decode()

		blocks = data.split(",")

		for block in range(0,len(blocks)):
			vals = blocks[block].split(";")

			if(block == 0):
				myDataToMine = vals[0]

			elif(block == 1):
				bc = BlockChain(vals[0],vals[1])
				with open("chain.txt", "w") as myfile:
					myfile.write("Genesis block\n")
			else:
				print(vals)
				bNew = Block(int(vals[0]), vals[1], int(vals[2]), vals[3], vals[4], vals[5])
				err = bc.AddBlock1(bNew)
				with open("chain.txt", "a") as myfile:
					myfile.write(bNew.getData() + '\n')
		sock.close()
	else:
		time.sleep(10)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(server_address)

		send_msg(sock,"READY".encode())
		#print("DONE")
		while True:
			data = recv_msg(sock)
			if(data):
				d= data.decode()
				print("ME " + d)
				d = data.split(",")

				c = bc.getChain()
				c = c[len(c)-1]
				h = c.GetHash()

				if("HIT" == d[0]):
					sock.close()

					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sock.connect(server_address)

					ip = "100.6.20.189"
					
					val = ip + str(h)
					fin = hashlib.sha256(val.encode('utf-8')).hexdigest()
					send_msg(sock,"VERIFY".encode())


				if("HASH" == d[0]):
					sock.close()
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sock.connect(server_address)
					#List of transactions
					#i hash & add to my block
					#data - d[1]    
					myBlock = hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()

					#def __init__(self, nIndexIn, sDataIn, nNonce=-1, tTime=0, sPrevHash=-1, sHash=-1):


					bNew = Block(len(bc.getChain()), d[1], -1, time.time(), h, myBlock)

					message = 'NEWBLOCK,'

					block = bNew.getData()
					
					message = message + block
					send_msg(sock,message.encode())
					myDataToMine = recv_msg(sock).decode()
					bc.AddBlock1(bNew)
					with open("chain.txt", "a") as myfile:
						myfile.write(bNew.getData() + '\n')
					break
				else:
					print("YOO")

		'''
		if(mine):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(server_address)








			mine = False

			block = Block(len(bc.getChain()), myDataToMine)
			finished = bc.AddBlock(block)

			if finished == 1:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect(server_address)
				
				message = 'NEWBLOCK,'
				block = block.getData()
				
				message = message + block
				send_msg(sock,message.encode())
				myDataToMine = recv_msg(sock).decode()
				mine=True
		
			elif finished == -1:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect(server_address)

				message = 'UPDATEME,' + str(len(bc.getChain())-1)
				send_msg(sock,message.encode())
				
				data = recv_msg(sock).decode()
				
				blocks = data.split(",")

				for block in range(0,len(blocks)):
					if(block == 0):
						myDataToMine = vals[0]
					else:
						vals = blocks[block].split(";")
						bNew = Block(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5])
						err = bc.AddBlock1(bNew)

				mine = True
			sock.close()

		c = bc.getChain()

		for i in c:
			print(i.getData())
		
		'''



	



