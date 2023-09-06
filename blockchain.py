# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:54:14 2023

@author: Juan_Cruz_Gimenez
"""

# Modelo 1 Crear una cadena de bloques

# Importar librerias

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Parte 1 - Crear la Cadena de Bloques
class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'previous_hash' : previous_hash,       
            }
        self.chain.append(block)
        
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**3).encode()).hexdigest()
            
            if hash_operation[:5] == "00000":
                check_proof = True
            else:
                new_proof += 1 
                
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**3).encode()).hexdigest()
            
            if hash_operation[:5] != "00000":
                return False
            
            previous_block = block
            block_index += 1
            
        return True
        
# Parte 2 - Minado de un Bloque de la Cadena

# Crear una aplicacion web
app = Flask(__name__)

# Crear una Blockchain
blockchain = Blockchain()

# Minar un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Has minado un nuevo bloque!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']        
        }
    
    return jsonify(response), 200

# Obtener la cadena de bloques al completo
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'lenght': len(blockchain.chain)
        }
    
    return jsonify(response), 200


# Verificar la validez de la cadena de bloques
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'La cadena de bloques es válida.'}
    else:
        response = {'message': 'La cadena de bloques no es válida.'}
    
    return jsonify(response), 200


# Ejecutar la app
app.run(host = '0.0.0.0', port = 5000)