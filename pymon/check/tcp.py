import socket
from .check import LocalCheck, CheckResult

REPR = 'CheckTcp'

class CheckTcp(LocalCheck):

    MANDATORY = ['port']
    OPTIONAL = ['timeout']

    def __init__(self, check):
        self.port = None
        self.sock = None
        self.timeout = None
        super().__init__(check, CheckTcp.MANDATORY)
        if self.timeout is None:
            self.timeout = 5

    def execute(self, remote):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        res = CheckResult(self, 0)
        try:
            self.sock.connect((remote.get_real_hostname(), self.port))
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            res.set(0, f"Connection to Port {self.port} successfull")
        except socket.timeout:
            res.set(2, "Timeout on TCP connect")
        except socket.error as exception:
            res.set(2, exception)
        except Exception as exception: #pylint: disable=broad-except
            res.set(-1, exception)

        return res

    def __repr__(self):
        return f"{self.name}: Check TCP port {self.port}"
