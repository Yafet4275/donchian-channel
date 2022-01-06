import openpyxl
from binance.client import Client

import config

client = Client(config.API_KEY, config.API_SECRET)

exchange_info = client.get_exchange_info()

# Loading the workbook for SST
wb = openpyxl.load_workbook('sst.xlsx')

# Loading the Main sheet from Workbook
sh1 = wb['Main']

# storing the total number of row count in row variable
row = sh1.max_row

# storing the total number of cloumn count in col variable
col = sh1.max_column

# Loading the workbook for SST
wb = openpyxl.load_workbook('sst_1.xlsx')

for s in exchange_info['symbols']:
    i= 0
    # print(type(s))
    if 'USDT' in s['symbol']:
        sh1.cell(i + 1, 1).value = s['symbol']
        i= i+1

#Saving the final workbook
wb.save('sst.xlsx')