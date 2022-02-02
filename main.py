# cursed 1 file code
# >> CPSC 210 angry noises
# Matcha!!
# Workflow:
# Step 1. import data from spreadsheet. probably a csv for now, but ideally straight from Google Sheets API later on
# Step 2. use data to create preferences for each person
# Step 3. use preferences to create stable matchas using Gale Shapley
# Step 4. profit

# Gale Shapley import
from collections import deque





# Below: Gale Shapley
def pref_to_rank(pref):
    return {
        a: {b: idx for idx, b in enumerate(a_pref)}
        for a, a_pref in pref.items()
    }


def gale_shapley(*, A, B, A_pref, B_pref):
    """Create a stable matching using the
    Gale-Shapley algorithm.
    
    A -- set[str].
    B -- set[str].
    A_pref -- dict[str, list[str]].
    B_pref -- dict[str, list[str]].

    Output: list of (a, b) pairs.
    """
    B_rank = pref_to_rank(B_pref)
    ask_list = {a: deque(bs) for a, bs in A_pref.items()}
    pair = {}
    #
    remaining_A = set(A)
    while len(remaining_A) > 0:
        a = remaining_A.pop()
        b = ask_list[a].popleft()
        if b not in pair:
            pair[b] = a
        else:
            a0 = pair[b]
            b_prefer_a0 = B_rank[b][a0] < B_rank[b][a]
            if b_prefer_a0:
                remaining_A.add(a)
            else:
                remaining_A.add(a0)
                pair[b] = a
    #
    return [(a, b) for b, a in pair.items()]


output = gale_shapley(
    A={"S.Samuel", "S.Bobby", "S.John"},
    B={"F.Smith", "F.Martinez", "F.Brown"},
    A_pref={
        "S.Samuel": ["F.Smith", "F.Brown", "F.Martinez"],
        "S.Bobby": ["F.Martinez", "F.Brown", "F.Smith"],
        "S.John": ["F.Martinez", "F.Brown", "F.Smith"],
    },
    B_pref={
        "F.Smith": ["S.Samuel", "S.John", "S.Bobby"],
        "F.Martinez": ["S.Samuel", "S.Bobby", "S.John"],
        "F.Brown": ["S.John", "S.Samuel", "S.Bobby"],
    },
)

print(output)