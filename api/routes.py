from flask import Flask, jsonify, request, render_template
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from blockchain.wallet import Wallet
from networking.node import Node

app = Flask(__name__,
            static_folder='../static',
            template_folder='../templates')

node = Node()

# Web interface routes
@app.route('/', methods=['GET'])
def index():
    """Render the homepage"""
    return render_template('index.html')

@app.route('/blockchain-view', methods=['GET'])
def blockchain_view():
    """Render the blockchain visualization page"""
    chain_date = node.blockchain.chain
    return render_template('blockchain.html', chain=chain_date)

@app.route('/wallet-view', methods=['GET'])
def wallet_view():
    """Render the wallet page"""
    return render_template('wallet.html', wallet_address=node.wallet.address)

@app.route('/transaction-view', methods=['GET'])
def transaction_view():
    """Render the transaction page"""
    return render_template('transactions.html', transaction=node.transaction_pool)

# API endpoints
@app.route('/mine', methods=['GET'])
def mine():
    """
    Mine a new block.
    """
    block = node.mine_block()

    if not block:
        return jsonify({'message': 'No transactions to mine'}), 400
    
    return jsonify({
        'message': 'New block minded',
        'block': block.__dict__
    }), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Create a new transaction.
    """
    try:
        values = request.get_json()

        required = ['recipient', 'amount']
        if not all(k in values for k in required):
            return jsonify({'message': 'Missing values'}), 400
        
        # Validate amount is positive
        amount = float(values['amount'])
        if amount <= 0:
            return jsonify({'message': 'Amount must be positive'}), 400
        
        transaction = Transaction(
            sender_wallet=node.wallet,
            recipient=values['recipient'],
            amount=amount
        )

        transaction.sign()
        node.add_transaction(transaction)

        return jsonify({
            'message': f'Transaction will be added to Block {len(node.blockchain.chain)}',
            'transaction_id': transaction.id
        }), 201
    except ValueError:
        return jsonify({'message': 'Invalid amount format'}), 400
    except Exception as e:
        return jsonify({'message': f'Error creating transaction: {str(e)}'}), 500

@app.route('/chain', methods=['GET'])
def full_chain():
    """
    Return the full blockchain.
    """
    response = {
        'chain': node.blockchain.to_json(),
        'length': len(node.blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """
    Register a new node in the network.
    """
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return jsonify({'message': 'Error: Please supply a valid list of nodes'}), 400
    
    for node_address in nodes:
        node.register_peer(node_address)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(node.peers)
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """
    Resolve conflict between blockchain nodes.
    """
    replaced = node.consensus()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': node.blockchain.to_json()
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': node.blockchain.to_json()
        }
    
    return jsonify(response), 200