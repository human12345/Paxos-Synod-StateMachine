# test_paxos_state_machine.py
import unittest
from axos_state_machine import PaxosStateMachine
from paxos_client import Client
from Synod_paxos import Acceptor
class TestPaxosStateMachine(unittest.TestCase):
    
    def setUp(self):
        self.acceptors = [Acceptor(i) for i in range(3)]
        # Passing the list of acceptors to the PaxosStateMachine
        self.psm = PaxosStateMachine(self.acceptors)
        self.client = Client('http://localhost:5000')
    
    def test_add_command(self):
        # Test adding a command to the Paxos State Machine
        command_num = self.client.add_command('test_command')
        self.assertIsNotNone(command_num, "Command number should not be None")
        self.assertIsInstance(command_num, int, "Command number should be an integer")
        
    def test_list_commands(self):
        # Test listing commands from the Paxos State Machine
        commands_list = self.client.list_commands()
        self.assertIsNotNone(commands_list, "Commands list should not be None")
        self.assertIsInstance(commands_list, list, "Commands list should be a list")
        for command in commands_list:
            self.assertIsInstance(command, tuple, "Command should be a tuple")
            self.assertEqual(len(command), 2, "Command should be a tuple with 2 elements")
            self.assertIsInstance(command[0], int, "First element of command should be an integer")
            self.assertIsInstance(command[1], str, "Second element of command should be a string")
        
if __name__ == '__main__':
    unittest.main()
