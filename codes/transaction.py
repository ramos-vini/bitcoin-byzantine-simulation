# codes/transaction.py

import uuid

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f"TX({self.sender}->{self.receiver}, {self.amount})"
