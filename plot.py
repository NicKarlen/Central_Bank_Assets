import main 
import matplotlib.pyplot as plt

# get data with the functions in main.py

total_assets = main.Central_bank_assets()

df_ecb = total_assets.ecb
df_snb = total_assets.snb
df_fed = total_assets.fed
df_boj = total_assets.boj

# scale was 100 million Yen, for 1 million Yen *100
df_boj['Total Assets USD'] = df_boj['Total Assets USD'] * 100

plt.rcParams['axes.grid'] = True

fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)

df_ecb.plot(kind='line', x='Date', y='Total Assets USD', xlabel='Year', ylabel='Million USD', legend='True', ax=axes[0])
df_snb.plot(kind='line', x='Date', y='Total Assets USD', xlabel='Year', ylabel='Million USD', legend='True', ax=axes[0])
df_fed.plot(kind='line', x='Date', y='Total Assets',     xlabel='Year', ylabel='Million USD', legend='True', ax=axes[0])
df_boj.plot(kind='line', x='Date', y='Total Assets USD', xlabel='Year', ylabel='Million USD', legend='True', ax=axes[0])

df_ecb.plot(kind='line', x='Date', y='Total Assets',     xlabel='Year', ylabel='Million', legend='True', ax=axes[1])
df_snb.plot(kind='line', x='Date', y='Total Assets',     xlabel='Year', ylabel='Million', legend='True', ax=axes[1])
df_fed.plot(kind='line', x='Date', y='Total Assets',     xlabel='Year', ylabel='Million', legend='True', ax=axes[1])
df_boj.plot(kind='line', x='Date', y='Total Assets',     xlabel='Year', ylabel='Million', legend='True', ax=axes[1])
     
axes[0].legend(['ECB in USD', 'SNB in USD', 'FED in USD', 'BOJ in USD'])
axes[1].legend(['ECB in EUR', 'SNB in CHF', 'FED in USD', 'BOJ in JPY (100 Mio.)'])
fig.suptitle('Central Bank Assets')



plt.show()

total_assets.save_to_db('ecb')
total_assets.save_to_db('snb')
total_assets.save_to_db('fed')
total_assets.save_to_db('boj')