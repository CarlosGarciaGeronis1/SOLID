from solid.message_type import Message, TextFormatter
from solid.message_printer import Printer


def main():
    message = Message("Hello world!")
    formatter = TextFormatter()

    Printer.write_message(message, formatter)


if __name__ == '__main__':
    main()

