import requests
import os

MAILGUN_API_KEY=os.environ['MAILGUN_API_KEY']
MAILGUN_DOMAIN=os.environ['MAILGUN_DOMAIN']
def send_email(to, subject, text):
    URL=f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    PARAMS = {
        'from': f'Jarvis <jarvis@{MAILGUN_DOMAIN}>',
        'to': to,
        'subject': subject,
        'text': text
    }
    response = requests.post(
        url=URL,
        auth=('api', MAILGUN_API_KEY),
        data=PARAMS
    )
    return response.json()

with open('../email_template.txt', 'r') as r_file:
    TEMPLATE=r_file.read()
def prepare_email_txt(rate_today):
    return TEMPLATE.format(today=rate_today)
