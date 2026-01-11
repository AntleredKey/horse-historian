import csv

class match:
    winner: str
    honses: list[str]
    weight: float 

with open('honses.csv', newline='') as csvfile:

    matches = []
    
    csv = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(csv)
    for row in csv:
        m = match();
        m.winner = row[0]
        m.honses = eval(row[1])
        m.weight = (len(m.honses)-1) / 11
        matches.append(m)

    distinct_honses = set([m.winner for m in matches])
    print("Distrinct horses: ", distinct_honses)

    for honse in distinct_honses:
        wins = len([m for m in matches if m.winner == honse])
        participations = len([m for m in matches if honse in m.honses])

        winrate = 100*float(wins)/participations
        
        weighted_winrate = 100*float(sum([m.weight for m in matches if m.winner == honse]))/participations
        
        print("%s wins %d of %d matches, winrate %.0f%%, weighted winrate %.0f%%"%(honse, wins, participations, winrate, weighted_winrate))