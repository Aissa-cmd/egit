from typing import List, Tuple
from rich.console import Console
from rich.theme import Theme
from rich.text import Text

custom_theme = Theme({
    "info": "cyan",
    "verbose": "magenta",
    "warning": "yellow",
    "danger": "bold red"
})

class Console:
    console = Console(theme=custom_theme)

    @staticmethod
    def info(message: str):
        Console.console.print(message, style="info")

    @staticmethod
    def error(message: str):
        Console.console.print(message, style="danger")

    @staticmethod
    def rich_text(message_parts: List[Tuple[str, str]]):
        text = Text()
        for message, style in message_parts:
            text.append(message, style=style)
        Console.console.print(text)
