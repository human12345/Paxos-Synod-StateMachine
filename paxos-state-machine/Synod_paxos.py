import json
import os
import threading


class Acceptor:
    def __init__(self, id):
        self.id = id
        self.highest_proposal_number = -1
        self.highest_accepted_proposal = -1
        self.accepted_value = None
        self.lock = threading.Lock()
        self.load_state()

    def prepare(self, proposal_number):
        with self.lock:
            if proposal_number > self.highest_proposal_number:
                self.highest_proposal_number = proposal_number
                self.save_state()
                return self.highest_accepted_proposal, self.accepted_value
            else:
                return None, None

    def accept(self, proposal_number, value):
        with self.lock:
            if proposal_number >= self.highest_proposal_number:
                self.highest_proposal_number = proposal_number
                self.highest_accepted_proposal = proposal_number
                self.accepted_value = value
                self.save_state()
                return True
            else:
                return False

    def save_state(self):
        data = {
            'highest_proposal_number': self.highest_proposal_number,
            'highest_accepted_proposal': self.highest_accepted_proposal,
            'accepted_value': self.accepted_value
        }
        with open(f'acceptor_state_{self.id}.json', 'w') as f:
            json.dump(data, f)

    def load_state(self):
        try:
            with open(f'acceptor_state_{self.id}.json', 'r') as f:
                data = json.load(f)
                self.highest_proposal_number = data.get('highest_proposal_number', -1)
                self.highest_accepted_proposal = data.get('highest_accepted_proposal', -1)
                self.accepted_value = data.get('accepted_value', None)
        except FileNotFoundError:
            pass  # If the file does not exist, that's okay; we'll just stick with the initial state


class Proposer:
    def __init__(self, acceptors):
        self.acceptors = acceptors
        self.proposal_number = 0
        self.value = None

    def propose(self, value):
        self.proposal_number += 1
        self.value = value

        responses = [acceptor.prepare(self.proposal_number) for acceptor in self.acceptors]
        valid_responses = [(proposal, value) for proposal, value in responses if proposal is not None]

        if valid_responses:
            highest_accepted_proposal, accepted_value = max(valid_responses)
            if highest_accepted_proposal is not None:
                self.value = accepted_value

        responses = [acceptor.accept(self.proposal_number, self.value) for acceptor in self.acceptors]
        if responses.count(True) > len(self.acceptors) / 2:
            return True
        else:
            return False


class Learner:
    def __init__(self, acceptors):
        self.acceptors = acceptors

    def learn(self):
        responses = [acceptor.accepted_value for acceptor in self.acceptors]
        if responses.count(None) < len(self.acceptors) / 2:
            return max(set(responses), key=responses.count)
        else:
            return None


class Proposer:
    def __init__(self, acceptors):
        self.acceptors = acceptors
        self.proposal_number = 0
        self.value = None

    def propose(self, value):
        self.proposal_number += 1
        self.value = value

        responses = [acceptor.prepare(self.proposal_number) for acceptor in self.acceptors]
        valid_responses = [(proposal, value) for proposal, value in responses if proposal is not None]

        if valid_responses:
            highest_accepted_proposal, accepted_value = max(valid_responses)
            if highest_accepted_proposal is not None:
                self.value = accepted_value

        responses = [acceptor.accept(self.proposal_number, self.value) for acceptor in self.acceptors]
        if responses.count(True) > len(self.acceptors) / 2:
            return True
        else:
            return False


class Learner:
    def __init__(self, acceptors):
        self.acceptors = acceptors

    def learn(self):
        responses = [acceptor.accepted_value for acceptor in self.acceptors]
        if responses.count(None) < len(self.acceptors) / 2:
            return max(set(responses), key=responses.count)
        else:
            return None
