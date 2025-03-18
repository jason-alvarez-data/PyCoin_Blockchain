import json
import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

class Wallet:
    """
    Individual wallet for a miner.
    Keeps track of the miner's balance.
    Allows a miner to authorize transactions.
    """
    def __init__(self):
        self.address = str(uuid.uuid4())
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),
            default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()

    def sign(self, data):
        """
        Generate a signature based on the data using the local private key.
        """
        encoded_data = json.dumps(data, sort_keys=True).encode('utf-8')

        return self.private_key.sign(
            encoded_data,
            ec.ECDSA(hashes.SHA256())
        ).hex()
    
    def serialize_public_key(self):
        """
        Reset the public key to its serialized version.
        """
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the original public key and data.
        """
        try:
            public_key_bytes = serialization.load_pem_public_key(
                public_key.encode('utf-8'),
                default_backend()
            )

            encode_data = json.dumps(data, sort_keys=True).encode('utf-8')

            public_key_bytes.verify(
                bytes.fromhex(signature),
                encoded_data,
                ec.ECDSA(hashes.SHA256())
            )

            return True
        except InvalidSignature:
            return False