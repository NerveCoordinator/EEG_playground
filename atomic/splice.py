# Takes rows from guess.csv and uses them to overwrite values in test.csv. 
# Enables only guessing for some values instead of all of them
# This way I can guage effectiveness of predictions without predicting all 3 million datapoints.

import random

guess_rows = {}

data = []
with open("guess.csv", "r") as f:
        data = f.read().split("\n")
        for datum in data:
                print(datum)
                if len(datum) < 2:
                        continue
                id, guess = datum.split(",")
                guess_rows[id] = guess


test_rows = []
with open("test.csv") as f:
        data = f.read().split("\n")
        test_rows = data#[1:30]
        output = ""
        for row in test_rows:
                id = row.split(",")[0]
                new_row = id + ","
                try:
                        new_row += guess_rows[id]
                except:
                        new_row += "0"
                output += new_row + "\n"
        with open("splice.csv", "w") as f_2:
                f_2.write(output)
