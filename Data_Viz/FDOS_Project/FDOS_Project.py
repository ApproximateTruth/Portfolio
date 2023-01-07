import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


con_dict = {'DK': 'EU', 'KR': 'AS', 'KW': 'AS', 'UA': 'EU', 'FR': 'EU', 'ID': 'AS', 'JP': 'AS', 'PE': 'SA', 'TH': 'AS',
            'RO': 'EU', 'CL': 'SA', 'IL': 'AS', 'HK': 'AS', 'IT': 'EU', 'PL': 'EU', 'FI': 'EU', 'ES': 'EU', 'RS': 'EU',
            'PH': 'AS', 'TR': 'AS', 'CH': 'EU', 'IR': 'AS', 'NZ': 'OC', 'SE': 'EU', 'SA': 'AS', 'UZ': 'AS', 'MY': 'AS',
            'CN': 'AS', 'HU': 'EU', 'AT': 'EU', 'MX': 'NA', 'AE': 'AS', 'TW': 'AS', 'RU': 'EU', 'VN': 'AS', 'DE': 'EU',
            'BD': 'AS', 'EC': 'SA', 'NO': 'EU', 'PA': 'NA', 'AU': 'OC', 'US': 'NA', 'BH': 'AS', 'BE': 'EU', 'CA': 'NA',
            'IN': 'AS', 'GR': 'EU', 'NL': 'EU', 'BR': 'SA', 'UK': 'EU', 'EG': 'AF', 'CZ': 'EU', 'PK': 'AS', 'QA': 'AS',
            'SG': 'AS', 'AR': 'SA', 'BG': 'EU', 'PT': 'EU'}
color_dict = {'NA':'firebrick', 'SA':'sandybrown', 'EU':'cornflowerblue', 'AS':'violet', 'AF':'lawngreen', 'OC':'aqua'}
num_dict = {0: 'NA', 1: 'SA', 2: 'EU', 3: 'AS', 4: 'AF', 5: 'OC'}
continents = ['NA', 'SA', 'EU', 'AS', 'AF', 'OC']

# Functions for use as here


def lin_arrange(ceof, intercept, end_y, start_x, end_x):
    y_values = np.arange(intercept, end_y + ceof, ceof)
    # x_values = np.arange(start_x, end_x, 1)
    x_values = np.arange(start_x, start_x + len(y_values), 1)
    # print("Coef = " + str(ceof) + " lenX = " + str(len(x2_values)) + " versus lenY = " + str(len(y_values)) )
    final_list = [x_values, y_values]
    return final_list


# Functions for program begin here


def clean():
    cost_df = pd.read_csv("TransitCostData.csv")
    clean_df = cost_df[["Country", "City", "Line", "Start year", "End year", "RR?", "Length", "Tunnel", "Elevated", "Atgrade", "Stations", "Cost/km (Millions)", "Cheap?", "Anglo?"]]
    # clean_df = clean_df[(clean_df['RR?'] == 0)]  # Filters out regional rail
    # print(clean_df.dtypes)
    # print(clean_df.head())
    return clean_df


def syvcost(clean_df):
    # Data Prep
    temp_df = clean_df[["Start year", "Cost/km (Millions)"]].replace('not started', '').replace('4 years', '').replace('5 years','').dropna()
    temp_df = temp_df[(temp_df["Start year"] != '')]
    years = temp_df["Start year"].to_list()
    costs = temp_df["Cost/km (Millions)"].to_list()
    years = [int(i) for i in years]

    # Linear Regression
    sy_X = np.asarray(years).reshape(-1, 1)
    sy_y = np.asarray(costs).reshape(-1, 1)
    sy_model = LinearRegression().fit(sy_X, sy_y)
    sy_output = lin_arrange(sy_model.coef_, sy_model.intercept_, max(costs), min(years), max(years))
    test_y = []
    for x in sy_X:
        test_y.append(sy_model.predict(x.reshape(-1, 1)))
    test_y = np.asarray(test_y)
    sy_2 = r2_score(sy_y, test_y.reshape(-1, 1))

    # graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    ax.plot(sy_output[0], sy_output[1], alpha=0.6, linestyle='dashed', color='black', label=str(sy_2))
    ax.scatter(years, costs, s=25, alpha=0.333333, c='deepskyblue')
    ax.set_xlabel("Start Year")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Average Contruction cost per Kilometer (Millions USD) versus starting year")
    ax.legend()
    ax = plt.gca()
    ax.set(ylim=(0, 1500))
    ax.set(xlim=(1965, 2028))
    fig.savefig("graphs/start_year_verus_cost.png")


