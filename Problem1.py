input_file = "input_p1.txt"
try: 
    f = open(input_file,"r")
    input_lines = []
    
    sensorsInFile = -1
    for line in f:
        sensorsInFile += 1
        input_lines.append(line.strip())

    lapsStr,sensorsStr = input_lines[0].split(", ")
    laps = int(lapsStr)
    sensors = int(sensorsStr)

    if(sensors != sensorsInFile):
        print("Not enough sensors provided")

    f.close()
except FileNotFoundError:
    print("File not found")