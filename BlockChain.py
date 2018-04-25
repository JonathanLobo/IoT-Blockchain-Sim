from Block import Block

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
		finished = bNew.MineBlock(int(self._nDifficulty))
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




