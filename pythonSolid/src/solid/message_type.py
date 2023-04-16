import abc
from datetime import datetime


class Message(abc.ABC):

    def __init__(self, msg: str):
        self.msg = msg
        self.time = datetime.now()


class Formatter(abc.ABC):

    @abc.abstractmethod
    def format(self, message: Message):
        raise Exception("I am an interface")


class TextFormatter(Formatter):

    def format(self, message: Message):
        return f"{message.msg} - {message.time.isoformat()}"