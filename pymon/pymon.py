import logging
from .exceptions import HostEntryNotValid
from .check import CheckFactory
from .alert import AlertFactory
from .host import Host

class PyMon:

    def __init__(self, host_list, check_list, alert_list):
        self.hosts = {}
        self.checks = []
        self.alerts = []
        self.logger = logging.getLogger('PyMon')
        for host in host_list:
            if 'name' not in host:
                raise HostEntryNotValid(host)
            name = host['name']
            self.hosts[name] = Host(host['name'], host)

        for check in check_list:
            self.checks.append(CheckFactory(check).create())
            self.add_check(self.checks[-1])

        for alert in alert_list:
            self.alerts.append(AlertFactory(alert).create())

    def add_check(self, check):
        for host in check.hosts:
            try:
                self.add_check_to_host(host, check)
            except HostEntryNotValid:
                self.logger.warn(f"Host entry {host} unknown")
            except Exception:
                raise

    def add_check_to_host(self, check_host, check):
        if check_host not in self.hosts:
            raise HostEntryNotValid(check_host)
        self.hosts[check_host].add(check)

    def print_hosts(self):
        print("Hostlist:")
        for k in self.hosts:
            print(self.hosts[k])
        print()

    def run(self):
        print("Run:")
        for k in self.hosts:
            result = self.hosts[k].run()
            for alert in self.alerts:
                alert.send(result)