def durvcost(clean_df):
    # Data Prep
    temp_df = clean_df[["Start year", "End year", "Cost/km (Millions)"]].replace('not started', '').replace('4 years', '').replace('5 years','').replace('X', '').dropna()
    temp_df = temp_df[(temp_df["Start year"] != '') & (temp_df["End year"] != '')]
    syears = temp_df["Start year"].to_list()
    eyears = temp_df["End year"].to_list()
    costs = temp_df["Cost/km (Millions)"].to_list()
    syears = [int(i) for i in syears]
    eyears = [int(i) for i in eyears]
    duration = []
    token = 0
    limit = len(syears)
    while token < limit:
        duration.append(eyears[token] - syears[token])
        token = token + 1

    # Linear Regression
    dur_X = np.asarray(duration).reshape(-1, 1)
    dur_y = np.asarray(costs).reshape(-1, 1)
    dur_model = LinearRegression().fit(dur_X, dur_y)
    dur_output = lin_arrange(dur_model.intercept_, dur_model.coef_, max(costs), min(duration), max(duration))
    test_y = []
    for x in dur_X:
        test_y.append(dur_model.predict(x.reshape(-1, 1)))
    test_y = np.asarray(test_y)
    dur_2 = r2_score(dur_y, test_y.reshape(-1, 1))

    # Graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    ax.plot(dur_output[0], dur_output[1], alpha=0.6, linestyle='dashed', color='black', label=str(dur_2))
    ax.scatter(duration, costs, s=25, alpha=0.333333, c='deepskyblue')
    ax.set_xlabel("Duration of Contruction")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Average Contruction cost per Kilometer (Millions USD) versus duration of project contruction")
    ax = plt.gca()
    ax.legend()
    fig.savefig("graphs/duration_verus_cost.png")
    ax.set(ylim=(0, 1500))
    fig.savefig("graphs/duration_verus_cost_zoom.png")


def tunnelpvcost(clean_df):
    # Data prep
    tunnel_df = clean_df[['Length', 'Tunnel', 'Cost/km (Millions)']]
    tunnel_df = tunnel_df.dropna()
    tunnel_len = tunnel_df['Tunnel'].to_list()
    line_len = tunnel_df['Length'].to_list()
    costs = tunnel_df["Cost/km (Millions)"].to_list()
    tunnel_len = [float(i) for i in tunnel_len]
    line_len = [float(i) for i in line_len]
    limit = len(line_len)
    token = 0
    tunnel_per = []
    while token < limit:
        ratio = tunnel_len[token] / line_len[token]
        tunnel_per.append(ratio)
        token = token + 1

    # Linear Regression
    tun_X = np.asarray(tunnel_per).reshape(-1, 1)
    tun_y = np.asarray(costs).reshape(-1, 1)
    tun_model = LinearRegression().fit(tun_X, tun_y)
    tun_output = lin_arrange(tun_model.intercept_, tun_model.coef_, max(costs), min(tunnel_per), max(tunnel_per))
    test_y = []
    for x in tun_X:
        test_y.append(tun_model.predict(x.reshape(-1, 1)))
    test_y = np.asarray(test_y)
    tun_2 = r2_score(tun_y, test_y.reshape(-1, 1))

    # Graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    ax.plot(tun_output[0], tun_output[1], alpha=0.6, linestyle='dashed', color='black', label=str(tun_2))
    ax.scatter(tunnel_per, costs, s=25, alpha=0.333333, c='deepskyblue')
    ax.set_xlabel("Percentage of rail line in a tunnel")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Proportion of Line length tunneled versus Average Contruction cost per Kilometer (Millions USD)")
    ax = plt.gca()
    ax.legend()
    ax.set(ylim=(0, 4000))
    ax.set(xlim=(-0.1, 1.1))
    fig.savefig("graphs/tunelper_verus_cost.png")


