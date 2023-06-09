class EnvironmentVariableNotFoundError(KeyError):
    """A more descriptive error for KeyError when environment variable is not found"""

    def __init__(self, missing_key) -> None:
        self.value = f"Please make sure you have the environment variable: {missing_key} configured"

    def __str__(self) -> str:
        return repr(self.value)
