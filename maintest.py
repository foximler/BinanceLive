import requests
import pandas as pd
import time
import talib as ta

#coin to test on, one for now but should be looped for data recovery

market = 'LINKBTC'
tickrate = '15m'
url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval='+tickrate
data = requests.get(url).json()

#print(data)

#now we get the live data to set the moving average to something live
def getliveprice(markettopull):
   url_live = 'https://api.binance.com/api/v1/ticker/price?symbol='+markettopull
   data_live = requests.get(url_live).json()
   lastprice = data_live['price']
   return lastprice

def updateOhlcv(markettopull,tick,currentdf):
   #sameshitasearlier
   url='https://api.binamce.com/api/v1/klines?symbol='+markettopull+'&interval='+tick
   data=requests.get(url).json()
   dfTomerge = pd.DataFrame(data,columns=['opentime','open','high','low','close','volume',
                                           'close_time','quote_asset_volume','number_of_trades',
                                           'taker_buy_base_asset_volume','taker_buy_base_asset_volume',
                                           'ignore'])
   dfTomerge['Date_Humanized'] = (pd.to_datetime(dfTomerge['opentime'],unit='ms'))
   dfTomerge = dfTomerge.set_index('opentime')
   newpd = pd.merge(dfTomerge,currentdf, on='opentime')
   return newdf
def generate_tadata(df):
   df['RSI'] = ta.RSI(df.close,14)
   df['MACD'], df['MACDISGNAL'], df['MACDHIST'] = ta.MACD(df.close, fastperiod=8, slowperiod=16, signalperiod=11)
   df['Momentum'] = ta.MOM(df.close, timeperiod=10)
   return df
#create initial dataset
df = pd.DataFrame(data,columns=['opentime','open','high','low','close','volume','close_time',
                                'quote_asset_volume','number_of_trades','taker_buy_base_asset_volume',
                                'taker_buy_quote_asset_volume','ignore'])
df['Date_Humanized'] = (pd.to_datetime(df['opentime'],unit='ms'))
df = df.set_index("opentime")
print(df.tail(1))
#df.iloc[-1,df.columns.get_loc('close')] = getliveprice()
while True:
   df.iloc[-1,df.columns.get_loc('close')] = getliveprice(market)
   print("latest price for ", market," is ", df.iloc[-1,df.columns.get_loc('close')])
   df = generate_tadata(df)
   if (df.index[-1]-time.time()*1000) >=900000 :
       #updatedataset
       df = updateOhlcv(market,tickrate,df)
       print(df.tail(1))
   else:
       time.sleep(5)
       #print("Sleeping for 5 seconds")
       #print(ta.RSI(df.close,14))
       #df['RSI'] = ta.RSI(df.close,14)
       print(df.tail(1))
