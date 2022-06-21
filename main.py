import requests
from xml.dom import minidom
import pandas as pd
from datetime import date, datetime

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
