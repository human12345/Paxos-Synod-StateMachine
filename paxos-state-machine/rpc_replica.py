# replica.py
from flask import Flask, request
from paxos_state_machine import PaxosStateMachine
from Synod_paxos import Acceptor

app = Flask(__name__)
acceptors = [Acceptor(i) for i in range(3)]  # Change this to match the number of acceptors in your system
state_machine = PaxosStateMachine(acceptors)

@app.route('/add_command', methods=['POST'])
def add_command():
    value = request.json['value']
    command_num = state_machine.add_command(value)
    return {'command_num': command_num}

@app.route('/list_commands', methods=['GET'])
def list_commands():
    commands = state_machine.list_commands()
    return {'commands': commands}

if __name__ == '__main__':
    app.run(port=5000)  # Change this to set the port your replica server should listen on
