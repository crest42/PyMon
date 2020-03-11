from .exceptions import (MissingHostEntry, MissingCheckParams,
                         MissingAttributeError, MissingRemoteError,
                         CheckTypeUnknown)
from ..ssh import Ssh
from socket import timeout

class CheckResultList:

    def __init__(self):
        self.list = []

    def add(self, check_result):
        self.list.append(check_result)

    def to_string(self):
        string = ''
        for check_result in self.list:
            string += str(check_result) + '\n'
        return string

    def __repr__(self):
        return self.to_string()

class CheckResult:

    def __init__(self, check, rc, stdout=None, stderr=None, state=None, output=''):
        self.check = check
        self.return_code = rc
        self.stderr = stderr
        self.stdout = stdout
        self.result = None
        self.state = state
        self.output = output

    def __repr__(self):
        state = 'OK'
        if self.state is None:
            state = 'Unknown'
        elif self.state == 0:
            pass
        elif self.state == 1:
            state = 'Warning'
        elif self.state == 2:
            state = 'Error'
        else:
            state = 'Unknown'

        return f"{self.check} state: {state}, output: '{self.output}'"

    def add_result(self, result):
        self.result = result

    def set(self, state, output):
        self.state = state
        self.output = output

class Check:

    def __init__(self, check, mandatory, optional=None):
        if 'name' not in check:
            raise MissingAttributeError('name', check)
        self.name = check['name']

        self.expect = None

        if 'hosts' not in check:
            raise MissingHostEntry(check)

        if 'params' not in check:
            raise MissingCheckParams(check)

        if 'expect' in check:
            self.expect = check['expect']

        self.hosts = check['hosts']
        self.params = check['params']
        for attr in mandatory:
            if attr not in check['params']:
                raise MissingAttributeError(self, attr)
            setattr(self, attr, check['params'][attr])

        if optional is not None:
            for attr in optional:
                if attr in check['params']:
                    setattr(self, attr, check['params'][attr])
                else:
                    setattr(self, attr, None)

    def __repr__(self):
        return 'CHECK REPR NYI'

    def __str__(self):
        return self.__repr__()

    def get_command(self):
        return f'/bin/true {self}'

    def _run(self, host):
        raise CheckTypeUnknown()

    def run(self, host):
        return self._run(host)

class RemoteCheck(Check):
    TYPE = 'remote'

    def __init__(self, check, mandatory, optional=None):
        self.type = RemoteCheck.TYPE
        super().__init__(check, mandatory, optional)

    def execute(self, remote):
        if remote is None:
            raise MissingRemoteError()
        return_code, stdout, stderr = remote.exec(self.get_command())
        return CheckResult(self, return_code, stdout, stderr)

    def _run(self, host):
        remote = Ssh(host)
        try:
            remote.connect()
        except timeout:
            return CheckResult(self, -1, state=2, output='Timeout on ssh connect')
        except Exception:
            raise

        res = self.execute(remote)
        remote.disconnect()
        return res

class LocalCheck(Check):
    TYPE = 'local'

    def __init__(self, check, mandatory, optional=None):
        self.type = LocalCheck.TYPE
        super().__init__(check, mandatory, optional)

    def execute(self, remote):
        res = CheckResult(self, 1, remote.get_real_hostname(), 'NYI')
        res.set(-1, f'Check {self} is NYI')
        return res

    def _run(self, host):
        return self.execute(host)
