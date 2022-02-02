# Version w/o Gale-Shapley to reflect true preferences

import pandas as pd
import numpy as np

X_preferences = {}
Y_preferences = {}

# init dict of X and Y for Gale Shapley
# X = boys
# Y = girls
X = set()
Y = set()

# Creating the DataFrame, here I have added the attribute 'name' for identifying the record.
df = pd.DataFrame({
    'name' : ['jacob', 'mary', 'rick', 'emily', 'sabastein', 'anna', 
              'christina', 'allen', 'jolly', 'rock', 'smith', 'waterman', 
              'mimi', 'katie', 'john', 'rose', 'leonardo', 'cinthy', 'jim', 
              'paul'],
    'sex' : ['Man', 'Woman', 'Man', 'Woman', 'Man', 'Woman', 'Woman', 'Man', 'Woman', 'Man', 'Man', 'Man', 'Woman', 
             'Woman', 'Man', 'Woman', 'Man', 'Woman', 'Man', 'Man'],
    'prefs' : ['Woman', 'Man', 'Woman', 'Man', 'Woman', 'Man', 'Man', 'Woman', 'Man', 'Woman', 'Woman', 'Woman', 'Man', 
             'Man', 'Woman', 'Man', 'Woman', 'Man', 'Woman', 'Woman'],
    'food' : [0, 0, 1, 3, 2, 3, 1, 0, 0, 3, 3, 2, 1, 2, 1, 0, 1, 0, 3, 1],
    'age' : ['10-18', '22-26', '29-34', '40-45', '18-22', '34-40', '55-75',
             '45-55', '26-29', '26-29', '18-22', '55-75', '22-26', '45-55', 
             '10-18', '22-26', '40-45', '45-55', '10-18', '29-34'],
    'kitchen' : [0, 1, 2, 0, 1, 2, 2, 1, 0, 0, 1, 0, 1, 1, 1, 0, 2, 0, 2, 1],
})

# Adding a normalized field 'k_scr' for kitchen
df['k_scr'] = np.where((df['kitchen'] == 2), 0.5, df['kitchen'])

# Adding a normalized field 's_scr' for sex
df['s_scr'] = np.where((df['sex'] == "No preference"), 0, df['sex'])
df['s_scr'] = np.where((df['sex'] == "Man"), -1, df['s_scr'])
df['s_scr'] = np.where((df['sex'] == "Male"), -1, df['s_scr'])
df['s_scr'] = np.where((df['sex'] == "Woman"), 1, df['s_scr'])
df['s_scr'] = np.where((df['sex'] == "Female"), 1, df['s_scr'])

# Adding a normalized field 'p_scr' for preference
df['p_scr'] = np.where((df['prefs'] == "No preference"), 0, df['prefs'])
df['p_scr'] = np.where((df['prefs'] == "Man"), -1, df['p_scr'])
df['p_scr'] = np.where((df['prefs'] == "Male"), -1, df['p_scr'])
df['p_scr'] = np.where((df['prefs'] == "Woman"), 1, df['p_scr'])
df['p_scr'] = np.where((df['prefs'] == "Female"), 1, df['p_scr'])

# Adding a normalized field 'a_scr' for age
df['a_scr'] = np.where((df['age'] == '10-18'), 1, df['age'])
df['a_scr'] = np.where((df['age'] == '18-22'), 2, df['a_scr'])
df['a_scr'] = np.where((df['age'] == '22-26'), 3, df['a_scr'])
df['a_scr'] = np.where((df['age'] == '26-29'), 4, df['a_scr'])
df['a_scr'] = np.where((df['age'] == '29-34'), 5, df['a_scr'])
df['a_scr'] = np.where((df['age'] == '34-40'), 6, df['a_scr'])
df['a_scr'] = np.where((df['age'] == '40-45'), 7, df['a_scr'])
df['a_scr'] = np.where((df['age'] == '45-55'), 8, df['a_scr'])
df['a_scr'] = np.where((df['age'] == '55-75'), 9, df['a_scr'])

commonarr = [] # Empty array for our output
dfarr = np.array(df) # Converting DataFrame to Numpy Array
for i in range(len(dfarr)): # Iterating the Array row
    name = dfarr[i][0]
    if dfarr[i][1] == "Man": 
        # adding to X set
        X.add(name)
        X_preferences[name] = []
    else:
        # yeah
        Y.add(name)
        Y_preferences[name] = []

    for j in range(i + 1, len(dfarr)): # Iterating the Array row + 1
        # check preferences align. THIS IS PROBABLY REALLY CRITICAL :)
        # TODO: gender not taken into consideration, naive solution
        # TODO: idfk about this or condition lmao
        # old: if dfarr[i][6] * dfarr[j][6] <= 0:
        #print(f'${dfarr[i][0]} - ${dfarr[i][9]}')
        # if this is too restrictive, could make optional and instead add to score
        if dfarr[i][7] == dfarr[j][8] and dfarr[i][8] == dfarr[j][7]:
            if dfarr[i][5] + dfarr[j][5] > 0:
                row = []
                # Appending the names
                row.append(dfarr[i][0])
                row.append(dfarr[j][0])
                # Appending the final score
                row.append(abs((dfarr[i][6] * dfarr[j][6])) +
                        (dfarr[i][5] + dfarr[j][5]) +
                        # ages
                        (round((1 - (abs(dfarr[i][9] -
                                            dfarr[j][9]) / 10)), 2)))

                # Appending the row to the Final Array
                commonarr.append(row)

# Converting Array to DataFrame
ndf = pd.DataFrame(commonarr)

# Sorting the DataFrame on Final Score
ndf = ndf.sort_values(by=[2], ascending=False)
people = np.array(ndf)


# Scuffed implementation: searching each set by name and figuring out who's who

determine = []
names_taken = []

# ideas: filter out people by their emails. no identical names problem
for i in people:
    if i[0] in names_taken or i[1] in names_taken:
        continue
    names_taken.append(i[0])
    names_taken.append(i[1])
    determine.append(i)

# TODO: make less restrictive; currently limited by number of X or number of Y. make it score-based instead
print(determine)

# for i in range(len(people) - 1): # Iterating the Array row to add both pairs of people to their list of preferences
#     if people[i][0] in X:
#         X_preferences[people[i][0]].append(people[i][1])
#         Y_preferences[people[i][1]].append(people[i][0])
#     else:
#         X_preferences[people[i][1]].append(people[i][0])
#         Y_preferences[people[i][0]].append(people[i][1])
    
