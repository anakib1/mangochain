from .models import Transaction
from .network import Network
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from .signature import sign_message




class Client:
    def __init__(self, network: Network):
        self.network = network
        self.name = input('What is your name?\n>> ')
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.network.add_user(self.name, self.public_key)

    def add_transaction(self, to_id, amount):
        transaction = Transaction(self.name, to_id, amount)
        transaction.signature = sign_message(transaction.__hash__(), private_key=self.private_key)
        self.network.add_transaction(transaction)
