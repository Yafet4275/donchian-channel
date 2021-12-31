import nsepy
import datetime
import pandas as pd

def get_historical_data(stock_name):
    today = datetime.date.today()
    duration = 2000
    start = today + datetime.timedelta(-duration)
    stock_data = nsepy.get_history(symbol = stock_name,start=start,end=today)
    return stock_data

data = get_historical_data('HDFC')
data=pd.DataFrame(data)
# data['date']=data['date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
# print(data)

#df[['Open','High','Low','Close']].to_csv("nse.csv")
print(data[data.columns[0]])
data.to_csv("nse.csv")
