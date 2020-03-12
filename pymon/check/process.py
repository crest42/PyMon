from .check import RemoteCheck
from .exceptions import MissingExpectedValueError

REPR = 'CheckProcess'

class CheckProcess(RemoteCheck):

    MANDATORY = ['pid_file']

    PS_FLAGS = {'pid': '-opid',
            'ppid': '-oppid',
            'cpu': '-ocpu',
            'cmd': '-ocmd',
            'comm ': '-ocomm',
            'cputime': '-ocputime',
            'user': '-ouser',
            'uid': '-oeuid',
            'group': '-ogroup',
            'gid': '-ogid',
            'times': '-oetimes',
            }
    def __init__(self, check):
        self.pid_file = None
        super().__init__(check, self.MANDATORY)

    def __repr__(self):
        return f"Check Process pid_file: {self.pid_file}"

    def _parse_proc_output(self, output):
        return_dict = {}
        lines = output.split('\n')
        for line in lines:
            k = line.split()
            value = ''
            for elem in k[1:]:
                value += f'{elem} '
            return_dict[k[0][:-1]] = value.strip()
        return return_dict 

    def __get_pid_file_cmd(self):
        return f"cat {self.pid_file}"

    def __parse_pid_file(self, pid_file):
        if pid_file.isnumeric():
            return int(pid_file)
        else:
            return -1

    def get_command(self):
        return f'cat /proc/{self.pid}/status'

    def execute(self, remote):
        check_result = self.execute_command(remote, self.__get_pid_file_cmd())
        if check_result.return_code != 0:
            check_result.add_result(check_result.stderr)
            check_result.set(-1,"Unable to read pid file: {check_result.stderr}")
        else:
            check_result.add_result(check_result.stdout)
            pid = self.__parse_pid_file(check_result.stdout)
            if pid < 1:
                check_result.set(-1,"Unable to parse pid file: {check_result.stdout}")
                return check_result            
            self.pid = pid

        check_result = super().execute(remote)
        if check_result.return_code == 0:
            if check_result.stdout is not None:
                try:
                    check_result.add_result(self._parse_proc_output(check_result.stdout))
                    check_result.set(0,check_result.result)
                    if self.expect is not None:
                        for k in self.expect:
                            if k not in check_result.result:
                                check_result.set(-1,f"Missing expected value in result: {MissingExpectedValueError(k)}")
                            elif check_result.result[k] != self.expect[k]:
                                check_result.set(1, f'{k}: {check_result.result[k]} != {self.expect[k]}')   
                except Exception as exception:
                    check_result.set(-1,f"command returned 0 but no output available: '{exception}'")
        else:
            check_result.set(2,f"Error command returned '{check_result.stderr}'")

        return check_result
