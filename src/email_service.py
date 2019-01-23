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
    TEMPLATE_TXT=r_file.read()
def prepare_email_txt(today, weekly, monthly):
    return TEMPLATE_TXT.format(
        today=round(today, 4),
        weekly_absolute=round(weekly['absolute'], 4),
        weekly_percentage=f"{round(weekly['percentage'], 2)}%",
        monthly_absolute=round(monthly['absolute'], 4),
        monthly_percentage=f"{round(monthly['percentage'], 2)}%",
    )

with open('../email_template.html', 'r') as r_file:
    TEMPLATE_HTML=r_file.read()
def prepare_email_html(today, weekly, monthly):
    return TEMPLATE_HTML.format(
        today=round(today, 4),
        weekly_absolute=round(weekly['absolute'], 4),
        weekly_percentage=f"{round(weekly['percentage'], 2)}%",
        monthly_absolute=round(monthly['absolute'], 4),
        monthly_percentage=f"{round(monthly['percentage'], 2)}%",
    )
