import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation, writers

matplotlib.use('TkAgg')  # for displaying in separate window
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Computer Modern Roman"
})

dt = 1/30


class Sensor:
    times = []
    location = [0, 0]

    def __init__(self, location, times):
        self.times = times
        self.location = location

inputFile = "real track_p1.txt"
try: 
    f = open(inputFile, "r")

except FileNotFoundError:
    print("File not found")
    exit(-1)

inputLines = []

sensorsInFile = -1
for line in f.readlines():
    sensorsInFile += 1
    inputLines.append(line.strip())
try:
    lapsStr, sensorsStr = inputLines[0].split(", ")
    laps = int(lapsStr)
    sensors = int(sensorsStr)

    print(laps, sensors)
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

for i in range(1, len(sensorLines) + 1):
    splitLine = inputLines[i].split(', ')
    sensorX = splitLine[0]
    sensorY = splitLine[1]
    pos = np.array([sensorX, sensorY]).astype(float)

    sensorMeasurements = np.around(np.array(splitLine[2:]).astype(float), 15)

    if len(sensorMeasurements) != laps:
        print("Number of measurements do no match number of laps.")
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

# Find Lap Times
lapTimes = []
for i in range(len(timesMatrix)):
    lapTime = timesMatrix[i][0] - timesMatrix[i][-1]
    lapTimes.append(lapTime)
lapTimes = np.array(lapTimes)


# Find Split Times
flatTimes = timesMatrix.flatten()
splitTimesMatrix = timesMatrix*0
for ti in range(len(timesMatrix)):
    for tj in range(len(timesMatrix[ti])):
        if ti == 0 and tj == 0:
            # Set error value
            splitTimesMatrix[ti][tj] = np.NaN
        else:
            # Calculate time since pass prev sensor
            splitTimesMatrix[ti][tj] = timesMatrix[ti][tj] - flatTimes[ti*len(timesMatrix[ti]) + tj - 1]


totalTime = timesMatrix[0][0]
for ti in range(len(timesMatrix)):
    for tj in range(len(timesMatrix[ti])):
        if ti + tj != 0:
            totalTime += splitTimesMatrix[ti][tj]

print(totalTime)


sensorPlotPoints = []
for sensor in sensors:
    sensorPlotPoints.append(sensor.location)
sensorPlotPoints.append(sensors[0].location)

sensorPlotPoints = np.array(sensorPlotPoints).transpose()

fig = plt.figure()
fig.set_size_inches(7, 7, True)
ax = fig.add_subplot(1, 1, 1)
ax.ticklabel_format(axis='both', style="sci")
ax.set_aspect('equal')

ax.set_xlabel(r"$x\ (\textnormal{m})$")
ax.set_ylabel(r"$y\ (\textnormal{m})$")

# timeText = ax.text(xmin + 1, ymax + 2, r"$t={0:.3f}".format(t[-1]) + r"\, \textnormal{s}$", fontsize=12)

carPoint, = ax.plot(sensorPlotPoints[0][0], sensorPlotPoints[1][0], marker='.', markersize=15)



def animate(i):
    tmax = np.max(flatTimes)
    t = i*dt

    indexOfLastTime = np.where(flatTimes > t)[0][0] - 1
    indexOfLastSensor = indexOfLastTime % (len(timesMatrix[0]))
    #print(indexOfLastSensor)

    tLast = flatTimes[indexOfLastTime]
    tNext = flatTimes[indexOfLastTime + 1]
    xLast = sensorPlotPoints[0][indexOfLastSensor]
    yLast = sensorPlotPoints[1][indexOfLastSensor]
    xNext = sensorPlotPoints[0][indexOfLastSensor + 1]
    yNext = sensorPlotPoints[1][indexOfLastSensor + 1]

    x = ((xNext - xLast) / (tNext - tLast))*(t - tLast) + xLast
    y = ((yNext - yLast) / (tNext - tLast)) * (t - tLast) + yLast

    carPoint.set_data(x, y)


ax.plot(sensorPlotPoints[0], sensorPlotPoints[1])
# Create Animation, comment out to just plot regular plot of paths
ts = np.arange(0, np.max(flatTimes), dt)
anim = FuncAnimation(fig, animate, frames=ts.size, interval=dt)
# Comment out if not saving
# DPI = 1200 / 7
# Writer = writers['ffmpeg']
# Writer = Writer(fps=1/dt, bitrate=12000)
# anim.save('Race Sim.mp4', writer=Writer, dpi=DPI)

# Comment if saving as mp4
plt.show()

f.close()
# f = open(input_file, "r")
# print(f.read())