from Block import Block
import struct

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

class BlockChain:

	_nDifficulty = -1
	chain = []
	def __init__(self, nDifficulty, genesis):
		self._nDifficulty = nDifficulty

		self.chain.append(Block(0, genesis))

	def _GetLastBlock(self):
		return self.chain[len(self.chain)-1]

	def AddBlock(self, bNew):
		bNew.sPrevHash = self._GetLastBlock().GetHash()
		bNew.MineBlock(int(self._nDifficulty))
		
		# Create a TCP/IP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect the socket to the port where the server is listening
		server_address = (ip, port)
		print('connecting to %s port %s' % server_address)
		connection = sock.connect(server_address)

		message = "DIDILOSE" + "," + str(self._nIndex)
		send_msg(sock, message.encode())
		finished = -2
		while True:
			data = recv_msg(sock).decode()
			if(data):
				if(data == "YES"):
					sock.close()
					finished =  -1
				else:
					sock.close()
					finished = 0

		if(finished == 0):
			self.chain.append(bNew)
			return finished

	def AddBlockServer(self, bNew):
		bNew.sPrevHash = self._GetLastBlock().GetHash()
		finished = bNew.MineBlockServer(int(self._nDifficulty))
		if(finished == -1):
			return -1
		else:
			self.chain.append(bNew)
			return finished

	def AddBlock1(self, bNew):
		bNew.sPrevHash = self._GetLastBlock().GetHash()
		self.chain.append(bNew)

	def getChain(self):
		return self.chain

	def getDifficulty(self):
		return self._nDifficulty
