from flask import Flask, jsonify
import json
import hashlib
import datetime

class Blockchain(object):

	def __init__(self):
		self.chain = []
		self.create_block(1234,'1234')

	def create_block(self, nonce, previous_hash):
		block = {
			'index':len(self.chain) + 1,
			'time_stamp':str(datetime.datetime.now()),
			'nonce':nonce,
			'prev_hash':previous_hash
		}
		self.chain.append(block)
		return block


	def get_prev_block(self):
		return self.chain[-1]

	def challenge(self, prev_nonce):
		nonce = 1
		while True:
			hash_val = hashlib.sha256(str((nonce **2) - (prev_nonce**2)).encode()).hexdigest()
			if hash_val[:4] == '0000':
				return nonce
				break
			nonce += 1

	def hash_block(self, block):
		return hashlib.sha256(json.dumps(block).encode()).hexdigest()


	def is_valid(self):
		prev_block = self.chain[0]
		current_block_no = 1
		while current_block_no < len(self.chain):
			current_block = self.chain[current_block_no]
			prev_nonce = prev_block['nonce']
			current_nonce = current_block['nonce']
			hash_val = hashlib.sha256(str((current_nonce **2) - (prev_nonce**2)).encode()).hexdigest()
			if hash_val[:4] != '0000':
				return False

			if self.hash_block(prev_block) != current_block['prev_hash']:
				return False

			prev_block = current_block
			current_block_no += 1
		return True 

app = Flask(__name__)

block_chain = Blockchain()

@app.route("/mine-block")
def mine_block():
	prev_nonce = block_chain.chain[-1]['nonce']
	nonce = block_chain.challenge(prev_nonce)
	prev_block = block_chain.get_prev_block()
	prev_hash = block_chain.hash_block(prev_block)
	block = block_chain.create_block(nonce, prev_hash)
	return jsonify(block)

@app.route("/valid")
def is_valid():
	if block_chain.is_valid():
		return jsonify('The Blockchain is valid')
	return jsonify('Blockchain is not valid')

if __name__ == "__main__":
	app.run(debug=True)
