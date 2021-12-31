# Author: Bhargav
# To get 1-min OHLC data and store it in a Json file.


from binance.client import Client
from binance.helpers import date_to_milliseconds
import json
import datetime
import time
from calendar import monthrange

import config

client = Client(config.API_KEY, config.API_SECRET)

global get_backtest_data


def get_backtest_data():
    backtest_data = [['0'], ['0']]

    symbol = "BTCUSDT"
    start_year = 2018
    start_month = 4
    start_day = 23
    start_hour = 0
    start_min = 30
    start = str(start_year) + '_' + str(start_month) + '_' + str(start_day)  # this is just for naming the json file

    end_year = 2018
    end_month = 5
    end_day = 23
    end_hour = 0
    end_min = 30
    end = str(end_year) + '_' + str(end_month) + '_' + str(end_day)

    current_year = start_year
    current_month = start_month
    current_day = start_day
    current_hour = start_hour
    current_min = start_min

    while current_month <= end_month:
        days = monthrange(2018, current_month)
        no_of_days = days[1]

        if current_month == end_month:
            no_of_days = end_day

        while current_day <= no_of_days:

            # --------------------- (covering exceptions)

            current_day1 = current_day
            current_month1 = current_month

            if current_day == no_of_days:
                if current_month == end_month:

                    current_month1 = end_month

                    if end_day == days[1]:
                        current_day1 = 0
                        current_month1 = end_month + 1
                    if end_day != days[1]:
                        current_day1 = end_day

                if current_month != end_month:
                    current_day1 = 0
                    current_month1 = current_month + 1

            # -----------------------------

            current_slot = int(current_hour / 6)
            no_of_slots = 4
            while current_slot < no_of_slots:

                start_date = str(current_year) + '-' + str(current_month) + '-' + str(current_day)
                start_time = str(current_hour) + ':' + str(current_min)
                start_datetime = start_date + ' ' + start_time + ' +0530'

                interval = Client.KLINE_INTERVAL_1MINUTE

                end_date = start_date
                end_time = str(current_hour + 6) + ':' + str(current_min - 1)

                # ----------(exception)

                if current_slot == 3:
                    end_date = str(current_year) + '-' + str(current_month1) + '-' + str(current_day1 + 1)
                    end_time = '0:' + str(current_min - 1)

                # ------------

                end_datetime = end_date + ' ' + end_time + ' +0530'

                backtest_data += client.get_historical_klines(symbol, interval, start_datetime, end_datetime)

                current_hour += 6
                current_slot = int(current_hour / 6)

            current_day += 1
            current_hour = 0

        current_month += 1
        current_day = 1

    with open(
            "Binance_{}_{}_{}-{}.json".format(
                symbol,
                interval,
                start,
                end
            ),
            'w'  # set file write mode
    ) as f:
        f.write(json.dumps(backtest_data))


get_backtest_data()

print('Data transfer complete.')