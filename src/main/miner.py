from .models import Block, Transaction
from .network import Network
from typing import List, Tuple, Dict, Any
from .signature import verify_signature

MAX_TRANSACTIONS = 2
DIFFICULTY = 4

zeros_bytes = '0' * DIFFICULTY


class Miner:
    def __init__(self, network: Network):
        self.block = Block()
        self.network = network
        self.network.add_consumer(self)
        self.chain: Dict[Any, Tuple[int, Block]] = {}
        self.build_chain(network.get_blocks())
        self.main_chain: Tuple[int, Block] = (0, None)
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
            genesis = Block()
            genesis.balances = {'alice': 1000, 'bob': 1000}  # ToDo: CONFIGURE
            self.mine(genesis)
            self.chain[genesis.__hash__()] = (1, genesis)

    def on_transaction(self, transaction: Transaction):
        key = self.network.users.get(transaction.from_id, None)

        if key is None:
            print('Unknown sender.')
            return

        if not verify_signature(transaction.__hash__(), transaction.signature, key):
            print('Got invalid transaction. Signature does not match.')
            return

        chain: Block = self.main_chain[1]

        if transaction.amount < 0:
            print("Negative transactions are not allowed.")
            return

        if chain.balances.get(transaction.from_id, 0) < transaction.amount:
            print('Insufficient balance.')
            return

        self.block.transactions.append(transaction)
        self.block.balances[transaction.from_id] = self.block.balances.get(transaction.from_id, 0) + transaction.amount
        if len(self.block.transactions) >= MAX_TRANSACTIONS:
            self.block.previous_hash = self.main_chain[1].__hash__()
            self.mine(self.block)
            self.network.add_block(self.block)
            print('\nNode added new block to network. Block hash = ', self.block.__hash__())
            self.block = Block()

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
