import math
import os
import pandas as pd
import datetime
from datetime import date
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates


# Created by: Ryan Flynn
# Date Created: 23/09/21
# Last Updated: 01/10/21
# This was created with the documentation and examples of https://matplotlib.org/
# This is meant to demonstrate a more realized principal of "effective" immunity
# This tells a better story of how protected a certain populace is which is muddied under first dose strategies
# The countries chosen were just for my own interests, if you want to change the group, simply edit "Countries"


def truncate(number, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


# This is a image method to resize flags (I used samsung emojis) so that they fit the legend specs
def resize(directory):
    for pic in os.listdir(directory):
        img = Image.open(directory + "/" + pic)
        img = img.resize((33, 31), Image.ANTIALIAS)
        img.save(directory + "/" + pic)


# Country index is from their 'iso_code", find them here  https://www.nationsonline.org/oneworld/country_code_list.htm
countries = ['CHL', 'GBR', 'ISR', 'JPN', 'TWN', 'USA']
country_data = []
# This is a dictionary used for custom colours if colourCode is True
colourDic = {"CAN": "red", "ESP": "black", "FRA": "orange", "GBR": "limegreen", "ISR": "dodgerblue",
             "USA": "blueviolet", "EUN": "cyan", "TWN": "gold", "DEU": "teal", "NZL": "grey",
             "JPN": "crimson", "AUS": "fuchsia", "HUN": "yellowgreen", "ZAF": 'darkkhaki', 'CHL': 'hotpink',
             "ITA": "green", "GRC": "lightsteelblue", 'MEX': 'peachpuff', 'CUB': "sienna", 'BRA': 'lightsalmon'}

colourCode, offline, smooth = True, True, True


if offline:
    v_df = pd.read_csv("owid-covid-data.csv")
else:
    v_df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    v_df.to_csv("owid-covid-data.csv")
    # This saves in the data as downloading from the site takes a lot longer, switch back to False for update
# OWID_XXX for the EU and international as they has no ISO code, to make the label less ugly we filter.
v_df.replace('OWID_EUN', 'EUN', inplace=True)
v_df.replace('OWID-INT', 'UNA', inplace=True)


# The first filter keeps only the columns we need well the 2nd elimates all countries but the ones in our list
filters = [["iso_code", "date", "people_fully_vaccinated_per_hundred", "people_vaccinated_per_hundred"],
           v_df["iso_code"].isin(countries)]
v_df = v_df[filters[0]]
v_df = v_df.loc[filters[1]]
# This cleans up and re-introduces the numerical index
v_df = v_df.dropna()
v_df = v_df.set_index("iso_code")
v_df = v_df.reset_index()
v_df.index = v_df.index.set_names("index")
# This create the new column for effective immunity, the weighing used is based on Public Health England vaccine report, To download the report I used is here https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1016465/Vaccine_surveillance_report_-_week_36.pdf
v_df["effective_immunity_per_hundred"] = (v_df["people_fully_vaccinated_per_hundred"]) \
                        + 0.333333*(v_df["people_vaccinated_per_hundred"] - v_df["people_fully_vaccinated_per_hundred"])


# This separates each country into it's own dataframe and resets it's index individually, adding it to countries list
for i in countries:
    con_filter = v_df["iso_code"] == i
    temp = v_df[con_filter].reset_index()
    temp.drop(columns=["index", "people_fully_vaccinated_per_hundred", "people_vaccinated_per_hundred"], inplace=True)
    temp.index.set_names("index", inplace=True)
    if smooth:
        weeks = temp["effective_immunity_per_hundred"].rolling(7, min_periods=1)
        average = weeks.mean()
        temp["effective_immunity_per_hundred"] = average
    country_data.append(temp)


# Graphing Section
j = 0
plt.style.use("seaborn-dark")
for i in country_data:
    x = pd.to_datetime(i["date"])
    y = i["effective_immunity_per_hundred"]
    # This checks if you want to use custom colours or not
    if colourCode:
        # I made mark size very small to make the graphs more like line graphs
        plt.plot_date(x, y, markersize=0.1, linestyle='solid', label=countries[j], color=colourDic[countries[j]])
    else:
        plt.plot_date(x, y, markersize=0.1, linestyle='solid', label=countries[j])
    j += 1


# This adds the legend and formats the graph to be compact then saves the graph as a PNG
plt.xlabel('Date')
plt.ylabel('Effective Immunity per Hundred')
plt.title("Effective Immunity Over Time")
a = date.today()
b = datetime.timedelta(days=31)
plt.text((a - b), 0, "@NeoMaxwellian", fontsize=8, va="baseline", alpha=0.45)
date_format = mpl_dates.DateFormatter('%b, %Y')
plt.gca().xaxis.set_major_formatter(date_format)
plt.legend()
plt.tight_layout()
plt.gcf().autofmt_xdate()
plt.savefig('Effective_Immunity.png')

# This section then pastes the little flags on to the canvas, not that this is hard coded on the tight layout
h, w = 38, 147
for i in countries:
    main = Image.open('Effective_Immunity.png')
    flag = Image.open('Flags/' + i + ".png")
    flag_mask = flag.convert('RGBA')
    main.paste(flag, (w, h), flag_mask)
    main.save('Effective_Immunity.png')
    h = h + 21
final = Image.open('Effective_Immunity.png')
final.show()
