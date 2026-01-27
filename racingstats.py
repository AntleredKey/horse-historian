import sys
import sqlite3
database = "horseraces.db"
horses = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD", "VOID"]
gen0 = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD"]
gen1 = ["DDD", "FLP", "LFS", "MET", "SFE", "WSY"]
gen2 = ["GUN", "LWN", "PSN", "SJU", "SUN", "VOD"]
generations = {"0": gen0, "1": gen1, "2": gen2}
maps = ["1", "2", "3"]
map_names = ["pools", "vyral_cbt", "reya_castle"]

def main():
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
        if sys.argv[3] not in range(len(generations) + 1):
            print(f"{sys.argv[3]} is not a valid generation number. Use '0' (for ALL), '1', or '2'.")
            sys.exit(1)


    horse_code = sys.argv[1].upper()
    if horse_code not in horses:
        print(f"{horse_code} is not a valid horse code.")
        sys.exit(1)
    if horse_code == "VOID":
        horse_code = "VOD"

    # Connect to the database
    conn = sqlite3.connect('./horseraces.db')
    cursor = conn.cursor()

    if len(sys.argv) == 2:
        print(f"==== Calculating Stats for {horse_code} ====")

        # Number of races participated by the horse
        cursor.execute(f"select count(*) from horsesInRace where horse = '{horse_code}';")
        race_count = cursor.fetchone()[0]
        print("Races participated: ", race_count)

        # Number of races won by the horse
        cursor.execute(f"select count(*) from horsesInRace where horse = '{horse_code}' and wonRace = 1;")
        win_count = cursor.fetchone()[0]
        print("Races won:          ", win_count)

        # Overall win percentage
        if race_count > 0:
            win_percentage = (win_count / race_count * 100)
            rounded_value = round(win_percentage, 4)
            print("Win percentage:     ", rounded_value, "%")

        # Last win X races ago
        cursor.execute(f"SELECT COUNT(*) FROM races WHERE id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%'); ")
        win_count = cursor.fetchone()[0]
        print("Last won:           ", win_count, "races ago")

    if len(sys.argv) == 3:
        map_code = sys.argv[2]
        if map_code not in maps:
            print(f"{map_code} is not a valid map code.")
            sys.exit(1)
        else:
            map_index = maps.index(map_code)
            print(f"==== Calculating Stats for {horse_code} on {map_names[map_index]} ====")

            cursor.execute(f"select count(*) from horsesInRace where horse = '{horse_code}' and race_id in (select id from races where level = '{map_code}');")
            map_race_count = cursor.fetchone()[0]
            print(f"Races participated:  {map_race_count}")

            cursor.execute(f"select count(*) from races where winningHorse = '{horse_code}' and level = '{map_code}';")
            map_win_count = cursor.fetchone()[0]
            print(f"Races won:          ", map_win_count)

            # Win percentage on this specific map
            if map_race_count > 0:
                map_win_percentage = (map_win_count / map_race_count * 100)
                rounded_value = round(map_win_percentage, 4)
                print("Map Win Percentage: ", rounded_value, "%")

    conn.close()

main()