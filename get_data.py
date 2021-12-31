import helper
import config
import openpyxl

from binance.client import Client
from datetime import datetime
from openpyxl.styles import PatternFill
from openpyxl.styles.colors import *

def init():
    new_symbols_for_tracking = []
    #opening client connection to binance
    client = Client(config.API_KEY, config.API_SECRET)

    # Loading the workbook for SST
    wb = openpyxl.load_workbook('sst.xlsx')

    # Loading the Main sheet from Workbook
    sh1 = wb['Main']

    #storing the total number of row count in row variable
    row = sh1.max_row

    #storing the total number of cloumn count in col variable
    col = sh1.max_column

    # Iterating all the rows in sst.xlsx
    for i in range(1, row):

        #Skipping the header using + 1 and reading the first column of each row in variable sym
        sym = sh1.cell(i + 1, 1).value

        #Passing the symbol to get the last 20 day data which is a list of list
        candles = helper.get_historic_data_by_symbol_days(client,sym,20)

        # Iterating the list of list
        for candle in candles:
            #Converting the raw timestamp to date time , NOTE - timestamp is coming in miliseconds hence divided by 1000
            candle[0] = datetime.fromtimestamp(candle[0] / 1000).strftime('%d-%m-%y')

        # Below will return the row which represents last 20 day low record
        lowest_row = min(candles, key=lambda x: x[3])

        #Fethcing the low
        low_20_day = lowest_row[3]

        #fethcing the low date
        low_20_day_date = lowest_row[0]

        #Below will return last 20 day high record
        highest_row = max(candles, key=lambda x: x[2])

        #fetching the high
        high_20_day = highest_row[2]

        # fethcing the high date
        high_20_day_date = lowest_row[0]

        sh1.cell(i + 1, 3).value = low_20_day
        sh1.cell(i + 1, 4).value = low_20_day_date

        #TODO Code to get last 20 day high from today and last 20 day high from t-1 day
        if sh1.cell(i + 1, 5).value is None :
            sh1.cell(i + 1, 5).value = high_20_day
        else:
            sh1.cell(i + 1, 6).value = high_20_day

        # Below will query and fetch the lastest spot price of the symbol
        spot = list(filter(lambda x: x.get('symbol') == sym, client.get_all_tickers()))

        #storing the spot price in excel
        sh1.cell(i + 1, 2).value = spot[0].get('price')

        #Passing the symbol to get the last 3 day data which is a list of list
        candles_3_day_low = helper.get_historic_data_by_symbol_days(client,sym,3)
        lowest_from_3_day_row = min(candles_3_day_low, key=lambda x: x[3])
        lowest_from_3_day = lowest_from_3_day_row[3]
        sh1.cell(i + 1, 8).value = lowest_from_3_day

        #Missed the opportunity in last 3 days
        if lowest_from_3_day == low_20_day:
            sh1.cell(i + 1, 9).value = 'Yes'
            new_symbols_for_tracking.append(sym)

        #Populate Away %
        away_per = ((float(high_20_day) - float(spot[0].get('price'))) / float(spot[0].get('price'))) * 100
        sh1.cell(i + 1, 7).value = int(away_per)

        #Adding a blue color background if the difference between the trigger price and current price is less thn 5
        if int(away_per) <= 15:
            sh1.cell(i + 1, 7).fill =PatternFill(start_color="d1d2ef", end_color="d1d2ef", fill_type="solid")

        #

    #Add these new symbols in Tracking sheet if already not present
    # Loading the Tracking sheet from Workbook
    sh2 = wb['Tracking']
    #storing the total number of row count in row variable
    row = sh2.max_row

    # Iterating all the rows in sst.xlsx in Tracking sheet and fetch the symbols which are already being tracked
    previous_sym_already_tracked = []
    for i in range(1, row):
        previous_sym_already_tracked.append(sh2.cell(i + 1, 1).value)

    #Apending new symbols in tracking sheet
    sym_not_in_tracking_sheet = set(new_symbols_for_tracking) - set(previous_sym_already_tracked)
    if len(sym_not_in_tracking_sheet) > 0 :
        sym_not_in_tracking_sheet_list = list(sym_not_in_tracking_sheet)
        for i in range(0,len(sym_not_in_tracking_sheet_list)):
            sh2.cell(row+ i + 1, 1).value = sym_not_in_tracking_sheet_list[i]


    #Saving the final workbook
    wb.save('sst.xlsx')
def main():
    init()

main()
