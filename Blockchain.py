# -*- coding: utf-8 -*-
""" Created on Thu Aug  1 11:08:06 2019

@author: dhbhatt
"""
#Module 1 - Creating a Blockchain 
#importing library
import datetime 
import hashlib
import json
from flask import Flask, jsonify
#Part1 - Building a blockchain
#Class will contain Genesis block fn,create block fn 
class Blockchain:
#  Instance object of class
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self,proof,previous_hash):
        block={'index': len(self.chain) + 1,
               'timestamp': str(datetime.datetime.now()),
               'proof':proof,
               'previous_hash':previous_hash}    
        self.chain.append(block)
        return block
       
    def get_previous_block(self):
        return self.chain[-1]
    
#    nonce value
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof 
        
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys = False).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False 
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

#Part 2 Mining a block chain

#creating a web app
app = Flask(__name__)        
    
#creating a blockchain object to use the class
blockchain = Blockchain() 

#Mining a new block 
@app.route('/mine_block', methods=['GET'])  
def mine_block():
    previous_block =  blockchain.get_previous_block()
    previous_proof =  previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response  = {'message': "Congratulations you just mine a block",
                 'index': block['index'],
                 'timestamp': block['timestamp'],
                 'proof': block['proof'],
                 'previous_hash': block['previous_hash'],
                 'Current_hash':blockchain.hash(block)}
    return jsonify(response), 200

#getting the full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200      


     
#Creatin is chain valid response 
@app.route('/is_valid', methods=['GET'])  
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid == True:
        response = {'messaege':'All good. The blockchain is Valid'}
    else:
        response = {'messaege':'Problem.The blockchain is not Valid'}
        
    return jsonify(response),200
  
#running the app
app.run(host = '0.0.0.0', port = 5000)          
                
        