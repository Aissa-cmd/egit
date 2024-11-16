class HookException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PreHookException(HookException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PostHookException(HookException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
