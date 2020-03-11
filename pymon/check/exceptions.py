from ..exceptions import PyMonError

class MissingRemoteError(PyMonError):
    pass

class MissingAttributeError(PyMonError):

    def __init__(self, check, attribute):
        super().__init__(f"Missing Attribute: '{attribute}' for '{check}'")

class MissingHostEntry(PyMonError):
    pass
class MissingCheckParams(PyMonError):
    pass
class MissingCheckType(PyMonError):
    pass
class MissingExpectedValueError(PyMonError):
    pass
class CheckTypeUnknown(PyMonError):
    pass
