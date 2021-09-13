import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.dates as mdates
style.use('seaborn')

df = pd.read_csv('data/BTCUSD.csv', index_col=[0])

# log returns of buy and hold (ln base e)
df['returns'] = np.log(df['close'] / df['close'].shift(1))
df['close_shift1'] = df['close'].shift(1)
df['divide'] = df['close'] / df['close'].shift(1)

# moving average of log returns converted to positive or negative 1 
day = 2
df['position'] = np.sign(df['returns'].rolling(day).mean())
df['ma'] = df['returns'].rolling(day).mean()


# log returns of strategy based on given market position (1, -1)
# the strategy will be positive or negative based on the position
df['strategy'] = df['position'].shift(1) * df['returns']
df['position1'] = df['position'].shift(1) 

print(df[['close', 'close_shift1', 'divide','returns', 'ma', 'position', 'position1', 'strategy']])
df = df.dropna()

# plots the cumulative sum of log returns of buy and holding and the strategy 
# applied to an exponential
plt.figure(figsize=(10,6))
plt.title('BTCUSD')
plt.plot(df['date'], df[['returns', 'strategy']].cumsum().apply(np.exp))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
plt.legend(['returns', 'strategy'])
plt.savefig('graphs/BTC_{}.png'.format(day))
plt.show()