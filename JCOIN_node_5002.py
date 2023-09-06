# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 10:13:47 2023

@author: Juan_Cruz_Gimenez
"""

# Modulo 2 Crear una Criptomoneda

# Importar librerias
import datetime
import hashlib
import json
import requests
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse

# Parte 1 - Crear la Cadena de Bloques

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        
        
    def create_block(self, proof, previous_hash):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'previous_hash' : previous_hash,
            'transactions' : self.transactions,
            }
        self.transactions = []
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
    
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender'.sender,
            'receiver'.receiver,
            'amaount'.amount,
            })
        previous_block = self.previous_block()
        return previous_block['index'] + 1
    
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
        
    def replace_chain(self):
        network = self.nodes
        longuest_chain = None
        max_lenght = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_lenght and self.is_chain_valid(chain):
                    max_lenght = length
                    longuest_chain = chain
        if longuest_chain:
            self.chain = longuest_chain
            return True
        return False
    
        
# Parte 2 - Minado de un Bloque de la Cadena

# Crear una aplicacion web
app = Flask(__name__)

# Crear la direcciondel nodo en el puerto 5000
node_address = str(uuid4()).replace('-', '')

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
    blockchain.add_transaction(sender = node_address, receiver = "Kirril", amount = 10)
    response = {
        'message': 'Bien hecho, has minado un nuevo bloque!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transctions': block['transactions'],
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


# Añadir una nueva transaction a la cadena de bloques
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transction_keys):
        return 'Faltan alguns elementos de la transaction', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'La transaction sera añadida al bloque {index}'}
    return jsonify(response), 201
    

# Parte 3 - Descentralizar la Cadena de Bloques

# Conectar nuevos nodos
@app.route('/conect_node', methods = ['POST'])
def conect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No hay nodos para añadir', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': 'Todos los nodos han sido conectado. La cadena de JCOIN contiene ahora los nodos siguientes: ',
        'total_nodes': list(blockchain.nodes),
        }
    return jsonify(response), 201

# Reemplazar la cadena por la mas larga (si es necesario)
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            'message': 'Los nodos tenian diferentes cadenas, han sido reeplazado por la mas larga',
            'new_chain': blockchain.chain, 
            }
    else:
        response = {
            'message': 'Todo correcto. La cadena en todos los nodos ya es la mas larga',
            'actual_chain': blockchain.chain,
            }
    return jsonify(response), 200


# Ejecutar la app
app.run(host = '0.0.0.0', port = 5002)