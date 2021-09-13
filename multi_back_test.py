import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.dates as mdates
style.use('seaborn')


df = pd.read_csv('data/BTCUSD.csv', index_col=[0])

df['returns'] = np.log(df['close'] / df['close'].shift(1))
to_plot = ['returns']


for i in [1, 3, 5, 7, 9]:
    df['position_%d' % i] = np.sign(df['returns'].rolling(i).mean())
    df['strategy_%d' % i] = (df['position_%d' % i].shift(1) * df['returns']) 
    to_plot.append('strategy_%d' % i)

df = df.dropna()

plt.figure(figsize=(10,6))
plt.title('BTCUSD')
plt.plot(df['date'],df[to_plot].cumsum().apply(np.exp))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
plt.legend(['returns', 1, 3, 5, 7, 9])
# plt.savefig('graphs/AllDay.png') 
plt.show()