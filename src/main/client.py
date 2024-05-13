from .models import Transaction
from .network import Network


class Client:
    def __init__(self, network: Network):
        self.network = network

    def add_transaction(self, from_id, to_id, amount):
        self.network.add_transaction(Transaction(from_id, to_id, amount))
