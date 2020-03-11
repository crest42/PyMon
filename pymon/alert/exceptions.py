from ..exceptions import PyMonError


class MissingAttributeError(PyMonError):

    def __init__(self, alert, attribute):
        super().__init__(f"Missing Attribute: '{attribute}' for '{alert}'")

class MissingAlertType(PyMonError):
    pass
class AlertTypeUnknown(PyMonError):
    pass
