# Helping Aru
# Dec 15 2020

infile = open("throwaway_v003.txt", "r")
arr = [0, 0, 0, 0, 0]
for i in range(0, 49):
    line = infile.readline()
    line = line.split(". ")[1]
    print(">>> %s" % line)
    if "DISCARDED" in line or "+" in line:
        continue
    if "A" in line:
        arr[0] += 1
    if "B" in line:
        arr[1] += 1
    if "C" in line:
        arr[2] += 1
    if "D" in line:
        arr[3] += 1
    if "E" in line:
        arr[4] += 1

print("A: {}\nB: {}\nC: {}\nD: {}\nE: {}\n".format(*arr))