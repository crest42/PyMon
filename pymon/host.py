from .exceptions import (CheckAlreadyExists, MissingHostName,
                         MissingUserName)
from .ssh import Ssh
from .check.check import CheckResultList

class HostCheckRelation:

    def __init__(self, host, check):
        self.host = host,
        self.check = check
        self.last_result = None

    def __repr__(self):
        return f"'{self.last_result}'"

class Host:

    def __init__(self, name, host):
        self.checks = {}
        self.name = name
        self.username = None
        self.password = None
        self.key_file = None
        self.addr = None
        if 'name' not in host:
            raise MissingHostName(host)
        self.name = host['name']

        if 'username' not in host:
            raise MissingUserName(host)
        self.username = host['username']

        if 'password' in host:
            self.password = host['password']

        if 'key' in host:
            self.key_file = host['key']

        if 'addr' in host:
            self.addr = host['addr']

    def __repr__(self):
        if self.addr is not None:
            return f"{self.name}({self.addr})"
        else:
            return f"{self.name}"

    def get_real_hostname(self):
        if self.addr is not None:
            return self.addr
        else:
            return self.name

    def add(self, check):
        relation = HostCheckRelation(self, check)
        if check in self.checks:
            CheckAlreadyExists(check)
        self.checks[check] = relation

    def run(self):
        result = {'HOST': self,
                  'RESULTS': CheckResultList()}
        for k in self.checks:
            try:
                self.checks[k].last_result = self.checks[k].check.run(self)
                result['RESULTS'].add(self.checks[k].last_result)
            except KeyError as key_error:
                raise key_error
        return result
