import uuid
import time

class Transaction:
    """
    Document of a exchange in currency from a sender to one or more recipients.
    """
    def __init__(self, sender_wallet, recipient, amount, id=None):
        self.sender_wallet = sender_wallet
        self.recipient = recipient
        self.amount = amount
        self.id = id or str(uuid.uuid4())
        self.timestamp = time.time_ns()
        self.signature = None

    def __repr__(self):
        return (
            f'Transaction('
            f'sender_wallet: {self.sender_wallet.address}, '
            f'recipient: {self.recipient}, '
            f'amount: {self.amount}, '
            f'id: {self.id})'
        )
    
    def to_json(self):
        """
        Serialize the transaction.
        """
        return {
            'sender_wallet': self.sender_wallet.address,
            'recipient': self.recipient,
            'amount': self.amount,
            'id': self.id,
            'timestamp': self.timestamp,
            'signature': self.signature
        }
    
    def sign(self):
        """
        Sign the transaction with the sender's wallet.
        """
        self.signature = self.sender_wallet.sign(
            self.to_json()
        )

    def verify(self):
        """
        Verify the transaction signature.
        """
        from blockchain.wallet import Wallet

        return Wallet.verify(
            self.sender_wallet.address,
            self.to_json(),
            self.signature
        )