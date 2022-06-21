import main 
import matplotlib.pyplot as plt

# get data with the functions in main.py
df_ecb = main.get_data_ECB()
df_snb = main.get_data_SNB()
df_fed = main.get_data_FED()

fig, ax = plt.subplots()

df_ecb.plot(kind='line', x='Date', y='Total Assets', xlabel='Date', ylabel='Millions', legend='True', ax=ax)
df_snb.plot(kind='line', x='Date', y='Total Assets', xlabel='Date', ylabel='Millions', legend='True', ax=ax)
df_fed.plot(kind='line', x='Date', y='Total Assets', xlabel='Date', ylabel='Millions', legend='True', ax=ax)

ax.legend(['ECB', 'SNB', 'FED'])

fig.suptitle('Central Bank Assets')

plt.show()