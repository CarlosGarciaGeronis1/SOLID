from solid.message_type import Message, Formatter


class Printer:

    @staticmethod
    def write_message(message: Message, formatter: Formatter):
        print(formatter.format(message))
