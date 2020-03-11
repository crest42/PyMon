
import importlib
from .exceptions import CheckTypeUnknown, MissingCheckType

class CheckFactory:

    def __init__(self, check):
        if 'type' not in check:
            raise MissingCheckType(check)

        self.type = check['type']
        self.check = check

    def create(self):
        module_path = f'pymon.check.{self.type}'
        try:
            check = importlib.import_module(module_path)
            instance = getattr(check, check.REPR)
            return instance(self.check)
        except ModuleNotFoundError:
            raise CheckTypeUnknown(self.type)
        except Exception as exception:
            raise exception