def elevatedpvcost(clean_df):
    # Prepare Data
    elevate_df = clean_df[['Length', 'Elevated', 'Cost/km (Millions)']]
    elevate_df = elevate_df.dropna()
    elevate_len = elevate_df['Elevated'].to_list()
    line_len = elevate_df['Length'].to_list()
    costs = elevate_df["Cost/km (Millions)"].to_list()
    elevate_len = [float(i) for i in elevate_len]
    line_len = [float(i) for i in line_len]
    limit = len(line_len)
    token = 0
    elevate_per = []
    while token < limit:
        ratio = elevate_len[token] / line_len[token]
        elevate_per.append(ratio)
        token = token + 1

    # Linear Regression

    ele_X = np.asarray(elevate_per).reshape(-1, 1)
    ele_y = np.asarray(costs).reshape(-1, 1)
    ele_model = LinearRegression().fit(ele_X, ele_y)
    ele_output = lin_arrange(ele_model.intercept_, ele_model.coef_, max(costs), min(elevate_per), max(elevate_per))
    test_y = []
    for x in ele_X:
        test_y.append(ele_model.predict(x.reshape(-1, 1)))
    test_y = np.asarray(test_y)
    ele_2 = r2_score(ele_y, test_y.reshape(-1, 1))

    # Graphing

    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    ax.plot(ele_output[0], ele_output[1], alpha=0.6, linestyle='dashed', color='black', label=str(ele_2))
    ax.scatter(elevate_per, costs, s=25, alpha=0.333333, c='deepskyblue')
    ax.set_xlabel("Percentage of rail line elevated")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Proportion of Line length elevated versus Average Contruction cost per Kilometer (Millions USD)")
    ax = plt.gca()
    ax.legend()
    ax.set(ylim=(0, 4000))
    ax.set(xlim=(-0.1, 1.1))
    fig.savefig("graphs/elevateper_verus_cost.png")


def atgradevcost(clean_df):
    # Prepare Data
    atgrade_df = clean_df[['Length', 'Atgrade', 'Cost/km (Millions)']]
    atgrade_df = atgrade_df.dropna()
    atgrade_len = atgrade_df['Atgrade'].to_list()
    line_len = atgrade_df['Length'].to_list()
    costs = atgrade_df["Cost/km (Millions)"].to_list()
    atgrade_len = [float(i) for i in atgrade_len]
    line_len = [float(i) for i in line_len]
    limit = len(line_len)
    token = 0
    atgrade_per = []
    while token < limit:
        ratio = atgrade_len[token] / line_len[token]
        atgrade_per.append(ratio)
        token = token + 1

    # Linear Regression
    atg_X = np.asarray(atgrade_per).reshape(-1, 1)
    atg_y = np.asarray(costs).reshape(-1, 1)
    atg_model = LinearRegression().fit(atg_X, atg_y)
    atg_output = lin_arrange(atg_model.intercept_, atg_model.coef_, max(costs), min(atgrade_per), max(atgrade_per))
    test_y = []
    for x in atg_X:
        test_y.append(atg_model.predict(x.reshape(-1, 1)))
    test_y = np.asarray(test_y)
    atg_2 = r2_score(atg_y, test_y.reshape(-1, 1))

    # Graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    ax.plot(atg_output[0], atg_output[1], alpha=0.6, linestyle='dashed', color='black', label=str(atg_2))
    ax.scatter(atgrade_per, costs, s=25, alpha=0.333333, c='deepskyblue')
    ax.set_xlabel("Percentage of rail line atgrade")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Proportion of Line length atgrade versus Average Contruction cost per Kilometer (Millions USD)")
    ax = plt.gca()
    ax.legend()
    ax.set(ylim=(0, 4000))
    ax.set(xlim=(-0.1, 1.1))
    fig.savefig("graphs/atgradeper_verus_cost.png")


def durvtime(clean_df):
    # Data Prep
    temp_df = clean_df[["Start year", "End year"]].replace('not started', '').replace('4 years', '').replace('5 years','').replace('X', '').dropna()
    temp_df = temp_df[(temp_df["Start year"] != '') & (temp_df["End year"] != '')]
    syears = temp_df["Start year"].to_list()
    eyears = temp_df["End year"].to_list()
    syears = [int(i) for i in syears]
    eyears = [int(i) for i in eyears]
    duration = []
    token = 0
    limit = len(syears)
    while token < limit:
        duration.append(eyears[token] - syears[token])
        token = token + 1
    # Graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    ax.scatter(syears, duration, s=25, alpha=0.333333, c='deepskyblue')
    ax.set_xlabel("Start year of construction")
    ax.set_ylabel("Duration of construction")
    ax.set_title("Starting Year of Project versus duration of project contruction")
    ax = plt.gca()
    fig.savefig("graphs/syear_verus_duration.png")


