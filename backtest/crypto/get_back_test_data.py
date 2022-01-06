# opening client connection to binance
import csv
import datetime

from binance import Client

import config
import helper

client = Client(config.API_KEY, config.API_SECRET)

sym='EOSUSDT'
interval = Client.KLINE_INTERVAL_1DAY
start_date= "1 Jan, 2011"
current_time = datetime.datetime.now()

end_date= f"{current_time.day} {current_time.month}, {current_time.year}"

candles = helper.get_historic_data_by_start_and_end_date(client,sym,interval,start_date,end_date)
#candles = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1DAY, start_date, end_date)

csvfile = open('daily.csv', 'w', newline='')
candlestick_writer = csv.writer(csvfile,delimiter=',')

for candlestick in candles:
    candlestick[0] = candlestick[0]/1000
    candlestick_writer.writerow(candlestick)

csvfile.close()

