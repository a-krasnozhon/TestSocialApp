from typing import Any


class Response:
    def __init__(self, content: Any, multiple: bool = False):
        self.content = content
        self.multiple = multiple

    def __repr__(self):
        if self.multiple:
            return '\n'.join(self.content)
        return self.content

    def __str__(self):
        return self.__repr__()
