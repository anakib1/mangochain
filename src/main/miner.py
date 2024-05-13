from .models import Block, Transaction
from .network import Network
from typing import List

MAX_TRANSACTIONS = 2
DIFFICULTY = 4

zeros_bytes = '0' * DIFFICULTY


class Miner:
    def __init__(self, network: Network):
        self.transactions = []
        self.network = network
        self.network.add_consumer(self)
        self.chain = {}
        self.build_chain(network.get_blocks())
        self.main_chain = (0, None)
        for cnt, chain in self.chain.values():
            if self.main_chain[0] < cnt:
                self.main_chain = (cnt, chain)

    def build_chain(self, blocks: List[Block]):
        blocks = sorted(blocks, key=lambda x: x.timestamp)
        self.chain = {}
        for block in blocks:
            if block.__hash__()[:DIFFICULTY] != zeros_bytes:
                continue

            cnt, prev = self.chain.get(block.previous_hash, (0, None))
            self.chain[block.__hash__()] = (cnt + 1, block)

        if len(self.chain.values()) == 0:
            print('Chain is empty. Building genesis.')
            genesis = Block(None, [])
            self.mine(genesis)
            self.chain[genesis.__hash__()] = (1, genesis)

    def on_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        if len(self.transactions) >= MAX_TRANSACTIONS:
            block = Block(self.main_chain[1], self.transactions)
            self.mine(block)
            self.network.add_block(block)
            print('\nNode added new block to network. Block hash = ', block.__hash__())
            self.transactions = []

    def on_block(self, block: Block):
        block_hash = block.__hash__()
        if block_hash[:DIFFICULTY] != zeros_bytes:
            print('\nNetwork node received invalid block. Hash is invalid.')
        else:
            this_cnt, this_chain = self.chain.get(block.previous_hash, (0, None))
            if this_chain is None:
                print('\nNetwork node received invalid block. Previous block not found.')
                return
            self.chain[block.__hash__()] = (this_cnt + 1, block)
            if this_cnt + 1 > self.main_chain[0]:
                self.main_chain = self.chain[block.__hash__()]

    def mine(self, block: Block) -> None:
        while True:
            block.nonce += 1
            block_hash = block.__hash__()
            if block_hash[:DIFFICULTY] == zeros_bytes:
                return
