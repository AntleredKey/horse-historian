import sys
import sqlite3
database = "horseraces.db"
horses = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD", "VOID"]
gen0 = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD"]
gen1 = ["DDD", "FLP", "LFS", "MET", "SFE", "WSY"]
gen2 = ["GUN", "LWN", "PSN", "SJU", "SUN", "VOD"]
horse_list = []
generations = {"0": gen0, "1": gen1, "2": gen2}
maps = ["1", "2", "3"]
map_names = ["pools", "vyral_cbt", "reya_castle"]

def main():
    horse_list = []
    if len(sys.argv) == 1 or sys.argv[1] == "help" or len(sys.argv) < 4:
        print("Usage: python3 racingstats.py [MAP_CODE] [g/h] [generation number or list of horses]")
        sys.exit(1)
    if sys.argv[1] not in maps:
        print(f"{sys.argv[1]} is not a valid map code.")
        sys.exit(1)
    map_code = sys.argv[1]
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