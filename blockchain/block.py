import time
from utils.crypto_hash import crypto_hash

class Block:
    """
    Block: a unit of storage in the blockchain.
    Stores transactions and a hash reference to the previous block.
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            f'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )
    
    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data until a block hash
        is found that meets the leading 0's proof of work requirement.
        """
        from mining.proof_of_work import ProofOfWork

        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = ProofOfWork.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hash[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = ProofOfWork.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)
    
    @staticmethod
    def genesis():
        """
        Generate the genesis block.
        """
        return Block(
            timestamp=1,
            last_hash='genesis_last_hash',
            hash='genesis_hash',
            data=[],
            difficulty=3,
            nonce=0
        )