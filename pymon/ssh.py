import select
import paramiko

class Ssh:

    def __init__(self, host):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostname = host.get_real_hostname()
        self.username = host.username
        self.password = host.password
        self.key_file = host.key_file
        self.port = 22
        self.timeout = 5

    def connect(self):
        self.client.connect(self.hostname, self.port, self.username, self.password, self.key_file, timeout=self.timeout)

    def exec(self, command):
        """Executes a command via ssh"""
        out_str = None
        err_str = None
        chan = self.client.get_transport().open_session()
        chan.exec_command(command)
        return_code = -1
        return_code = chan.recv_exit_status()
        if chan.recv_ready():
            read_list, _, _ = select.select([chan], [], [], 0.0)
            if len(read_list) > 0:
                out_str = chan.recv(-1).decode('utf-8')
        if chan.recv_stderr_ready():
            read_list, _, _ = select.select([chan], [], [], 0.0)
            if len(read_list) > 0:
                err_str = chan.recv_stderr(1024).decode('utf-8')
        return (return_code, out_str, err_str)

    def disconnect(self):
        self.client.close()
