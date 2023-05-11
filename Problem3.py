inputFile = "maze_1.csv"
try:
    f = open(inputFile, "r")

except FileNotFoundError:
    print("File not found")
    exit(-1)

for line in f:
    x_coordStr , y_coordStr , upStr, rightStr,downStr,leftStr = line.strip().split(",")
    x_coord = int(x_coordStr)
    y_coord = int(y_coordStr)
    up = int(upStr)
    right = int(rightStr)
    down = int(downStr)
    left = int(leftStr)