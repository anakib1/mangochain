from src.main.network import Network
from src.main.miner import Miner
from src.main.client import Client

import threading
import queue


class ConsoleListener(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            line = input("Enter a command: ")
            self.queue.put(line)


class LineProcessor(threading.Thread):
    def __init__(self, queue, client:Client):
        threading.Thread.__init__(self)
        self.queue = queue
        self.client = client

    def run(self):
        while True:
            line = self.queue.get()
            try:
                self.on_line(line)
            except Exception as ex:
                print('Could not process command. Ex = ', ex)

    def on_line(self, line: str):
        from_id, to_id, amount = line.split()
        amount = float(amount)
        self.client.add_transaction(from_id, to_id, amount)



if __name__ == "__main__":
    q = queue.Queue()
    network = Network()
    miner = Miner(network)
    client = Client(network)
    console_listener = ConsoleListener(q)
    line_processor = LineProcessor(q, client)

    console_listener.start()
    line_processor.start()

    console_listener.join()
    line_processor.join()