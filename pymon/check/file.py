from .check import RemoteCheck
from .exceptions import MissingExpectedValueError

REPR = 'CheckFile'

class CheckFile(RemoteCheck):

    MANDATORY = ['filename']

    STAT_FLAGS = {'access_rights':  r'%a',
                  'blocks_num':     r'%b',
                  'byte_per_block': r'%B',
                  'dev_num':        r'%d',
                  'type':           r'%F',
                  'gid':            r'%g',
                  'group':          r'%G',
                  'link_refcount':  r'%h',
                  'inode':          r'%i',
                  'mount':          r'%m',
                  'name':           r'%n',
                  'size':           r'%s',
                  'uid':            r'%u',
                  'owner':          r'%U',
                  'create_time':    r'%W',
                  'access_time':    r'%X',
                  'mod_time':       r'%Y',
                 }

    def __init__(self, check):
        self.filename = None
        self.seperator = ','
        super().__init__(check, self.MANDATORY)

    def __repr__(self):
        return f"Check File filename: {self.filename}"

    def __parse_stat_output(self, output):
        return dict(item.split("=") for item in output.split(self.seperator)) if output is not None else None

    def execute(self, remote):
        check_result = super().execute(remote)
        if check_result.return_code == 0:
            if check_result.stdout is not None:
                try:
                    check_result.add_result(self.__parse_stat_output(check_result.stdout))
                    check_result.set(0,check_result.result)
                    if self.expect is not None:
                        for k in self.expect:
                            if k not in check_result.result:
                                check_result.set(-1,f"Missing expected value in result: {MissingExpectedValueError(k)}")
                            if check_result.result[k] != self.expect[k]:
                                check_result.set(1, f'{k}: {check_result.result[k]} != {self.expect[k]}')   
                except Exception as e:
                    check_result.set(-1,f'stat command returned 0 but no output available: {e}')
        else:
            check_result.set(2,f'Error stat command returned {check_result.stderr}')

        return check_result

    def get_command(self):
        format_string = '-c'
        for k in CheckFile.STAT_FLAGS:
            format_string += f'{k}={CheckFile.STAT_FLAGS[k]}{self.seperator}'
        return f'stat {self.filename} {format_string[:-1]}'
