
import logging
from string import Template
from .alert import Alert
REPR = 'LoggerAlert'

TEMPLATE = Template("""
Monitoring Results for ${HOST}:
${RESULTS}
""")

class LoggerAlert(Alert):

    MANDATORY = []
    OPTIONAL = []

    def __init__(self, meta):
        super().__init__(meta, LoggerAlert.MANDATORY, optional=LoggerAlert.OPTIONAL)
        self.logger = logging.getLogger('LoggerAlert')
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)

    def _alert(self, result):
        message = TEMPLATE.substitute(HOST=result['HOST'], RESULTS=result['RESULTS'])
        self.logger.info(message)
