# Using data from https://www.kaggle.com/c/grasp-and-lift-eeg-detection/data
# Simple superimposed graph of all the electrode channels
#
# This program assumes you've already unzipped the data

import matplotlib.pyplot as plt
import numpy as np

# Takes CSV and splits it into individual rows
# separates out headers from rows for you
def csv_to_rows(filename):
    # A list of lists of values
    headers = []
    rows = []    
    with open(filename) as f:
        # Get contents
        contents = f.read()

        # Split every line
        lines = contents.split("\n")        

        # Take first row as list of headers
        headers = lines[0].split(",")

        # Take other rows as list of values
        for line in lines[1:]:
            rows.append(line.split(","))    

    # Return list of headers and list of rows
    return headers, rows

# Takes CSV rows, turns each column
# into an array associated to an id
# inside the dict
def rows_to_streams(headers, rows):
    # Associates columns to ids
    data = {}
        
    for row in rows:                
        # If row is empty, ignore it
        if len(row) < 2:
            continue
        # For every column
        for x in range(len(headers)):            
            # Append to associated dict column
            try:
                data[headers[x]].append(row[x])
            # If there is no such dict column, assign instead of append
            # Should only occur if this is the first column
            except:
                data[headers[x]] = [row[x]]
    # Return dict of columns associated to headers
    return data

# Get example data 
data_headers, data_rows = csv_to_rows("train/subj1_series1_data.csv")
data = rows_to_streams(data_headers, data_rows)
event_headers, event_rows = csv_to_rows("train/subj1_series1_events.csv")
events = rows_to_streams(event_headers, event_rows)

# Plot every channel on top of eachother
for i in range(1,len(data_headers)):
    data_first = data[data_headers[i]]#[:100] if too much data
    results = [int(i) for i in data_first]
    x = list(range(len(results)))
    plt.plot(x, results) 

# Plot when events happen
for i in range(1,len(event_headers)):
    data_first = events[event_headers[i]]#[:100]
    # Size 20000 because the event is either 0 or 1
    # this makes it easily visible.
    results = [int(i)*20000 for i in data_first]
    x = list(range(len(results)))
    plt.plot(x, results) 

# Display plot    
plt.show()
