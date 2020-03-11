
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from .alert import Alert
REPR = 'MailAlert'

TO = [
        [
            'robin',
        ],
        [
            'robin@chilio.net',
        ]
    ]

SUBJECT_TEMPLATE = Template("Monitoring Results for ${HOST}")
BODY_TEMPLATE = Template("""

Dear ${PERSON_NAME}, 

Monitoring Results:

${RESULTS}

Yours Truly
Pymon
""")

class MailAlert(Alert):

    MANDATORY = ['hostname', 'port', 'username', 'password']
    OPTIONAL = ['starttls']
    def __init__(self, meta):
        self.hostname = None
        self.port = None
        self.starttls = None
        self.username = None
        self.password = None
        super().__init__(meta, MailAlert.MANDATORY, optional=MailAlert.OPTIONAL)
        self.smtp = smtplib.SMTP(host=self.hostname, port=self.port)
        if self.starttls:
            self.smtp.starttls()
        self.smtp.login(self.username, self.password)

    def _alert(self, result):
        for name, email in zip(TO[0], TO[1]):
            msg = MIMEMultipart()
            message = BODY_TEMPLATE.substitute(PERSON_NAME=name.title(), RESULTS=result['RESULTS'])
            subject = SUBJECT_TEMPLATE.substitute(HOST=result['HOST'])
            # setup the parameters of the message
            msg['From'] = "me"
            msg['To'] = email
            msg['Subject'] = subject

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            # send the message via the server set up earlier.
            self.smtp.send_message(msg)

            del msg
