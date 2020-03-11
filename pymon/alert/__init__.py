
import importlib
from .exceptions import AlertTypeUnknown, MissingAlertType

class AlertFactory:

    def __init__(self, alert):
        if 'type' not in alert:
            raise MissingAlertType(alert)

        self.type = alert['type']
        self.meta = alert

    def create(self):
        module_path = f'pymon.alert.{self.type}'
        try:
            print(module_path)
            alert = importlib.import_module(module_path)
            instance = getattr(alert, alert.REPR)
            return instance(self.meta)
        except ModuleNotFoundError:
            raise AlertTypeUnknown(self.type)
        except Exception as exception:
            raise exception
