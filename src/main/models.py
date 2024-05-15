import json
from uuid import uuid4
from time import time as current_milli_time
import hashlib


class Transaction:
    def __init__(self, from_id, to_id, amount, tr_id=None):
        self.from_id = from_id
        self.to_id = to_id
        self.tr_id = str(uuid4()) if tr_id is None else tr_id
        self.amount = amount
        self.signature = None

    def __repr__(self):
        return json.dumps(
            {"transaction_id": self.tr_id, "from_id": self.from_id, "to_id": self.to_id, "amount": self.amount})

    def __hash__(self):
        return hashlib.sha256(str(self.__repr__()).encode()).hexdigest()

    def to_json(self):
        return {
            "from_id": self.from_id,
            "to_id": self.to_id,
            "tr_id": self.tr_id,
            "amount": self.amount,
            "signature": self.signature
        }

    @classmethod
    def from_json(cls, json_data):
        transaction = cls(json_data['from_id'], json_data['to_id'], json_data['amount'], json_data['tr_id'])
        transaction.signature = json_data['signature']
        return transaction


class Block:
    def __init__(self):
        self.timestamp = current_milli_time()
        self.transactions = []
        self.previous_hash: str = None
        self.balances = {}
        self.nonce = 0

    def to_json(self):
        return {
            "timestamp": self.timestamp,
            "transactions": [vars(tr) for tr in self.transactions],  # Serialize Transaction objects
            "previous_hash": self.previous_hash,
            "balances": self.balances,
            "nonce": self.nonce
        }

    @classmethod
    def from_json(cls, json_data):
        block = cls()
        block.timestamp = json_data["timestamp"]
        block.previous_hash = json_data["previous_hash"]
        block.balances = json_data["balances"]
        block.nonce = json_data["nonce"]
        # Deserialize Transaction objects
        for tr_data in json_data["transactions"]:
            tr = Transaction(tr_data["from_id"], tr_data["to_id"], tr_data["amount"], tr_data.get("tr_id"))
            block.transactions.append(tr)
        return block

    def __repr__(self):
        return json.dumps(self.to_json())

    def __hash__(self):
        return hashlib.sha256(str(self.__repr__()).encode()).hexdigest()
