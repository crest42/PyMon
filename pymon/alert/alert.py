from .exceptions import MissingAttributeError

class Alert:

    def __init__(self, alert, mandatory, optional=None):
        if 'enabled' not in alert:
            self.enabled = True
        else:
            self.enabled = alert['enabled']

        for attr in mandatory:
            if attr not in alert['params']:
                raise MissingAttributeError(self, attr)
            setattr(self, attr, alert['params'][attr])

        if optional is not None:
            for attr in optional:
                if attr in alert['params']:
                    setattr(self, attr, alert['params'][attr])
                else:
                    setattr(self, attr, None)

    def _alert(self, result):
        print(result)

    def send(self, message):
        if self.enabled:
            self._alert(message)
