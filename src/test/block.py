import unittest
from ..main.models import Block, Transaction
import json


class MyTestCase(unittest.TestCase):
    def test_something(self):
        block = Block()
        block.transactions = [Transaction('alice', 'bob', 10), Transaction('bob', 'alice', 10)]
        hash_code = block.__hash__()

        block2 = block.from_json(json.loads(json.dumps(block.to_json())))
        hash_code_2 = block2.__hash__()
        self.assertEqual(hash_code, hash_code_2)  # add assertion here


if __name__ == '__main__':
    unittest.main()
