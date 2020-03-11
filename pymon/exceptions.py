class PyMonError(Exception):
    """Base class for exceptions in this module."""

class HostEntryNotValid(PyMonError):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, host):
        super().__init__()
        self.message = host


class CheckAlreadyExists(PyMonError):

    def __init__(self, check):
        super().__init__()
        self.message = f"A Check with name {check} already exists"

class MissingHostName(PyMonError):

    def __init__(self, check):
        super().__init__()
        self.message = check

class MissingUserName(PyMonError):

    def __init__(self, check):
        super().__init__()
        self.message = check
