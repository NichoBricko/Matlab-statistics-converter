import os
import numpy as np
import re

#directory containing files
directory = r'C:\Users\nicho\OneDrive\Documents\Ex-jobb\simulation results'

#statistics we're interested in
stats = ['departed vehicles [#]', 'running vehicles [#]','collisions [#]', 'avg. speed [m/s]',
         'loaded persons [#]', 'running persons [#]', 'received:', 'sent:', 'emergency braking:']

#dictionary to hold our data
data = {stat: [] for stat in stats}

#collect filenames and sort them using a regex to extract numbers
def sort_key(filename):
    match = re.match(r'(\d+)auto_(\d+)conn\.txt', filename)
    if match:
        return (int(match.group(2)), int(match.group(1)))  #sort by conn, then auto
    else:
        print("Filename does not match expected format:", filename)
        return (0, 0)  #default sort key for unmatched format

filenames = [f for f in os.listdir(directory) if f.endswith('.txt')]
sorted_filenames = sorted(filenames, key=sort_key)

#loop through each sorted file
for filename in sorted_filenames:
    file_path = os.path.join(directory, filename)
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            for stat in stats:
                if line.startswith(stat):
                    #extract the number and convert to int or float
                    value = float(line.split()[-1])
                    data[stat].append(value)
                    break

#convert lists to numpy arrays for matlab
for key in data:
    data[key] = np.array(data[key])

#example of how the print for matlab looks like
for key, values in data.items():
    print(f"{key}: {values}")
