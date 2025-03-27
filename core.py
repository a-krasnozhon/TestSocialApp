from actions import AVAILABLE_COMMANDS

from models import DB, User


class Request:
    def __init__(self, username: str, command: str, content: str):
        self.user = self._check_user_in_db(username)
        self.command = command
        self.content = content

    def _check_user_in_db(self, username):
        if username in DB['USER']:
            return DB['USER'][username]

        new_user = User(username=username)
        DB['USER'][username] = new_user
        return new_user


def _validate_command(cmd):
    if cmd not in AVAILABLE_COMMANDS:
        raise ValueError('Invalid command')

def parse_commandline(command: str):
    username = command
    cmd = ''
    content = ''

    for i, c in enumerate(command):
        if c == ' ':
            username = command[:i]
            command = command[i:].strip()
            cmd = command
            break

    for i, c in enumerate(command):
        if c == ' ':
            cmd = command[:i]
            content = command[i:].strip()
            break

    _validate_command(cmd)

    return Request(*(username, cmd, content))


def execute_request(command):
    request = parse_commandline(command)
    return AVAILABLE_COMMANDS[request.command](request)
