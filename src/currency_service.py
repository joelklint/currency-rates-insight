import requests
import os
from datetime import date, timedelta
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np

BASE_CURRENCY=os.environ['BASE_CURRENCY']
TARGET_CURRENCY=os.environ['TARGET_CURRENCY']

BASE_URL="https://api.exchangeratesapi.io"

def convert_date(date):
    return date.strftime('%Y-%m-%d')

def get_rate_at_day(date=date.today()):
    URL=f"{BASE_URL}/{date.strftime('%Y-%m-%d')}"
    PARAMS = {
        'base': BASE_CURRENCY,
        'symbols': TARGET_CURRENCY
    }
    response = requests.get(url=URL, params=PARAMS)
    return response.json()['rates'][TARGET_CURRENCY]

def get_rate_for_period(start, end):
    URL=f"{BASE_URL}/history"
    PARAMS = {
        'start_at': convert_date(start),
        'end_at': convert_date(end),
        'base': BASE_CURRENCY,
        'symbols': TARGET_CURRENCY
    }
    response = requests.get(url=URL, params=PARAMS)
    return response.json()

def get_change(start, end):
    start_rate=get_rate_at_day(date=start)
    end_rate=get_rate_at_day(date=end)
    return {
        'absolute': start_rate - end_rate,
        'percentage': (start_rate / end_rate)*100-100
    }

def get_weekly_change(date=date.today()):
    return get_change(start=date, end=date-timedelta(days=7))

def get_monthly_change(date=date.today()):
    return get_change(start=date, end=date-timedelta(days=30))

def generate_plot_data(start, end):
    response = get_rate_for_period(start, end)
    RATES = []
    DATES = []
    cur_date = start
    while cur_date < end:
        try:
            rate = response['rates'][convert_date(cur_date)][TARGET_CURRENCY]
        except KeyError:
            if len(RATES) == 0:
                cur_date += timedelta(days=1)
                continue
            rate = RATES[-1]
        DATES.append(cur_date.strftime('%b %d'))
        RATES.append(rate)
        cur_date += timedelta(days=1)
    return np.array(RATES), np.array(DATES)

def draw_plot(x, y, xtick_i=[]):
    if xtick_i != []:
        xtick_i = list(xtick_i)

    plt.figure(num=None, figsize=(6,2.5), dpi=70)
    plt.plot(range(len(y)), y)

    if len(xtick_i) > 0:
        plt.xticks(xtick_i, x[xtick_i], rotation=40)

    # plt.savefig('chart.png', bbox_inches='tight')
    figfile = BytesIO()
    plt.savefig(figfile, format='png', bbox_inches='tight')
    return base64.b64encode(figfile.getvalue()).decode('utf8')

def create_monthly_plot(end=date.today()):
    RATES, DATES = generate_plot_data(start=end-timedelta(days=30), end=end)
    len_dates = len(DATES)
    date_tick_indicies = range(len_dates)[0:len_dates:int(len_dates/5)]
    base64_plot = draw_plot(x=DATES, y=RATES, xtick_i=date_tick_indicies)
    return base64_plot

def create_yearly_plot(end=date.today()):
    RATES, DATES = generate_plot_data(start=end-timedelta(days=365), end=end)
    date_tick_indicies = np.where(np.array(['01' in e for e in DATES]))[0]
    base64_plot = draw_plot(x=DATES, y=RATES, xtick_i=date_tick_indicies)
    return base64_plot
