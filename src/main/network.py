from .models import Block, Transaction
from typing import List
import requests
import json


class CentralClient:
    def __init__(self, url, port):
        self.url = f"http://{url}:{port}/api"

    def get_blocks(self):

        response = requests.get(self.url + "/blocks")

        if response.status_code == 200:
            blocks = response.json()  # Convert JSON response to Python list
            ret = []
            for x in blocks:
                try:
                    ret.append(Block.from_json(json.loads(x)))
                except Exception as ex:
                    print('Broken block. Ex = ', ex)
            return ret
        else:
            print(f"Error: {response.status_code} - {response.reason}")

    def get_transactions(self):

        response = requests.get(self.url + "/transactions")

        if response.status_code == 200:
            transactions = response.json()  # Convert JSON response to Python list
            ret = []
            for x in transactions:
                try:
                    ret.append(Transaction.from_json(json.loads(x)))
                except Exception as ex:
                    print('Broken transaction. Ex = ', ex)
            return ret
        else:
            print(f"Error: {response.status_code} - {response.reason}")

    def get_users(self):
        response = requests.get(self.url + "/users")
        if response.status_code == 200:
            users = response.json()
            ret = {}
            for x in users:
                try:
                    ret.update({x['userName']: x['signature']})
                except Exception as ex:
                    print('Broken users. Ex = ', ex)

            return ret
        else:
            print(f"Error: {response.status_code} - {response.reason}")

    def add_user(self, username, signature):
        return requests.post(self.url, json=json.dumps({'userName': username, "signature": signature}))

    def add_block(self, block):
        return requests.post(self.url, json=block.__repr__())

    def add_transaction(self, transaction):
        return requests.post(self.url, json=json.dumps(transaction.to_json()))


class Network:
    def __init__(self, url='127.0.0.1', port=8000):
        self.client = CentralClient(url, port)
        self.blocks = self.client.get_blocks()
        self.users = self.client.get_users()
        self.consumers = []

    def get_blocks(self) -> List[Block]:
        return self.blocks

    def add_consumer(self, consumer):
        self.consumers.append(consumer)

    def add_block(self, block):
        self.client.add_block(block)
        for consumer in self.consumers:
            consumer.on_block(block)
        self.blocks.append(block)

    def add_transaction(self, transaction):
        self.client.add_transaction(transaction)
        for consumer in self.consumers:
            consumer.on_transaction(transaction)

    def add_user(self, name, public_key):
        self.client.add_user(name, public_key)
        if name in self.users:
            raise Exception(f'User {name} already exists.')
        self.users[name] = public_key
