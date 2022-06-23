import requests
from xml.dom import minidom
import pandas as pd
from datetime import date, datetime
import json

"""
    Tutorials I used:
    https://www.youtube.com/watch?v=g7n1MZyYjOM 

"""

def format_df(df):
    # Adjust the date
    df['Date'] = pd.to_datetime(df['Date'])
    # Adjust the type
    df['Total Assets'] = df['Total Assets'].astype('float')
    # return dataframe
    return df

def get_data_FED():
    # URL direction to the Data from the FED-Website. Was able to see it after inspection it with the development Tool from Chrome
    url = "https://www.federalreserve.gov/data.xml"

    # Request the data
    req = requests.get(url)

    # Write the requested data to a .xml file
    with open("Data/data_fed.xml", "w", encoding="utf-8") as f:
        f.write(req.text)

    # parse an xml file. We use minidom for parsing of the .xml
    file = minidom.parse('Data/data_fed.xml')

    # Get elements by name
    elements = file.getElementsByTagName('chart')

    # Search for the correct titel
    for ele in elements:
        if ele.attributes['title'].value == 'Selected Assets of the Federal Reserve':
            series = ele.getElementsByTagName('series')
            break

    # Access the fields with the actual data
    for ele in series:
        if ele.attributes['description'].value == "Total Assets":
            observations = ele.getElementsByTagName('observation')
            break

    # Read the data in to a dictionary
    dict_data_FED = {}
    for ele in observations:
        dict_data_FED[ele.attributes['index'].value] = ele.attributes['value'].value

    # Creat a dataframe from a dict
    df = pd.DataFrame(dict_data_FED.items(), columns=['Date','Total Assets'])

    # return the formatted dataframe
    return format_df(df)


def get_data_SNB():
    # get timestamp
    time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # URL direction to the Data from the SNB-Website. 
    url = f"https://data.snb.ch/json/table/getFile?fileId=fa7a447f30380005c9d93ecdbc11d70f1a5d9ed28b2431da4ff8883b118e33f8&pageViewTime={time}&lang=de"

    # Request the data
    req = requests.get(url)

    # Write the requested data to a .xml file
    with open("Data/data_snb.csv", "w", encoding="utf-8") as f:
        f.write(req.text)

    # read the just downloaded csv in to a dataframe
    df = pd.read_csv("Data/data_snb.csv",sep=";" , header=2)

    # Select the needed rows
    df = df[df['D0']  == 'T1']
    # Drop unused column
    df.drop('D0', axis="columns", inplace=True)
    # Rename columns
    df.columns=['Date', 'Total Assets']

    # return the formatted dataframe
    return format_df(df)

def get_data_ECB():
    # get timestamp
    time = datetime.now().strftime("%Y-%m-%d")

    # URL direction to the Data for the ECB BalanceSheet. 
    url = f"""https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&
            drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=
            off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_
            titles=yes&show_tooltip=yes&id=ECBASSETSW&scale=left&cosd=1999-01-01&coed=2022-06-17&line
            _color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Weekly&fam=avg&
            fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={time}&revision_date={time}&nd=1999-01-01"""

    # Request the data
    req = requests.get(url)

    # Write the requested data to a .xml file
    with open("Data/data_ecb.csv", "w", encoding="utf-8") as f:
        f.write(req.text)

    # read the just downloaded csv in to a dataframe
    df = pd.read_csv("Data/data_ecb.csv",sep="," , header=0)

    # Rename columns
    df.columns=['Date', 'Total Assets']

    return format_df(df)

def get_data_BOJ():
    # get timestamp
    time = datetime.now().strftime("%Y-%m-%d")

    # URL direction to the Data for the ECB BalanceSheet. 
    url = f"""https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo
            =open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444
            444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_toolt
            ip=yes&id=JPNASSETS&scale=left&cosd=1998-04-01&coed=2022-05-01&line_color=%234572a7&link_val
            ues=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Mont
            hly%2C%20End%20of%20Period&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin
            &vintage_date={time}&revision_date={time}&nd=1998-04-01"""

    # Request the data
    req = requests.get(url)

    # Write the requested data to a .xml file
    with open("Data/data_boj.csv", "w", encoding="utf-8") as f:
        f.write(req.text)

    # read the just downloaded csv in to a dataframe
    df = pd.read_csv("Data/data_boj.csv",sep="," , header=0)

    # Rename columns
    df.columns=['Date', 'Total Assets']

    return format_df(df)

# class to get the fx rates from any currency to the USD on a monthly bases
class fx_rates:
    def __init__(self, b):
        self.base = b
        self.quote = 'USD'
        self.url = f'https://api.ofx.com/PublicSite.ApiService//SpotRateHistory/allTime/{self.base}/{self.quote}?DecimalPlaces=6&ReportingInterval=monthly&format=json'
        self.rates, self.unix_timestamps = self.convert_json_to_dict()

    # get the data via API call
    def get_monthly_rates(self):
        # Request the data
        req = requests.get(self.url)
        # convert to json
        json_res = json.loads(req.text)
        # get the historical-data from the json response
        return json_res['HistoricalPoints']

    # convert the data from the API request in to a dictionary
    def convert_json_to_dict(self):
        # get rates
        json_res = self.get_monthly_rates()
        # empty dict
        res = {}
        unix_timestamps = []
        # loop throu and create dict
        for ele in json_res:
            time = int(str(ele['PointInTime'])[0:-3])
            unix_timestamps.append(time)
            timestamp = str(datetime.utcfromtimestamp(time).date())
            res[timestamp] = ele['InterbankRate']
        return res, unix_timestamps

    # return the rate closesd to the date given
    def get_rate(self, date):
        # build unix timestamp from date given
        tstamp = datetime.timestamp(pd.to_datetime(date))
        # check where the abs difference is the smallest
        diff = []
        for t in self.unix_timestamps:
            diff.append(abs(tstamp-t))
        # get min difference
        min_value = min(diff)
        # build the date-string from the closed Unix 
        date = self.unix_timestamps[diff.index(min_value)]
        key = str(datetime.utcfromtimestamp(date).date())

        return self.rates[key]

            

eur = fx_rates("EUR")
print(datetime.utcnow())
print(eur.get_rate('2022-06-14'))
print(datetime.utcnow())

# chf = fx_rates("CHF")
# jpy = fx_rates("JPY")

