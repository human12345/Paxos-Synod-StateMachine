# pxos_client.py
import requests

class Client:
    def __init__(self, url):
        self.url = url

    def add_command(self, value):
        response = requests.post(f"{self.url}/add_command", json={'value': value})
        if response.status_code == 200:
            return response.json()['command_num']
        else:
            print(f"Error: {response.text}")
            return None

    def list_commands(self):
        response = requests.get(f"{self.url}/list_commands")
        if response.status_code == 200:
            commands = response.json()['commands']
            return [tuple(command) for command in commands]
        else:
            print(f"Error: {response.text}")
            return None


if __name__ == "__main__":
    client = Client("http://localhost:5000")

