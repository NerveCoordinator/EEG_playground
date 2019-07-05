# generates random guesses to test splice script

gen_range.py 
import random

rows = []
with open("test.csv") as f:
        data = f.read().split("\n")
        rows = data[1:10] + data[20:30]

print(rows)


output = ""
for row in rows:
        id = row.split(",")[0]
        guess = str(random.uniform(-1,1))
        output += id + "," + guess + "\n"

with open("guess.csv", "w") as f:
        f.write(output)