def stationvcost(clean_df):
    # Data Prep
    station_df = clean_df[['Stations', 'Cost/km (Millions)']]
    station_df = station_df.dropna()
    stations = station_df['Stations'].to_list()
    costs = station_df["Cost/km (Millions)"].to_list()
    stations = [int(i) for i in stations]

    # Linear Regression
    sta_X = np.asarray(stations).reshape(-1, 1)
    sta_y = np.asarray(costs).reshape(-1, 1)
    sta_model = LinearRegression().fit(sta_X, sta_y)
    sta_output = lin_arrange(sta_model.intercept_, sta_model.coef_, max(costs), min(stations), max(stations))
    test_y = []
    for x in sta_X:
        test_y.append(sta_model.predict(x.reshape(-1, 1)))
    test_y = np.asarray(test_y)
    sta_2 = r2_score(sta_y, test_y.reshape(-1, 1))

    # Graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    ax.plot(sta_output[0], sta_output[1], alpha=0.6, linestyle='dashed', color='black', label=str(sta_2))
    ax.scatter(stations, costs, s=25, alpha=0.333333, c='deepskyblue')
    ax.set_xlabel("Number of Stations in Project")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Number of Stations built versus Average Contruction cost per Kilometer (Millions USD)")
    ax = plt.gca()
    ax.legend()
    ax.set(ylim=(0, 4000))
    fig.savefig("graphs/stations_verus_cost.png")


def linelength(clean_df):
    # Prepare Data

    length_df = clean_df[['Length', 'Cost/km (Millions)']]
    length_df = length_df.dropna()
    line_len = length_df['Length'].to_list()
    costs = length_df["Cost/km (Millions)"].to_list()
    line_len = [float(i) for i in line_len]

    # Linear regression
    len_X = np.asarray(line_len).reshape(-1, 1)
    len_y = np.asarray(costs).reshape(-1, 1)
    len_model = LinearRegression().fit(len_X, len_y)
    len_output = lin_arrange(len_model.intercept_, len_model.coef_, max(costs), min(line_len), max(line_len))
    test_y = []
    for x in len_X:
        test_y.append(len_model.predict(x.reshape(-1, 1)))
    test_y = np.asarray(test_y)
    len_2 = r2_score(len_y, test_y.reshape(-1, 1))

    # Graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    ax.plot(len_output[0], len_output[1], alpha=0.6, linestyle='dashed', color='black', label=str(len_2))
    ax.scatter(line_len, costs, s=25, alpha=0.333333, c='deepskyblue')
    ax.set_xlabel("Length of Line (km)")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Length of line (km) versus Average Contruction cost per Kilometer (Millions USD)")
    ax = plt.gca()
    ax.legend()
    ax.set(ylim=(0, 4000))
    fig.savefig("graphs/linelength_verus_cost.png")


def continentscostvtime(clean_df):
    # Data prep
    con_df = clean_df[["Country", "Start year", "Cost/km (Millions)"]].replace('not started', '').replace('4 years', '').replace('5 years','').dropna()
    con_df = con_df[(con_df["Start year"] != '')]
    con_df["Country"] = con_df["Country"].map(con_dict)

    # Graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    token = 0
    while token < 6:
        temp_df = con_df[(con_df["Country"] == num_dict[token])]
        years = temp_df["Start year"].to_list()
        costs = temp_df["Cost/km (Millions)"].to_list()
        years = [int(i) for i in years]
        ax.scatter(years, costs, s=25, alpha=0.6, c=color_dict[num_dict[token]], label=num_dict[token])

        token = token + 1
    ax.set_xlabel("Start Year")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Average Construction cost per Kilometer (Millions USD) versus starting year")
    ax.legend(loc='upper left')
    ax = plt.gca()
    ax.set(ylim=(0, 1500))
    ax.set(xlim=(1965, 2028))
    fig.savefig("graphs/start_year_verus_cost_CON.png")


