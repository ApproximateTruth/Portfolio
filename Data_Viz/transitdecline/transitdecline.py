# Created by Ryan Flynn
# First made 05/12/22 ; Last updated 05/12/22
# The purpose of this is to graph the decline of ridership in Canada and the US due to COVID pandemic


from matplotlib import pyplot as plt
import pandas as pd
from numpy import sqrt

# Constants


colours = {"Toronto":"maroon", "Montreal":"dodgerblue", "Vancouver":"gold", "Ottawa":"seagreen", "Calgary":"navajowhite",
           "Edmonton":"aquamarine", "Quebec City":"darkmagenta", "Winnipeg":"navy", "Hamilton":"firebrick",
           "KWC":"darkorange", "London":"magenta"}


def dataclean(df):
    df.set_index("Area", inplace=True)
    df = df.applymap(lambda x: str(x).replace(",", ""))
    df = df.applymap(lambda x: float(x))
    return df


def metro_scatter(df):
    # This section prepares the data for the scatter plot
    columns = df.columns.to_list()
    plt.style.use("seaborn")
    plt.tight_layout()
    fig, ax = plt.subplots()
    for col in columns:
        # print(col)
        data = df[col].to_list()
        # print(data)
        ax.scatter(data[2], data[6], color=colours[col], label=col, s=(data[4]*250/3101112.5), alpha=0.8)
        size_adjust = sqrt((data[4]*250/3101112.5)/452.16)
        ax.arrow(data[2], data[2], 0, data[6] - data[2] + 0.3 + size_adjust,
                 width=0.1, alpha=0.75, ec='none', color='black', head_width=0.3)

        # ax.scatter()
        ax.legend()
    # ax.scatter(0,0,color='black', alpha=1, s=)
    ax.set_xbound(0, 30)
    ax.set_ybound(0, 30)
    ax.set_xlabel("2016 Census Metro Modal Share")
    ax.set_ylabel("2021 Census Metro Modal Share")
    ax.set_title("2016 versus 2021 Metro Modal Share")
    fig.savefig("Output/Metro_Scatter.png")


def city_scatter(df):
    # This section prepares the data for the scatter plot
    columns = df.columns.to_list()
    plt.style.use("seaborn")
    plt.tight_layout()
    fig, ax = plt.subplots()
    for col in columns:
        # print(col)
        data = df[col].to_list()
        # print(data)
        ax.scatter(data[3], data[7], color=colours[col], label=col, s=(data[4]*250/3101112.5), alpha=0.8)
        size_adjust = sqrt((data[4]*250/3101112.5)/200.16)
        ax.arrow(data[3], data[3], 0, data[7] - data[3] + 0.6 + size_adjust,
                 width=0.2, alpha=0.75, ec='none', color='black', head_width=0.6)
        # ax.scatter()
        ax.legend()
    ax.set_xbound(0, 50)
    ax.set_ybound(0, 50)
    ax.set_xlabel("2016 Census City Modal Share")
    ax.set_ylabel("2021 Census City Modal Share")
    ax.set_title("2016 versus 2021 City Modal Share")
    fig.savefig("Output/City_Scatter.png")

# Program starts here
transit_df = pd.read_csv("transitcensusdata.csv")
transit_df = dataclean(transit_df)
metro_scatter(transit_df)
city_scatter(transit_df)
