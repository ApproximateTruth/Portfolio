# Made by : Approximate Truth
# Status : Mostly Completely
# First made 09/12/22 ; Last updated 10/12/22
# The purpose of this is to simulate the true probabilities of the video game "Genshin Impact" gacha system
# The system to gain certain 5-star characters requires you use a "wish" to win a random chance with low chances
# This low chance as you get further into your attempts has a "pity" system which allows
# Complete: Everything works great, it's an exe and has user input. My only regret is not using textual but next time


# TODO plt.show() creates two figures when only one instance is there, the first figure is also blank
# TODO There is a limit on the number of Five Star Characters, implementing that should be useful
# TODO Some variable to allow different batch sizes for simulations instead of the hard coded 100,000
# TODO Have the text of the plot auto scale to not to touch any bars

import numpy as np
from numpy import random
from matplotlib import pyplot as plt
import time
import os
import keyboard
import math


# Constants
pity = 0.06626666666666666666666666666667  #


# Functions


def clear():
    os.system('cls')  # this automates the clearing of the screen


def truncate_0(number, decimals=0):  # This function truncates numbers to simply their integer parts
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


def progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    # This function was taken from
    # https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters/13685020
    # This creates the progress bar when the main program is runnign the monte carlo
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)

    # Progress Bar Printing Function
    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def pull_sim(pulls):
    # This function gets a number of 5 stars gotten from a certain number of pulls
    # A "5 star" is the victory condition ant and a "pull" is the number of times you take the chance for a victory
    # What makes this interesting is that although the base probability is low (0.6%) a "pity" mechanic increases this
    # The base chance increases from attempts 76-90 linearly to 100%
    # This rests upon victory
    token = 0  # This variable keeps track of total attempts
    counter = 0  # This variable keeps track of attempts since last victory
    fives = 0  # This variable keeps track of total victories
    pull = False  # This tells up at the top of loop if a victory has just been won
    while token < pulls:  # This check tells us if we've used all our attempts
        if pull:  # This checks to see if we just won so the pity counter can reset
            pull = False
            counter = 0
        else:
            roll = random.rand()  # This is our "roll" which determines if we won or not
            if counter <= 75:  # for the first 75 attempts it stays at base rate 0.6%
                if roll <= 0.006:
                    fives = fives + 1
                    pull = True
            elif counter > 75:
                if roll <= (0.006 + (pity * (counter - 75))):  # This raises the chance linearly
                    fives = fives + 1
                    pull = True
            counter = counter + 1
            token = token + 1
    return fives


def macau(sims, attempts, outcome):  # This is the monte carlo method to determine our distrobution
    token = 0  # This variable keeps track of how many simulations have been run
    data = []  # this list will store our data
    bottom = True  # This boolean tells us if the target needs to be in the 'top' or 'bottom' percentile
    simulation = list(range(0, sims))  # This variable just creates enough length of an iterable for our progress bar
    for sim in progressBar(simulation, prefix='Progress:', suffix='Complete', length=50):
        # This adds all the outcome to the data list
        data.append(pull_sim(attempts))
        token = token + 1

    token = 0
    output = []
    # This tells us the largest number of victories in this simulation, we don't need to graph the full domain
    limit = max(data)
    if outcome > limit:  # this check is incase the target outcome being checked is larger than our largest victory
        limit = outcome + 1
    base = np.arange(limit).tolist()  # This creates the x values for the graph
    total = 0
    while token < limit:
        total = total + data.count(token)  # This tells us our total number of victories
        output.append(data.count(token))  # This counts the number of occurrences of a victory count
        token = token + 1
    token = 0
    while token < len(output): # This transforms the number into a percentage
        output[token] = output[token] / total
        token = token + 1
    xlist = list(range(0, limit,(truncate_0(limit/15) + 1))) # This creates a nicer X-range
    xlist = [int(i) for i in xlist] # Converts the list of numbers from str to int

    # Graphing Begins
    plt.style.use("seaborn")
    plt.tight_layout()
    fig, ax = plt.subplots()
    ax.set_yticks([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
    ax.set_xticks(xlist)
    ax.bar(base, output)
    ax.set_xlabel("Number of 5 Star Pulls")
    ax.set_ylabel("Probability of that number of pulls")
    ax.set_title(("Genshin pull simulations of " + str(attempts) + " pulls, total simulations " + str(sims)))
    ax.bar(outcome, output[outcome], color="firebrick")  # This highlights user chosen outcome

    # This determines the text section
    percent = str(output[outcome])
    if len(percent) < 5: # This check is in case that the target outcome is 0.0%
        percent = percent + "%"
    else:
        percent = percent[2:4] + "." + percent[5] + "%"
    token = 0
    percentile = 0
    while token < (outcome + 1):
        percentile = percentile + output[token]
        token = token + 1
    percentile = str(percentile)
    if len(percentile) < 5:  # This check  is incase the percentile is 0.0%
        percentile = percentile + "%"
    else:
        percentile = percentile[2:4] + "." + percentile[5] + "%"
    ax.text(0.1, max(output) * 2 / 3, "This outcome individually has a probability of " + percent +
            "\noccurring. Taking all values from 0 to " + str(outcome) + ",\nthis outcome is in the " +
            percentile + " percentile of outcomes", size="small")
    plt.show()
    # title = "Output/GenshinPull_Attempts" + str(attempts) + "_Simulations" + str(sims) + "_5*count" + \
    #         str(outcome) + ".png"
    # fig.savefig(title)


def main_program():  # This runs all the user input portion of the program
    question = True
    print("This program will calculate how (un)lucky you are!")
    time.sleep(0.8)
    print("Enter in your pull amount and number of Five stars, a simulation will occur to determine your probability")
    time.sleep(0.8)
    print("Press enter to continue")
    while question:
        if keyboard.is_pressed("enter"):
            break
    clear()
    buffer = input()
    while question:
        try:
            attempts = int(input("How many times have you pulled?: "))
            break
        except ValueError:
            clear()
            print("Number of attempts Attempts must be an integer, please try again")
            time.sleep(1)
    clear()
    while question:
        try:
            outcome = int(input("How many 5 stars do you have?: "))
            break
        except ValueError:
            clear()
            print("Number of Five Stars must be an integer please try again")
    clear()
    macau(100000, attempts, outcome)


# program start
main_program()
