from typing import List, Tuple
from rich.prompt import Prompt
from egit.utils import ArgvOptions
from egit.console import Console


class Runner:
    def __init__(self, args: ArgvOptions):
        self.args = args
        self._Console = Console
        self.console = self._Console.console

    def verbose(self, message: str):
        if self.args.egit_args.verbose:
            self.console.print(message, style="verbose")

    def interactive(self, message: str, default: str | None = None, choices: List[str] | None = None):
        if self.args.egit_args.interactive:
            return Prompt.ask(
                message,
                default=default,
                choices=choices,
                case_sensitive=False,
                show_choices=True,
                show_default=True,
            )
        else:
            return default
    
    def ask(self, message: str, default: str, choices: List[str] | None):
        return Prompt.ask(
            message,
            default=default,
            choices=choices,
            case_sensitive=False,
            show_choices=True,
            show_default=True,
        )
        
    def info(self, message: str):
        self.console.print(message, style="info")

    def warning(self, message: str):
        self.console.print(message, style="warning")

    def error(self, message: str):
        self.console.print(message, style="danger")

    def rich_text(self, message_parts: List[Tuple[str, str]]):
        self._Console.rich_text(message_parts)
