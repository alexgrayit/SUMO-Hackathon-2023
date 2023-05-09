input_file = "input_p1.txt"
try: 
    f = open(input_file,"r")
    input_lines = []
    
    for line in f:
        input_lines.append(line.strip())

    for line in input_lines:
        print(line)

    f.close()
except FileNotFoundError:
    print("File not found")