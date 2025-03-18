from blockchain.block import Block

class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions.
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        """
        Mine a block and add it to the chain.
        """
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if the following rules apply:
            - The incoming chain is longer than the local one.
            - The incoming chain is formatted properly.
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer.')
        
        try:
            self.validate_chain(chain)
            self.chain = chain
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chanin is invalid: {e}')
        
    def validate_chain(self, chain):
        """
        Validate the incoming chain.
        Enforce the following rules:
            - The chain must start with the genesis block
            - Blocks must be formatted correctly
        """
        if chain[0].__dict__ != Block.genesis().__dict__:
            raise Exception('The genesis blokc must be valid')
        
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]

            if block.last_hash != last_block.hash:
                raise Exception('The block last_hash must be correct')
            
            if block.hash[0:block.difficulty] != '0' * block.difficulty:
                raise Exception('The proof of work requirement was not met')
            
    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return list(map(lambda block: block.__dict__, self.chain))