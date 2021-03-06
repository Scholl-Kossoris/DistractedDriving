import csv
import sys

import matplotlib.pyplot as plt
import numpy as np

from Processing import config

######## Configure File Info Here #########
filenum = "022"
columnCompare = "Breathing.Rate"
###########################################

fig, ax = plt.subplots()
configs = config.Config()
columnData = {}

# Basic validation to ensure file exists
if int(filenum) in configs.omitted:
    print("Invalid File Number!")
    sys.exit()

# Basic validation to ensure column name exists
if columnCompare not in configs.columnNames:
    print("Invalid Column Name!")
    sys.exit()

# Setup file into python-readable data
file = configs.localPathAverage + "Averaged_Normalized_T" + filenum + ".csv"

for columnName in configs.columnNames:
    columnData[columnName] = []

dictReader = csv.DictReader(open(file, 'rt'), fieldnames=configs.columnNames,
                            delimiter=',', quotechar='"')

for row in dictReader:
    for key in row:
        columnData[key].append(row[key])

# Variables to keep track of each new test
start = 1
count = 0
prevTime = 1

# Cycle through data and display new graph for each test run
for i in range(1, len(columnData["Time"])):
    if int(columnData["Time"][i]) < prevTime and count != 0 or i == len(columnData["Time"])-1:
        x = list(map(int, columnData["Time"][start:i-1]))
        y = list(map(float, columnData[columnCompare][start:i-1]))
        c = np.array([]);

        # This adds color coding (purple: none or yellow: stimulus) for whether or not there exists a stimulus
        for data in columnData["Stimulus"][start:i-1]:
            if data != '0':
                c = np.append(c, 1);
            else:
                c = np.append(c, 0);

        # Display plot
        plt.scatter(x,y, label='skitscat', c=c, s=25, marker="o")

        plt.xlabel('Time')
        plt.ylabel(columnCompare)
        plt.title(columnCompare + " v " + "Time\nRun " + str(count))
        plt.legend()
        plt.show()
        start = i
        count += 1
        prevTime = int(columnData["Time"][i])

    if count == 0:
        count = 1

    prevTime += 1