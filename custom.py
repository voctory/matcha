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

names = ['jacob', 'mary', 'rick', 'emily', 'sabastein', 'anna', 
              'tina', 'allen', 'jolly', 'rock', 'smith', 'waterman', 
              'mimi', 'katie', 'john', 'rose', 'leonardo', 'cynthia', 'jim', 
              'paul']

# Creating the DataFrame, here I have added the attribute 'name' for identifying the record.
df = pd.DataFrame({
    'name' : names,
    'sex' : ['Man', 'Woman', 'Man', 'Woman', 'Man', 'Woman', 'Woman', 'Man', 'Woman', 'Man', 'Man', 'Man', 'Woman', 
             'Woman', 'Man', 'Woman', 'Man', 'Woman', 'Man', 'Man'],
    'prefs' : ['Woman', 'Man', 'Woman', 'Man', 'Woman', 'Man', 'Man', 'Woman', 'Man', 'Woman', 'Woman', 'Woman', 'Man', 
             'Man', 'Woman', 'Man', 'Woman', 'Man', 'Woman', 'No preference'],
    'year' : ['4', '3', '5', '6+', '2', '6+', '6+',
             '5', '4', '4', '2', '6+', '3', '5', 
             '1', '3', '5', '4', '1', '5'],
    'food' : [0, 0, 1, 3, 2, 3, 1, 0, 0, 3, 3, 2, 1, 2, 1, 0, 1, 0, 3, 1],
    'kitchen' : [0, 1, 2, 0, 1, 2, 2, 1, 0, 0, 1, 0, 1, 1, 1, 0, 2, 0, 2, 1],
})

# Adding a normalized field 'k_scr' for kitchen
df['k_scr'] = np.where((df['kitchen'] == 2), 0.5, df['kitchen'])

# Adding a normalized field 's_scr' for sex
df['s_scr'] = np.where((df['sex'] == "Man"), -1, df['sex'])
df['s_scr'] = np.where((df['sex'] == "Male"), -1, df['s_scr'])
df['s_scr'] = np.where((df['sex'] == "Woman"), 1, df['s_scr'])
df['s_scr'] = np.where((df['sex'] == "Female"), 1, df['s_scr'])

# Adding a normalized field 'p_scr' for preference
df['p_scr'] = np.where((df['prefs'] == "No preference"), 0, df['prefs'])
df['p_scr'] = np.where((df['prefs'] == "Man"), -1, df['p_scr'])
df['p_scr'] = np.where((df['prefs'] == "Male"), -1, df['p_scr'])
df['p_scr'] = np.where((df['prefs'] == "Woman"), 1, df['p_scr'])
df['p_scr'] = np.where((df['prefs'] == "Female"), 1, df['p_scr'])

# Adding a normalized field 'a_scr' for year
df['a_scr'] = np.where((df['year'] == '1'), 1, df['year'])
df['a_scr'] = np.where((df['year'] == '2'), 3, df['a_scr'])
df['a_scr'] = np.where((df['year'] == '3'), 5, df['a_scr'])
df['a_scr'] = np.where((df['year'] == '4'), 7, df['a_scr'])
df['a_scr'] = np.where((df['year'] == '5'), 8, df['a_scr'])
df['a_scr'] = np.where((df['year'] == '6+'), 9, df['a_scr'])

commonarr = [] # Empty array for our output
dfarr = np.array(df) # Converting DataFrame to Numpy Array
for i in range(len(dfarr)): # Iterating the Array row
    for j in range(i + 1, len(dfarr)): # Iterating the Array row + 1
        # check preferences align. THIS IS PROBABLY REALLY CRITICAL :)
        # TODO: gender not taken into consideration, naive solution
        # TODO: idfk about this or condition lmao
        # old: if dfarr[i][6] * dfarr[j][6] <= 0:
        #print(f'${dfarr[i][0]} - ${dfarr[i][9]}')
        # if this is too restrictive, could make optional and instead add to score
        #if dfarr[i][7] == dfarr[j][8] and dfarr[i][8] == dfarr[j][7]:
        # ^ ideal, need to have below if nested inside
        c1 = dfarr[i][7] == dfarr[j][8] and dfarr[i][8] == dfarr[j][7]
        c2 = dfarr[j][7] == dfarr[i][8] and dfarr[j][8] == 0
        c3 = 0 == dfarr[i][8] and dfarr[j][8] == dfarr[i][7]
        c4 = 0 == dfarr[j][8] and dfarr[i][8] == 0

        if c1 or c2 or c3 or c4:
            # if dfarr[i][7] == dfarr[j][8] and dfarr[i][8] == dfarr[j][7]: pref += 6
            # if dfarr[j][7] == dfarr[i][8] and dfarr[j][8] == 0: pref += 6
            # if 0 == dfarr[i][8] and dfarr[j][8] == dfarr[i][7]: pref += 6
            # if 0 == dfarr[j][8] and dfarr[i][8] == 0: pref += 6

            row = []
            # Appending the names
            row.append(dfarr[i][0])
            row.append(dfarr[j][0])
            # Appending the final score
            row.append(
                    (dfarr[i][6] * dfarr[j][6]) +
                    (dfarr[i][5] + dfarr[j][5]) +
                    # years
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

# "name" is a guaranteed match, brute forcing optimal matches
def match(name, determine, brute_taken): # Iterating the Array row
    output = ''
    names_taken = brute_taken.copy()

    # optimal for person with input name
    optimal = []

    # ideas: filter out people by their emails. no identical names problem
    for i in people:
        if (i[0] == name or i[1] == name) and len(optimal) == 0 and (i[0] not in names_taken or i[1] not in names_taken): 
            print(i)
            optimal = i
            determine.append(i)
            output += f'\n{i[0]} and {i[1]} with {i[2]} (brute-force) confidence.'
            names_taken.append(i[0])
            names_taken.append(i[1])
            brute_taken.append(i[0])
            brute_taken.append(i[1])

        if i[0] in names_taken or i[1] in names_taken:
            continue
        names_taken.append(i[0])
        names_taken.append(i[1])
        determine.append(i)
        output += f'\n{i[0]} and {i[1]} with {i[2]} (perfect) confidence.'

    # determine unmatched after matching
    unmatched = set(names).difference(names_taken)

    print(output)

    if unmatched:
        # Should automatically figure out how to re-do matches if sub-optimal
        match(unmatched.pop(), determine, brute_taken)

    else: print('All matched!')

match("", determine, names_taken)

# for i in range(len(people) - 1): # Iterating the Array row to add both pairs of people to their list of preferences
#     if people[i][0] in X:
#         X_preferences[people[i][0]].append(people[i][1])
#         Y_preferences[people[i][1]].append(people[i][0])
#     else:
#         X_preferences[people[i][1]].append(people[i][0])
#         Y_preferences[people[i][0]].append(people[i][1])
    
