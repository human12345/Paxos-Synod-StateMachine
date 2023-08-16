# paxos_state_machine.py
from Synod_paxos import Acceptor, Proposer, Learner
import threading

class PaxosStateMachine:
    def __init__(self, acceptors):
        self.acceptors = acceptors
        self.learner = Learner(acceptors)
        self.commands = []
        self.lock = threading.Lock()
    
    def add_command(self, value):
        with self.lock:
            proposer = Proposer(self.acceptors)
            while not proposer.propose(value):
                pass
            self.commands.append((len(self.commands), value))
            return len(self.commands) - 1

    def list_commands(self):
        with self.lock:
            return list(self.commands)
