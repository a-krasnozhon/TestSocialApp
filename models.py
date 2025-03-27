from collections import deque
from datetime import datetime

from utils import get_human_time


DB = {
    'USER': {},
    'POST': {},
}


class Post:
    def __init__(self, content: str, username: str):
        self.content = content
        self.username = username
        self.created_at = datetime.now()

    def __repr__(self):
        return f'{self.username} - {self.content} ({get_human_time(self.created_at)} ago)'

    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        return self.created_at < other.created_at


class User:
    def __init__(self, username: str):
        self.username = username
        self.follows = set()

    def __hash__(self):
        return hash(self.username)

    def __eq__(self, other):
        return self.username == other.username

    def follow(self, user):
        if self != user:
            self.follows.add(user.username)

    def unfollow(self, user):
        self.follows.discard(user)

    def create_post(self, post: Post):
        if post.username in DB['POST']:
            DB['POST'][post.username].appendleft(post)
        else:
            DB['POST'][post.username] = deque([post])

    def __repr__(self):
        return str(self.__dict__)
