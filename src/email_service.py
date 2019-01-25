import requests
import os

MAILGUN_API_KEY=os.environ['MAILGUN_API_KEY']
MAILGUN_DOMAIN=os.environ['MAILGUN_DOMAIN']
def send_email(to, subject='', text='', html=''):
    URL=f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    PARAMS = {
        'from': f'Jarvis <jarvis@{MAILGUN_DOMAIN}>',
        'to': to,
        'subject': subject,
        'text': text,
        'html': html
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
def prepare_email_html(base_currency, target_currency, current, weekly, monthly, monthly_plot, yearly_plot):
    return TEMPLATE_HTML.format(
        base_currency=base_currency,
        target_currency=target_currency,
        current_rate=round(current, 4),
        weekly_absolute=round(weekly['absolute'], 4),
        weekly_percentage=f"{round(weekly['percentage'], 2)}%",
        weekly_color='green' if weekly['absolute'] > 0 else 'red',
        monthly_absolute=round(monthly['absolute'], 4),
        monthly_percentage=f"{round(monthly['percentage'], 2)}%",
        monthly_color='green' if monthly['absolute'] > 0 else 'red',
        monthly_plot=monthly_plot,
        yearly_plot=yearly_plot
    )
