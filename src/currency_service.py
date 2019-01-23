import requests
from datetime import date, timedelta

BASE_CURRENCY='DKK'
TARGET_CURRENCY='SEK'

BASE_URL="https://api.exchangeratesapi.io"
def get_rate(date=date.today()):
    URL=f"{BASE_URL}/{date.strftime('%Y-%m-%d')}"
    PARAMS = {
        'base': BASE_CURRENCY,
        'symbols': TARGET_CURRENCY
    }
    response = requests.get(url=URL, params=PARAMS)
    return response.json()['rates']['SEK']

def get_change(start, end):
    start_rate=get_rate(date=start)
    end_rate=get_rate(date=end)
    return {
        'absolute': start_rate - end_rate,
        'percentage': (start_rate / end_rate)*100-100
    }

def get_weekly_change(date=date.today()):
    return get_change(start=date, end=date-timedelta(days=7))

def get_monthly_change(date=date.today()):
    return get_change(start=date, end=date-timedelta(days=30))
