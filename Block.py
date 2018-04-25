import hashlib
import socket
import sys
from datetime import datetime
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



class Block:
	_nIndex = 0
	_sData = 0
	_nNonce = -1
	_tTime = 0
	sPrevHash = 0
	_sHash = -1

	def __init__(self, nIndexIn, sDataIn, nNonce=-1, tTime=0, sPrevHash=-1, sHash=-1):
		self._tTime = str(datetime.now())
		self._nIndex = nIndexIn
		self._sData = sDataIn
		self._nNonce = nNonce
		self.sPrevHash = sPrevHash
		self._sHash = sHash


	def GetHash(self):
		return self._sHash

	def _CalculateHash(self):
		val = str(self._nIndex) + str(self._tTime)+ str(self._sData)+ str(self._nNonce) + str(self.sPrevHash)
		return hashlib.sha256(val.encode('utf-8')).hexdigest()


	def MineBlock(self, nDifficulty):
		cstr = ""
		for i in range(0,nDifficulty):
			cstr = cstr + "0"

		cstr = str(cstr)

		tempHash = ""

		count = 0

		while tempHash[0:nDifficulty] != cstr:
			self._nNonce = self._nNonce + 1
			tempHash = self._CalculateHash()
			count = count + 1
			if(count % 100000 == 0):
				# Create a TCP/IP socket
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

				# Connect the socket to the port where the server is listening
				server_address = (ip, port)
				print('connecting to %s port %s' % server_address)
				connection = sock.connect(server_address)

				message = "DIDILOSE" + "," + str(self._nIndex)
				send_msg(sock, message.encode())
				while True:
					data = recv_msg(sock).decode()
					if(data):
						if(data == "YES"):
							sock.close()
							return -1
						else:
							sock.close()
							break



		self._sHash = tempHash

		print("Block Mined: " + self._sHash)
		return 1

	def MineBlockServer(self, nDifficulty):
		cstr = ""
		for i in range(0,nDifficulty):
			cstr = cstr + "0"

		cstr = str(cstr)

		tempHash = ""

		count = 0

		while tempHash[0:nDifficulty] != cstr:
			self._nNonce = self._nNonce + 1
			tempHash = self._CalculateHash()

		self._sHash = tempHash

		print("Block Mined:" + self._sHash)
		return 1

	def getData(self):
		formatted = str(self._nIndex) + ";" + str(self._sData) + ";" + str(self._nNonce) + ";" + str(self._tTime) + ";" + str(self.sPrevHash) + ";" + str(self._sHash)

		return formatted

	def getSData(self):
		return self._sData
