import os
import email_service
import currency_service

EMAIL_RECIPIENT=os.environ['CURRENCY_INSIGHT_EMAIL_RECIPIENT']

if __name__ == '__main__':
    today=currency_service.get_rate()
    weekly=currency_service.get_weekly_change()
    monthly=currency_service.get_monthly_change()
    email_text = email_service.prepare_email_txt(
        today=today,
        weekly=weekly,
        monthly=monthly
    )
    email_html = email_service.prepare_email_html(
        today=today,
        weekly=weekly,
        monthly=monthly
    )
    email_service.send_email(
        to=EMAIL_RECIPIENT,
        subject='DKK/SEK insight',
        text=email_text,
        html=email_html
    )
