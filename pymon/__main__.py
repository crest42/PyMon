from .pymon import PyMon
from .config import Config

CONFIG = Config()

PY_MON = PyMon(CONFIG.host_list, CONFIG.check_list, CONFIG.alert_list)
