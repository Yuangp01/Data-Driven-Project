import pandas as pd
import random
from collections import defaultdict

classification = pd.read_excel('classification.xlsx', sheet_name='Table', header=0, index_col=0)
clashes = pd.read_excel('classification.xlsx', sheet_name='Clashes', header=0)

num_simulations = 100

#W,T,L
system_points = [3, 1, 0]

def result(goals_local, goals_away):
    results = ['W', 'T', 'L']

    if goals_local > goals_away:
        return results[0]
    elif goals_away > goals_local:
        return results[2]
    else:
        return results[1]


def assignPoints(result):
    if result == 'W':
        return system_points[0], system_points[2]
    elif result == 'T':
        return system_points[1], system_points[1]
    else:
        return system_points[2], system_points[0]


def result_LigaChampion(classification):
    return classification.nlargest(1, 'Points').index[0]

def result_Champions(classification):
    return classification.nlargest(4, 'Points').index

def result_EuropeLeague(classification):
    return classification.nlargest(6, 'Points').index[4:6]

def result_Descending(classification):
    return classification.nsmallest(3, 'Points').index

def assignGoals():

    goals_local = random.choice(range(0, 5))
    goals_away = random.choice(range(0, 5))

    return goals_local, goals_away

def tieBreaker_averageGoal(name_team1, name_team2, classification_actual):

    dg1 = classification_actual.loc[name_team1]['DG']
    dg2 = classification_actual.loc[name_team2]['DG']

    if dg1 > dg2:
        return name_team1
    elif dg2 > dg1:
        return name_team2
    else:
        goals_in_favor1 = classification_actual.loc[name_team1]['GF']
        goals_in_favor2 = classification_actual.loc[name_team2]['GF']

        if goals_in_favor1 > goals_in_favor2:
            return name_team1
        else:
            return name_team2

def directTieBreaker(name_team1, name_team2, classification_actual):

    result1 = match_registration.at[name_team1, name_team2]
    result2 = match_registration.at[name_team2, name_team1]

    result_global_team1 = result1[0] + result2[1]
    result_global_team2 = result2[0] + result1[1]

    if result_global_team1 > result_global_team2:
        return name_team1
    elif result_global_team2 > result_global_team1:
        return name_team2
    else:
        return tieBreaker_averageGoal(name_team1, name_team2, classification_actual)


def tied_teams(classification):
    tied_teams = []

    #Get the teams with the same amount of points
    for idx, team1 in enumerate(classification.index):
        #Compare team1 with the team that are low in classification
        for team2 in classification.index[idx+1:]:
            #Check if they have the same amount of points
            if classification.loc[team1, 'Points'] == classification.loc[team2, 'Points']:
                tied_teams.append((team1, team2))

        return tied_teams

def reorderClassification(classification_copy, tied):
    #Reset index and save the column "Team"
        classification_copy['Team'] = classification_copy.index

        #TieBreak and reorder the classification: copy
        for team1, team2 in tied:
            winner = directTieBreaker(team1, team2, classification_actual=classification_copy)
            if winner == team1:
                temp = classification_copy.loc[team2].copy()
                classification_copy.loc[team2] = classification_copy.loc[team1]
                classification_copy.loc[team1] = temp
            elif winner == team2:
                temp = classification_copy.loc[team1].copy()
                classification_copy.loc[team1] = classification_copy.loc[team2]
                classification_copy.loc[team2] = temp

        #Restore "Team" as index
        classification_copy.set_index('Team', inplace=True)
        return classification_copy


match_registration = pd.DataFrame(index=range(20), columns=range(20))
match_registration = match_registration.applymap(lambda x: (0, 0))
match_registration.index = classification.index
match_registration.columns = classification.index

teams_champions = defaultdict(int)
teams_championLeague = defaultdict(int)
teams_europeLeague = defaultdict(int)
teams_descending = defaultdict(int)

for _ in range(0, num_simulations):

    classification_copy = classification.copy()
    clashes_copy = clashes.copy()

    for team in classification.index:
        rivals = clashes_copy[team].dropna()

        for rival in rivals:

            if rival == None:
                continue

            goals = assignGoals()

            match_registration.at[team, rival] = goals
            result_teams = result(goals[0], goals[1])
            score = assignPoints(result_teams)

            classification_copy.loc[team]['Points'] += score[0]
            classification_copy.loc[team]['PJ'] += 1
            classification_copy.loc[team]['GF'] += goals[0]
            classification_copy.loc[team]['GC'] += goals[1]
            classification_copy.loc[team]['DG'] += (goals[0] - goals[1])

            classification_copy.loc[rival]['Points'] += score[1]
            classification_copy.loc[rival]['PJ'] += 1
            classification_copy.loc[rival]['GF'] += goals[1]
            classification_copy.loc[rival]['GC'] += goals[0]
            classification_copy.loc[rival]['DG'] += (goals[1] - goals[0])

            clashes_copy.loc[clashes_copy[rival] == team, rival] = None

    classification_copy = classification_copy.sort_values(by='Points', ascending=False)
    tied = tied_teams(classification_copy)
    classification_copy = reorderClassification(classification_copy, tied)

    champion = result_LigaChampion(classification=classification_copy)
    teams_champions[champion] += 1

    championLeague = result_Champions(classification=classification_copy)
    for team_championLeague in championLeague:
        teams_championLeague[team_championLeague] += 1

    europeLeague = result_EuropeLeague(classification=classification_copy)
    for team_europeLeague in europeLeague:
        teams_europeLeague[team_europeLeague] += 1

    descending = result_Descending(classification=classification_copy)
    for team_descending in descending:
        teams_descending[team_descending] += 1

print()
print("Chances of winning LaLiga:\n")
for champion in teams_champions:
    print(champion + ' – ' + str(round(100*(teams_champions[champion]/num_simulations), 2)) + "%")

print()
print("Chances of qualifying for the Champions League:\n")
for championLeague in teams_championLeague:
    print(championLeague + ' – ' + str(round(100 * (teams_championLeague[championLeague] / num_simulations), 2)) + "%")

print()
print("Chances of qualifying for the Europe League:\n")
for europeLeague in teams_europeLeague:
    print(europeLeague + ' – ' + str(round(100*(teams_europeLeague[europeLeague]/num_simulations), 2)) + "%")

print()
print("Chances of Descending:\n")
for descending in teams_descending:
    print(descending + ' – ' + str(round(100*(teams_descending[descending]/num_simulations), 2)) + "%")
