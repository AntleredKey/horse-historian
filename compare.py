import sys
import sqlite3
horses = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD", "VOID"]
gen0 = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD"]
gen1 = ["DDD", "FLP", "LFS", "MET", "SFE", "WSY"]
gen2 = ["GUN", "LWN", "PSN", "SJU", "SUN", "VOD"]
generations = {"0": gen0, "1": gen1, "2": gen2}
maps = ["1", "2", "3"]
map_names = ["pools", "vyral_cbt", "reya_castle"]

def main():
    horse_list = []
    if len(sys.argv) == 1 or sys.argv[1] == "help":
        print("Usage: python3 compare.py [MAP_CODE] <g/h> <generation number or list of horses>")
        sys.exit(1)
    
    if sys.argv[1] not in maps:
        if sys.argv[1] != "0":
            print(f"{sys.argv[1]} is not a valid map code.")
            sys.exit(1)
    map_code = sys.argv[1]

    if len(sys.argv) == 2:
        if map_code == "0":
            print(f"==== Comparing Stats for all maps ====")
            most_races = 0
            most_mraces = []
            least_races = 99999
            least_mraces = []
            best_winpercentage = 0.0
            best_wphorse = []
            best_wpmap = []
            worst_winpercentage = 100.0
            worst_wphorse = []
            worst_wpmap = []
            for map in maps:
                conn = sqlite3.connect('./horseraces.db')
                cursor = conn.cursor()
                cursor.execute(f"select count(*) from races where level = '{map}';")
                race_count = cursor.fetchone()[0]
                if race_count > most_races:
                    most_races = race_count
                    most_mraces = [map]
                elif race_count == most_races:
                    most_mraces.append(map)
                if race_count < least_races:
                    least_races = race_count
                    least_mraces = [map]
                elif race_count == least_races:
                    least_mraces.append(map)
                
                for horse_code in gen0:
                    #print(f"Calculating stats for {horse_code} on map {map_names[maps.index(map)]}...")
                    cursor.execute(f"select count(*) from races where level = '{map}' and winningHorse = '{horse_code}';")
                    win_count = cursor.fetchone()[0]
                    cursor.execute(f"select count(*) from races where level = '{map}' and horsesInRace LIKE '%{horse_code}%';")
                    race_count = cursor.fetchone()[0]
                    if race_count > 0:
                        win_percentage = (win_count / race_count * 100)
                        rounded_value = round(win_percentage, 4)
                    else:
                        rounded_value = 0.0
                    #print(f"{horse_code} on {map_names[maps.index(map)]}: win percentage = {rounded_value}% ({win_count} wins out of {race_count} races)")
                    if rounded_value > best_winpercentage:
                        best_winpercentage = rounded_value
                        best_wphorse = [horse_code]
                        best_wpmap = [map]
                    elif rounded_value == best_winpercentage:
                        best_wphorse.append(horse_code)
                        best_wpmap.append(map)
                    if rounded_value < worst_winpercentage:
                        worst_winpercentage = rounded_value
                        worst_wphorse = [horse_code]
                        worst_wpmap = [map]
                    elif rounded_value == worst_winpercentage:
                        worst_wphorse.append(horse_code)
                        worst_wpmap.append(map)
            print(f"Most Races: {most_races} by {most_mraces}")
            print(f"Least Races: {least_races} by {least_mraces}")
            print(f"Best Win Percentage: {best_winpercentage}% by {best_wphorse} on map {best_wpmap}")
            print(f"Worst Win Percentage: {worst_winpercentage}% by {worst_wphorse} on map {worst_wpmap}")

            cursor.execute(f"select id, winningHorse, duration, date, level from races order by duration desc;")
            longest_race_time = cursor.fetchone()[2]
            longest_race_id = cursor.fetchone()[0]
            longest_race_horse = cursor.fetchone()[1]
            longest_race_date = cursor.fetchone()[3]
            longest_race_level = cursor.fetchone()[4]
            print("Longest Race Time:      ", longest_race_time, "by", longest_race_horse, "on", longest_race_date, "in race", longest_race_id, "on map", longest_race_level)
            cursor.execute(f"select id, winningHorse, duration, date, level from races order by duration asc;")
            shortest_race_time = cursor.fetchone()[2]
            shortest_race_id = cursor.fetchone()[0]
            shortest_race_horse = cursor.fetchone()[1]
            shortest_race_date = cursor.fetchone()[3]
            shortest_race_level = cursor.fetchone()[4]
            print("Shortest Race Time:     ", shortest_race_time, "by", shortest_race_horse, "on", shortest_race_date, "in race", shortest_race_id, "on map", shortest_race_level)
            conn.close()
            return
        print("Cannot compare only one map. Use '0' as the map code to compare all maps or use list.py")
        sys.exit(1)

    if sys.argv[2].upper() not in ["G", "H"]:
        print(f"{sys.argv[2]} is not a valid option. Use 'g' for generation or 'h' for horse list.")
        sys.exit(1)
    if sys.argv[2].upper() == "G":
        if sys.argv[3] in generations:
            horse_list = generations[sys.argv[3]]
        else:
            print(f"{sys.argv[3]} is not a valid generation number. Use '0' (for all horses), '1', or '2'.")
            sys.exit(1)
    if sys.argv[2].upper() == "H":
        for i in range(3, len(sys.argv)):
            horse_code = sys.argv[i].upper()
            if horse_code not in horses:
                print(f"{horse_code} is not a valid horse code.")
                sys.exit(1)
            if horse_code == "VOID":
                horse_code = "VOD"
            horse_list.append(horse_code)
    if sys.argv[1] == "0":
        print(f"==== Comparing Stats for {horse_list} on all maps ====")
        best_winpercentage = 0.0
        best_wphorse = []
        worst_winpercentage = 100.0
        worst_wphorse = []
        most_wins = 0
        most_winhorse = []
        least_wins = 9999
        least_winhorse = []
        most_totalraces = 0
        most_racehorse = []
        least_totalraces = 9999
        least_racehorse = []
        most_sincewin = 0
        most_sincewinhorse = []
        for horse_code in horse_list:
            # Connect to the database
            conn = sqlite3.connect('./horseraces.db')
            cursor = conn.cursor()

            #races_participated in
            cursor.execute(f"select count(*) from horsesInRace where horse = '{horse_code}';")
            map_race_count = cursor.fetchone()[0]

            cursor.execute(f"select count(*) from races where winningHorse = '{horse_code}';")
            map_win_count = cursor.fetchone()[0]

            cursor.execute(f"SELECT COUNT(*) FROM races WHERE horsesInRace LIKE '%{horse_code}%' and id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%'); ")
            since_win_count = cursor.fetchone()[0]

            if map_race_count > 0:
                map_win_percentage = (map_win_count / map_race_count * 100)
                rounded_map_value = round(map_win_percentage, 4)
            else:
                map_win_percentage = 0.0
                rounded_map_value = 0.0

            if rounded_map_value > best_winpercentage:
                best_winpercentage = rounded_map_value
                best_wphorse = [horse_code]
            elif rounded_map_value == best_winpercentage:
                best_wphorse.append(horse_code)
            if rounded_map_value < worst_winpercentage:
                worst_winpercentage = rounded_map_value
                worst_wphorse = [horse_code]
            elif rounded_map_value == worst_winpercentage:
                worst_wphorse.append(horse_code)
            if map_win_count > most_wins:
                most_wins = map_win_count
                most_winhorse = [horse_code]
            elif map_win_count == most_wins:
                most_winhorse.append(horse_code)
            if map_win_count < least_wins:
                least_wins = map_win_count
                least_winhorse = [horse_code]
            elif map_win_count == least_wins:
                least_winhorse.append(horse_code)
            if map_race_count > most_totalraces:
                most_totalraces = map_race_count
                most_racehorse = [horse_code]
            elif map_race_count == most_totalraces:
                most_racehorse.append(horse_code)
            if since_win_count > most_sincewin:
                most_sincewin = since_win_count
                most_sincewinhorse = [horse_code]
            elif since_win_count == most_sincewin:
                most_sincewinhorse.append(horse_code)
            conn.close()
        print(f"Best Win Percentage:     {best_winpercentage}% by {best_wphorse}")
        print(f"Worst Win Percentage:    {worst_winpercentage}% by {worst_wphorse}")
        print(f"Most Wins:               {most_wins} by {most_winhorse}")
        print(f"Least Wins:              {least_wins} by {least_winhorse}")
        print(f"Most Races Participated: {most_totalraces} by {most_racehorse}")
        print(f"Longest Since Win:       {most_sincewin} by {most_sincewinhorse}")
        return
        

    print(f"==== Calculating Stats for {horse_list} on map {map_names[maps.index(map_code)]} ====")
    best_winpercentage = 0.0
    best_wphorse = []
    worst_winpercentage = 100.0
    worst_wphorse = []
    most_wins = 0
    most_winhorse = []
    least_wins = 9999
    least_winhorse = []
    most_totalraces = 0
    most_racehorse = []
    least_totalraces = 9999
    least_racehorse = []
    most_sincewin = 0
    most_sincewinhorse = []
    for horse_code in horse_list:
        # Connect to the database
        conn = sqlite3.connect('./horseraces.db')
        cursor = conn.cursor()

        #races_participated in
        cursor.execute(f"select count(*) from horsesInRace where horse = '{horse_code}' and race_id in (select id from races where level = '{map_code}');")
        map_race_count = cursor.fetchone()[0]

        cursor.execute(f"select count(*) from races where winningHorse = '{horse_code}' and level = '{map_code}';")
        map_win_count = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM races WHERE level = '{map_code}' and horsesInRace LIKE '%{horse_code}%' and id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%' and level = '{map_code}'); ")
        since_win_count = cursor.fetchone()[0]

        if map_race_count > 0:
            map_win_percentage = (map_win_count / map_race_count * 100)
            rounded_map_value = round(map_win_percentage, 4)
        else:
            map_win_percentage = 0.0
            rounded_map_value = 0.0

        if rounded_map_value > best_winpercentage:
            best_winpercentage = rounded_map_value
            best_wphorse = [horse_code]
        elif rounded_map_value == best_winpercentage:
            best_wphorse.append(horse_code)
        if rounded_map_value < worst_winpercentage:
            worst_winpercentage = rounded_map_value
            worst_wphorse = [horse_code]
        elif rounded_map_value == worst_winpercentage:
            worst_wphorse.append(horse_code)
        if map_win_count > most_wins:
            most_wins = map_win_count
            most_winhorse = [horse_code]
        elif map_win_count == most_wins:
            most_winhorse.append(horse_code)
        if map_win_count < least_wins:
            least_wins = map_win_count
            least_winhorse = [horse_code]
        elif map_win_count == least_wins:
            least_winhorse.append(horse_code)
        if map_race_count > most_totalraces:
            most_totalraces = map_race_count
            most_racehorse = [horse_code]
        elif map_race_count == most_totalraces:
            most_racehorse.append(horse_code)
        if since_win_count > most_sincewin:
            most_sincewin = since_win_count
            most_sincewinhorse = [horse_code]
        elif since_win_count == most_sincewin:
            most_sincewinhorse.append(horse_code)
        conn.close()
    print(f"Best Win Percentage:     {best_winpercentage}% by {best_wphorse}")
    print(f"Worst Win Percentage:    {worst_winpercentage}% by {worst_wphorse}")
    print(f"Most Wins:               {most_wins} by {most_winhorse}")
    print(f"Least Wins:              {least_wins} by {least_winhorse}")
    print(f"Most Races Participated: {most_totalraces} by {most_racehorse}")
    print(f"Longest Since Win:       {most_sincewin} by {most_sincewinhorse}")


main()