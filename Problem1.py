import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')  # for displaying in separate window
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Computer Modern Roman"
})

# Taken from https://www.geeksforgeeks.org/program-find-gcd-floating-point-numbers/
# Recursive function to return gcd
# of a and b
def gcd(a, b):
    if (a < b):
        return gcd(b, a)

    # base case
    if (abs(b) < 0.001):
        return a
    else:
        return (gcd(b, a - np.floor(a / b) * b))


class Sensor:
    times = []
    location = [0, 0]

    def __init__(self, location, times):
        self.times = times
        self.location = location

inputFile = "input_p1.txt"
try: 
    f = open(inputFile, "r")

except FileNotFoundError:
    print("File not found")
    exit(-1)

inputLines = []

sensorsInFile = -1
for line in f:
    sensorsInFile += 1
    inputLines.append(line.strip())
try:
    lapsStr, sensorsStr = inputLines[0].split(", ")
    laps = int(lapsStr)
    sensors = int(sensorsStr)
except:
    print("There was an error in the first line, invalid format")
    exit(-1)

if sensors != sensorsInFile:
    print("Not enough sensors provided")

# Collect sensor objects and times into arrays
sensorLines = inputLines[1:]
sensors = []
timesMatrix = []

timeLen = 0

for i in range(1, len(sensorLines)):
    splitLine = inputLines[i].split(', ')
    sensorX = splitLine[0]
    sensorY = splitLine[1]
    pos = np.array([sensorX, sensorY]).astype(float)

    sensorMeasurements = np.array(splitLine[2:]).astype(float)
    if i == 1:
        timeLen = len(sensorMeasurements)
    else:
        if len(sensorMeasurements) != timeLen:
            print("Number of measurements from each sensor is different.")
            exit(-1)

    sensor = Sensor(pos, sensorMeasurements)
    sensors.append(sensor)
    timesMatrix.append(sensorMeasurements)

# Transpose times so that times [[0 -> n], [...], ...] are all in consecutive order
timesMatrix = np.array(timesMatrix)
timesMatrix = timesMatrix.transpose()

# Check the sensor times are in the correct order
tPrev = 0
for ti in range(len(timesMatrix)):
    for tj in range(len(timesMatrix[ti])):
        if timesMatrix[ti][tj] < tPrev:
            if timesMatrix[ti][tj] < 0:
                print("There is an error in the times, a time is negative.")
            else:
                print("Times are out of order from the sensor order.")
            exit(-1)
        else:
            tPrev = timesMatrix[ti][tj]

sensorPlotPoints = []
for sensor in sensors:
    sensorPlotPoints.append(sensor.location)
sensorPlotPoints.append(sensors[0].location)

sensorPlotPoints = np.array(sensorPlotPoints).transpose()

plt.plot(sensorPlotPoints[0], sensorPlotPoints[1])
plt.show()

f.close()
# f = open(input_file, "r")
# print(f.read())