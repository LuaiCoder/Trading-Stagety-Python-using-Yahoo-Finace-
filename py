import pandas as pd

import numpy as np
import yfinance as yf

from datetime import datetime
import matplotlib.pyplot as plt

plt.style.use('ggplot')

#Collecting Data from Tesla

x = datetime.now()

current_t = "{year}-{month}-{day}".format(year = x.year, month = x.month,day = x.day)


df = yf.download('TSLA', start='2015-01-01', end=current_t, progress=False)

SMA30 = pd.DataFrame()
SMA30['Adj Close'] = df['Adj Close'].rolling(window=30).mean()
SMA100 = pd.DataFrame()
SMA100['Adj Close'] = df['Adj Close'].rolling(window=100).mean()

data = pd.DataFrame()
data['TSLA'] = df['Adj Close']
data['SMA30'] = SMA30['Adj Close']
data['SMA100'] = SMA100['Adj Close']

#creating a function to show Buy and Sell signals

def buy_sell(signal):
    signalBuy = []
    signalSell = []
    flag = -1
    for i in range(0, len(signal)):

        if signal['SMA30'][i] > signal['SMA100'][i]:
            if flag != 1:
                signalBuy.append(signal['TSLA'][i])
                signalSell.append(np.nan)
                flag = 1
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)

        elif signal['SMA30'][i] < signal['SMA100'][i]:
            if flag != 0:
                signalSell.append(signal['TSLA'][i])
                signalBuy.append(np.nan)
                flag = 0
            else:
                signalSell.append(np.nan)
                signalBuy.append(np.nan)

        else:
            signalBuy.append(np.nan)
            signalSell.append(np.nan)

    return (signalBuy, signalSell)



x = buy_sell(data)
data['Buy_Signal_Price'] = x[0]
data['Sell_Signal_Price'] = x[1]

print (data)

plt.figure(figsize=(12.5, 4.5))
plt.plot(data['TSLA'], label='TSLA', color='white')
plt.plot(data['SMA30'], label='SMA30')
plt.plot(data['SMA100'], label='SMA100')
plt.scatter(data.index,data['Buy_Signal_Price'], label= 'Buy', marker= '^', color='green')
plt.scatter(data.index,data['Sell_Signal_Price'], label= 'Sell', marker= 'v', color='red')
plt.title('TSLA')
plt.xlabel('Time')
plt.ylabel('Adj Close Price in USD $')
plt.legend(loc='upper right')
plt.show()
