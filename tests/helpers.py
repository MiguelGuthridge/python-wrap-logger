class Simple:
    """Simple class for testing purposes"""
    def __init__(self) -> None:
        self.value = 42

    def __repr__(self) -> str:
        return 'simple'

    def __call__(
        self,
        *args: int,
        **kwargs: int,
    ) -> int:
        return sum(args) + sum(kwargs.values())

    def echo(self, value: str) -> str:
        return value
