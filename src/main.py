import os
import email_service
import currency_service

EMAIL_RECIPIENTS=os.environ['CURRENCY_INSIGHT_EMAIL_RECIPIENT']

if __name__ == '__main__':
    current=currency_service.get_rate_at_day()
    weekly=currency_service.get_weekly_change()
    monthly=currency_service.get_monthly_change()
    monthly_plot = currency_service.create_monthly_plot()
    yearly_plot = currency_service.create_yearly_plot()
    # email_text = email_service.prepare_email_txt(
    #     today=today,
    #     weekly=weekly,
    #     monthly=monthly
    # )
    email_html = email_service.prepare_email_html(
        current=current,
        weekly=weekly,
        monthly=monthly,
        monthly_plot=monthly_plot,
        yearly_plot=yearly_plot
    )
    for recipient in EMAIL_RECIPIENTS.split(','):
        email_service.send_email(
            to=recipient,
            subject='DKK/SEK insight',
            text='',
            html=email_html
        )
