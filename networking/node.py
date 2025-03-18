import requests
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from blockchain.wallet import Wallet

class Node:
    """
    A node in the blockchain network.
    Each node maintains a copy of the blockchain and can mine new blocks.
    """
    def __init__(self):
        self.blockchain = Blockchain()
        self.wallet = Wallet()
        self.transaction_pool = []
        self.peers = set()

    def add_transaction(self, transaction):
        """
        Add a transaction to the transaction pool.
        """
        self.transaction_pool.append(transaction)

    def mine_block(self):
        """
        Mine a new block with the current transaction pool.
        """
        if not self.transaction_pool:
            return None
        
        self.blockchain.add_block(self.transaction_pool)
        block = self.blockchain.chain[-1]
        self.transaction_pool = []

        return block
    def register_peer(self, address):
        """
        Add a new peer to the list of peers.
        """
        self.peers.add(address)

    def consensus(self):
        """
        Resolve conflicts between blockchain nodes by replacing our chain with the longest one in the network.
        """
        longest_chain = None
        max_length = len(self.blockchain.chain)

        for peer in self.peers:
            try:
                response = requests.get(f'http://{peer}/chain')

                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    if length > max_length:
                        try:
                            self.blockchain.validate_chain(chain) # Add validation
                            max_length = length
                            longest_chain = chain
                        except Exception as e:
                            print(f"Invalid chain from peer {peer}: {e}")
                            continue
            except requests.RequestException as e:
                print(f"Error connecting to peer {peer}: {e}")
                continue
        if longest_chain:
            self.blockchain.chain = longest_chain
            return True
        return False
        