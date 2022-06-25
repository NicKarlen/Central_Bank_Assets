import main 
import matplotlib.pyplot as plt

# get data with the functions in main.py

total_assets = main.Central_bank_assets()

df_ecb = total_assets.ecb
df_snb = total_assets.snb
df_fed = total_assets.fed
df_boj = total_assets.boj

fig, ax = plt.subplots()

df_ecb.plot(kind='line', x='Date', y='Total Assets', xlabel='Date', ylabel='Millions', legend='True', ax=ax)
df_snb.plot(kind='line', x='Date', y='Total Assets', xlabel='Date', ylabel='Millions', legend='True', ax=ax)
df_fed.plot(kind='line', x='Date', y='Total Assets', xlabel='Date', ylabel='Millions', legend='True', ax=ax)
df_boj.plot(kind='line', x='Date', y='Total Assets', xlabel='Date', ylabel='Millions', legend='True', ax=ax)

ax.legend(['ECB', 'SNB', 'FED', 'BOJ'])

fig.suptitle('Central Bank Assets')

plt.show()

total_assets.save_to_db('ecb')
total_assets.save_to_db('snb')
total_assets.save_to_db('fed')
total_assets.save_to_db('boj')