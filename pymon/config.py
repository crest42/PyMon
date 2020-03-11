import os
import yaml

ETC_DIR = '/etc/pymon'

class NoConfigAvailable(Exception):
    pass

class Config:

    def __init__(self):
        self.etcd = ETC_DIR
        self.homed = os.path.expanduser("~/pymon")
        self.cwd = os.getcwd()
        self.host_list = self.load_host_config()
        self.alert_list = self.load_alert_config()
        self.check_list = self.load_check_config()

    def _get_config_file(self, config):
        etc = f'{self.etcd}/{config}'
        home = f'{self.homed}/{config}'
        cwd = f'{self.cwd}/{config}'
        if os.path.isfile(cwd):
            return open(cwd, 'r')
        elif os.path.isfile(home):
            return open(home, 'r')
        elif os.path.isfile(etc):
            return open(etc, 'r')
        else:
            raise NoConfigAvailable()

    def load_host_config(self, name='hosts.yml'):
        config_file = self._get_config_file(name)
        return yaml.load(config_file, Loader=yaml.Loader)

    def load_check_config(self, name='checks.yml'):
        config_file = self._get_config_file(name)
        return yaml.load(config_file, Loader=yaml.Loader)

    def load_alert_config(self, name='alert.yml'):
        config_file = self._get_config_file(name)
        return yaml.load(config_file, Loader=yaml.Loader)
