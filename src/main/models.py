from datetime import datetime
from uuid import uuid4
import hashlib
import json
import time


def current_milli_time():
    return round(time.time() * 1000)


class Transaction:
    def __init__(self, from_id, to_id, amount):
        self.from_id = from_id
        self.to_id = to_id
        self.tr_id = uuid4()
        self.amount = amount

    def __repr__(self):
        return json.dumps(
            {"transaction_id": str(self.tr_id), "from_id": self.from_id, "to_id": self.to_id, "amount": self.amount})


class Block:
    def __init__(self, previous_block, transactions):
        self.timestamp = current_milli_time()
        self.transactions = transactions
        self.previous_hash: str = previous_block.__hash__() if previous_block is not None else None
        self.nonce = 0
    def __repr__(self):
        return json.dumps({"transactions": [x.__repr__() for x in self.transactions],
                           "previous_hash": self.previous_hash, "nonce": self.nonce, "block_time": self.timestamp})

    def __hash__(self):
        return hashlib.sha256(str(self.__repr__()).encode()).hexdigest()
