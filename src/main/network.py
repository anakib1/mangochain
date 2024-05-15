from .models import Block
from typing import List


class Network:
    def __init__(self):
        self.blocks = []
        self.users = {}
        self.consumers = []

    def get_blocks(self) -> List[Block]:
        return self.blocks

    def add_consumer(self, consumer):
        self.consumers.append(consumer)

    def add_block(self, block):
        for consumer in self.consumers:
            consumer.on_block(block)
        self.blocks.append(block)

    def add_transaction(self, transaction):
        for consumer in self.consumers:
            consumer.on_transaction(transaction)

    def add_user(self, name, public_key):
        if name in self.users:
            raise Exception(f'User {name} already exists.')
        self.users[name] = public_key
