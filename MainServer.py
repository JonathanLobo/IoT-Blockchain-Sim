import socket
import sys
import struct
from Block import Block
from BlockChain import BlockChain
from random import *

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

# Create BlockChain

bc = BlockChain(5,"hello world")
bc.AddBlockServer(Block(1, "Block 1 Data"))

with open("chain.txt", "a") as myfile:
    myfile.write("Genesis block" + '\n')
    myfile.write(bc.getChain()[1].getData())

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 8000)
print('Starting up on port %s' % server_address[1])
sock.bind(server_address)

sock.listen(4)

transactions = 1

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    print('connection from' + str(client_address))

    # Receive the data
    while True:

        data = recv_msg(connection)
        if data:
            data = data.decode("utf-8").split(',')
            message = data[0]
            print('received ' + message)
            if (message == 'new'):
                chain = bc.getChain()
                chainString = str(transactions) + ','

                for i in range(0, len(chain)):
                    if (i == 0):
                        chainString = chainString + str(bc.getDifficulty()) + ';' + str(chain[i].getSData())
                    else:
                        chainString = chainString + chain[i].getData()
                    if (i != len(chain) - 1):
                        chainString = chainString + ','

                send_msg(connection, chainString.encode())
                print('sent the blockchain to ' + str(client_address))

            elif (message == 'NEWBLOCK'):
                # think about edge case if 2 nodes send newblock at once
                vals = data[1].split(';')
                bNew = Block(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5])
                bc.AddBlock1(bNew)
                with open("chain.txt", "a") as myfile:
				    myfile.write(bNew.getData() + '\n')
                transactions = str(randint(1, 100000))
                send_msg(connection, str(transactions).encode())

            elif (message == 'DIDILOSE'):
                if (int(data[1]) == len(bc.getChain())):
                    send_msg(connection, 'NO'.encode())
                else:
                    send_msg(connection, 'YES'.encode())

            elif (message == 'UPDATEME'):
                chainString = str(transactions) + ','
                index = int(data[1]) + 1
                chain = bc.getChain()

                for i in range(index, len(chain)):
                    chainString = chainString + chain[i].getData()
                    if i != len(chain) - 1:
                        chainString = chainString + ','

                send_msg(connection, chainString.encode())

            break

# Clean up the connection
connection.close()
