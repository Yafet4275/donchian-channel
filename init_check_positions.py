import openpyxl
from binance import Client
from config import *


import config
import helper

def init():
    # opening client connection to binance
    client = Client(config.API_KEY, config.API_SECRET)

    # Loading the workbook for SST
    wb = openpyxl.load_workbook(WORKBOOK_FOR_SST)
    sh3 = wb[WORKBOOK_INVESTMENT_SHEET]
    sh2 = wb[WORKBOOK_TRACKING_SHEET]
    helper.fetch_all_symbols_from_main()
    helper.fetch_all_sym_where_we_have_positions(helper.get_exchange())
    for i in range(1, len(helper.sym_where_we_have_position)):
        sh3.cell(i + 1, 1).value = list(helper.sym_where_we_have_position)[i]
        spot = list(filter(lambda x: x.get('symbol') == list(helper.sym_where_we_have_position)[i], client.get_all_tickers()))
        spot_price = spot[0].get('price')
        sh3.cell(i + 1, 2).value = spot_price

    #Loop to delete rows in Tracking sheet
    row2 = sh2.max_row
    for i in range(1, row2):
        sym = sh2.cell(i + 1, 1).value
        if sym in helper.sym_where_we_have_position:
            sh2.delete_rows(idx = i+1)
            print(f'Position in {sym} therefore deleting it from Tracking sheet')


    wb.save(WORKBOOK_FOR_SST)
def main():
    init()

main()