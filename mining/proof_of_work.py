MINING_RATE = 4 * 1000 # 4 seconds in milliseconds

class ProofOfWork:
    """
    Implements the Proof of Work algorithim.
    """
    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to the MINING_RATE.
        Increase the difficulty for quickly mined blocks.
        Decrease the difficulty for slowly mined blocks.
        """
        if (new_timestamp - last_block.timestamp) < MINING_RATE:
            return last_block.difficulty + 1
        
        if (last_block.difficulty -1) > 0:
            return last_block.difficulty - 1
        
        return 1