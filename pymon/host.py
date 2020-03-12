from .exceptions import (CheckAlreadyExists, MissingHostName,
                         MissingUserName)
from .ssh import Ssh
from .check.check import CheckResultList
import time
from .logging import logger

class HostCheckRelation:

    def __init__(self, host, check):
        self.host = host
        self.check = check
        self.result_list = []
        self.changed = 0
        self.last_result = time.time()

    def add(self, result):
        if len(self.result_list) >= self.check.cycles:
            self.result_list.pop(0)
        self.result_list.append(result)

    def get_last_result(self):
        return self.result_list[-1] if len(self.result_list) > 0 else None

    def run(self):
        delta = (time.time() - self.last_result)
        if delta > self.check.threshold:
            self.add(self.check.run(self.host))
            self.last_result = time.time()
        if len(self.result_list) == 1:
            logger.info(f"First State for {self.result_list[-1]}")
            self.changed = 0
        elif len(self.result_list) > 1:
            if self.result_list[-1] != self.result_list[-2]:
                logger.info(f"State of {self.result_list[-1]} changed")
                self.changed = 0
            else:
                self.changed += 1

    def __repr__(self):
        return f"'{self.get_last_result()}' since {self.changed} cycles"

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
                self.checks[k].run()
                check_result = self.checks[k].get_last_result()
                if check_result is not None:
                    if self.checks[k].changed == self.checks[k].check.cycles:
                        result['RESULTS'].add(self.checks[k])
            except KeyError as key_error:
                raise key_error
        return result
