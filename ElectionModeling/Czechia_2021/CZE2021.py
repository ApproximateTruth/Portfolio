import pandas as pd
import math
import numpy as np
from matplotlib import pyplot as plt

# Canada Election Model for 2021
# Made by Ryan/NeoMaxwellian
# Created 06/10/21
# Last Updated : 10/10/21
# This will in some extent predict the outcome of the 2021 Czech lower house elections
# Here is a quick introduction to the Czech election https://english.radio.cz/czech-republics-electoral-system-8728570


alli_dict = {'ANO': 'ANO', "KDUTOPODS": 'SPO', 'PTISTA': 'P+S',
             'SPD': 'SPD', 'KSC': 'KSC', 'SSD': 'SSD', 'PRI': 'PRI', 'SVO': 'TRI', 'ZEL': 'ZEL', 'OTH': 'OTH'}
parti_colours = {'ANO': '#261060', 'SPO': '#034EA2', 'P+S': '#151413', 'SPD': '#2175BB', 'KSC': '#CC0000',
                 'SSD': '#EC5800', 'PRI': '#0030FF', 'TRI': '#FF69B4', 'ZEL': '#60B64B', 'OTH': '#979797'}


# 2017 Results :
# https://www-volby-cz.translate.goog/pls/ps2017/ps61?xjazyk=CZ&xv=2&_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en-GB&_x_tr_pto=nui

def truncate_2(number, decimals=2):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


def truncate_0(number, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


# The apportion process is taken from my limited the equivalent process in Luxembourg (See link below)
# https://elections.public.lu/en/systeme-electoral/legislatives-mode-emploi/principes.html

def normalize(f):
    base = f.apply(np.sum, axis=1).to_frame()
    base = base.rename(columns={0: "num"})
    for i in f:
        f[i] = (f[i] / base['num']) * 100
        f[i].fillna(0, inplace=True)
        f[i] = f[i].apply(truncate_2)
    return f


def alliance(elx, alliances):
    for l in alliances:
        if len(l) == 2:
            name = l[0] + l[1]
            elx[name] = elx[l[0]] + elx[l[1]]
            elx[name] = elx[name] / 2
            elx = elx.drop(columns={l[0], l[1]})
        else:
            name = l[0] + l[1] + l[2]
            elx[name] = elx[l[0]] + elx[l[1]] + elx[l[2]]
            elx[name] = elx[name] / 3
            elx = elx.drop(columns={l[0], l[1], l[2]})
    return elx


def cutoff(elx):
    for h in elx:
        if h == "SPO" or h == "TRI":
            threshold = elx[h] < 11
            elx.loc[threshold, h] = 0
        elif h == "P+S":
            threshold = elx[h] < 8
            elx.loc[threshold, h] = 0
        else:
            threshold = elx[h] < 5
            elx.loc[threshold, h] = 0
    return elx


def prop_swing(elx, polling, alliances):
    elx.set_index("region", inplace=True)
    seats = elx['seats']
    elx = elx.drop(columns={'seats'})
    nat = elx.loc["NAT"].to_frame()
    nat = nat.transpose()
    nat.index.set_names("region", inplace=True)
    elx = elx.drop("NAT")
    elx = elx / nat.loc["NAT"]
    output = elx.fillna(1)
    output = alliance(output, alliances)
    output.insert(0, "PRI", [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00])
    output = output.rename(columns=alli_dict)
    output = output[['ANO', 'SPO', 'P+S', 'SPD', 'KSC', 'SSD', 'PRI', 'TRI', 'ZEL', 'OTH']]
    output = output * polling.loc['NAT']
    output = normalize(output)
    hardcopy = pd.concat([polls, output])
    hardcopy.to_csv("CZE2021_Votes.csv")
    output.insert(0, "seats", seats)
    return output


def apportion(elx, region):
    elx_f = elx.loc[region].to_frame().transpose()
    seats = elx_f.loc[region, "seats"]
    elx_f = elx_f.drop(columns={'seats'})
    quota = 100 / (seats + 1)
    seat_quotient = elx_f / quota
    seat_quotient = seat_quotient.loc[region].apply(truncate_0).to_frame().transpose()
    incomplete = True
    parties = list(elx_f)
    while incomplete:
        if seats == seat_quotient.sum(axis=1)[region]:
            incomplete = False
        else:
            new_seats = seat_quotient + 1
            new_quotient = (elx_f / new_seats).fillna(0)
            maxi = new_quotient.max(axis=1)
            for p in parties:
                if maxi[region] == new_quotient.loc[region, p]:
                    seat_quotient.loc[region, p] = seat_quotient.loc[region, p] + 1
                    break
    seat_quotient.insert(0, 'seats', seats)
    return seat_quotient


def predict(elx_f):
    all_rows = []
    elx_f = elx_f.reset_index()
    region_list = elx_f['region'].to_list()
    elx_f = elx_f.set_index('region')
    for r in region_list:
        # print(elx_f)
        new_row = apportion(elx_f, r)
        all_rows.append(new_row)
    elx_f = pd.concat(all_rows)
    new_sum = elx_f.sum(axis=0).to_frame().rename(columns={0: "NAT"}).transpose()
    elx_f = pd.concat([new_sum, elx_f])
    return elx_f


# This is where the program begins
elx_2017 = pd.read_csv("CZE_2017.csv")
polls = pd.read_csv("CZE2021_Polls.csv")
polls = polls.set_index('region')
allis = [["PTI", "STA"], ['KDU', 'TOP', 'ODS']]
elx_2021_V = prop_swing(elx_2017, polls, allis)
elx_2021_S = cutoff(elx_2021_V)
elx_2021_S = predict(elx_2021_S)
polls.insert(0, 'seats', [200])
elx_2021_V = pd.concat([polls, elx_2021_V])
elx_2021_S = elx_2021_S[list(elx_2021_S)] = elx_2021_S[list(elx_2021_S)].astype(int)
elx_2021_S.to_csv("CZE2021_Seats.csv")

# Graphing Section
CZE2021_Votes = pd.read_csv("CZE2021_Votes.csv")
CZE2021_Votes.set_index("region", inplace=True)

parties = list(CZE2021_Votes)
regions = list(CZE2021_Votes.transpose())
custom_colours = []
for parti in parties:
    custom_colours.append(parti_colours[parti])
for b in regions:
    plt.style.use("fivethirtyeight")
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    results = CZE2021_Votes.loc[b].to_list()
    ax.pie(results, labels=parties, colors=custom_colours, autopct='%1.2f%%')
    plt.savefig('Output/Votes/CZE_2021_VGraph_' + b)
elx_2021_S = elx_2021_S.drop(columns={'seats'})
for b in regions:
    plt.style.use("fivethirtyeight")
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    results = elx_2021_S.loc[b].to_frame()
    results = results[results[b] > 0]
    results = results.transpose()
    parties = list(results)
    results = results.loc[b].to_list()
    custom_colours = []
    for parti in parties:
        custom_colours.append(parti_colours[parti])
    total = elx_2017.loc[b, 'seats']
    print(total)
    ax.pie(results, labels=parties, autopct=lambda p: '{:.0f}'.format(p * total / 100),
           textprops=dict(color="darkgray"), colors=custom_colours)
    plt.savefig('Output/Seats/CZE_2021_SGraph_' + b)