def anglovtime(clean_df):
    # Data Prep
    anglo_df = clean_df[["Start year", "Cost/km (Millions)", "Anglo?"]].replace('not started', '').replace('4 years', '').replace('5 years','').dropna()
    anglo_df = anglo_df[(anglo_df["Start year"] != '')]

    # Graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    token = 0
    cols = ['gray', 'goldenrod']
    labs = ['Non-anglo', 'Anglo']
    while token < 2:
        temp_df = anglo_df[(anglo_df["Anglo?"] == token)]
        years = temp_df["Start year"].to_list()
        costs = temp_df["Cost/km (Millions)"].to_list()
        years = [int(i) for i in years]
        ax.scatter(years, costs, s=25, alpha=0.6, c=cols[token], label=labs[token])

        token = token + 1
    ax.set_xlabel("Start Year")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Average Construction cost per Kilometer (Millions USD) versus starting year")
    ax.legend(loc='upper left')
    ax = plt.gca()
    # ax.set(ylim=(0, 1500))
    ax.set(xlim=(1965, 2028))
    fig.savefig("graphs/start_year_verus_cost_ANGLO.png")


def cheapvtime(clean_df):
    # Data Prep
    anglo_df = clean_df[["Start year", "Cost/km (Millions)", "Cheap?"]].replace('not started', '').replace('4 years', '').replace('5 years','').dropna()
    anglo_df = anglo_df[(anglo_df["Start year"] != '')]

    # Graphing
    plt.style.use("seaborn")
    fig, ax = plt.subplots()
    token = 0
    cols = ['gray', 'palegreen']
    labs = ['Expensive', 'Cheap']
    while token < 2:
        temp_df = anglo_df[(anglo_df["Cheap?"] == token)]
        years = temp_df["Start year"].to_list()
        costs = temp_df["Cost/km (Millions)"].to_list()
        years = [int(i) for i in years]
        ax.scatter(years, costs, s=25, alpha=0.6, c=cols[token], label=labs[token])

        token = token + 1
    ax.set_xlabel("Start Year")
    ax.set_ylabel("Cost/km (Millions)")
    ax.set_title("Average Construction cost per Kilometer (Millions USD) versus starting year")
    ax.legend(loc='upper left')
    ax = plt.gca()
    # ax.set(ylim=(0, 1500))
    ax.set(xlim=(1965, 2028))
    fig.savefig("graphs/start_year_verus_cost_CHEAP.png")


def main():
    clean_df = clean()
    syvcost(clean_df)
    durvcost(clean_df)
    tunnelpvcost(clean_df)
    elevatedpvcost(clean_df)
    atgradevcost(clean_df)
    durvtime(clean_df)
    stationvcost(clean_df)
    linelength(clean_df)
    continentscostvtime(clean_df)
    anglovtime(clean_df)
    cheapvtime(clean_df)


def averagecost(clean_df):
    cost_df = clean_df[(clean_df["Anglo?"] == 0)]
    con_list = cost_df["Country"].to_list()
    con_list = list(set(con_list))
    final_cost = 0
    final_con = ''
    for con in con_list:
        temp_df = cost_df[(cost_df["Country"] == con)]
        costs = temp_df["Cost/km (Millions)"].to_list()
        print(con + ": "+  str(len(costs)))
        total = 0
        for pro in costs:
            total = total + pro
        total = total / len(costs)
        if total > final_cost & len(costs) > 0:
            final_cost = total
            final_con = con
    print("The highest average non-anglo cost is " + str(final_cost) + " from " + str(final_con))
    print(cost_df[(cost_df["Country"] == final_con)])

    return 5


def postmain():
    clean_df = clean()
    anglo_df = clean_df[(clean_df["Anglo?"] == 1)]
    anglo_con = anglo_df["Country"].to_list()
    # print(list(set(anglo_con)))
    # print(clean_df[(clean_df['Country'] == 'NL') | (clean_df['Country'] == 'IL')])
    # print(clean_df[(clean_df["City"] == "Dublin")])
    # averagecost(clean_df)
    print(continents[2])

# Program begins here
postmain()
# main()'
# test()


