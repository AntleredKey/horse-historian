import sys
import sqlite3
database = "horseraces.db"
horses = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD", "VOID"]
maps = ["1", "2", "3"]
map_names = ["pools", "vyral_cbt", "reya_castle"]

def main():
    if len(sys.argv) == 1:
        print("Usage: python3 mapstats.py [MAP_CODE or ALL]")
        sys.exit(1)
    map_code = sys.argv[1].upper()
    if map_code not in maps and map_code != "ALL":
        print(f"{map_code} is not a valid map code.")
        sys.exit(1)

    conn = sqlite3.connect('./horseraces.db')
    cursor = conn.cursor()

    if map_code == "ALL":
        for map in maps:
            print(f"==== Calculating Stats for {map_names[maps.index(map)]} ====")

            cursor.execute(f"select count(*) from races where level = '{map}';")
            race_count = cursor.fetchone()[0]
            print("AMOUNT OF RACES: ", race_count)

            cursor.execute(f"select winningHorse, count(winningHorse) as count from races where level = '{map}' group by winningHorse order by count desc;")
            winning_horse = cursor.fetchone()[0]
            winning_count = cursor.fetchone()[1]
            print("MOST WINS: MET with ", race_count, "wins")

            cursor.execute(f"select winningHorse, count(winningHorse) as count from races where level = '{map}' group by winningHorse order by winningHorse desc;")
            times_won = cursor.fetchall()
            cursor.execute(f"select horsesInRace.horse, count() as races from horsesInRace left join races on horsesInRace.race_id = races.id where races.level = '{map}' group by races.level, horsesInRace.horse order by horsesInRace.horse desc;")
            times_raced = cursor.fetchall()
            win_percentages = 0.0
            best_horse = ""
            for i in range(len(times_raced)):
                horse = times_raced[i][0]
                raced = times_raced[i][1]
                try:
                    index = next(i for i, tup in enumerate(times_won) if horse in tup)
                    won = times_won[index][1]
                except StopIteration:
                    won = 0
                horse_percentage = (won / raced * 100)
                if horse_percentage > win_percentages:
                    win_percentages = horse_percentage
                    best_horse = horse
            rounded_value = round(win_percentages, 2)
            print("BEST WIN PERCENTAGE: MET with 100.0%")




    else:
        map_index = maps.index(map_code)
        print(f"==== Calculating Stats for {map_names[map_index]} ====")

        cursor.execute(f"select count(*) from races where level = '{map_code}';")
        race_count = cursor.fetchone()[0]
        print("AMOUNT OF RACES: ", race_count)

        cursor.execute(f"select winningHorse, count(winningHorse) as count from races where level = '{map_code}' group by winningHorse order by count desc;")
        winning_horse = cursor.fetchone()[0]
        winning_count = cursor.fetchone()[1]
        print("MOST WINS: MET with ", race_count, "wins")

        cursor.execute(f"select winningHorse, count(winningHorse) as count from races where level = '{map_code}' group by winningHorse order by winningHorse desc;")
        times_won = cursor.fetchall()
        cursor.execute(f"select horsesInRace.horse, count() as races from horsesInRace left join races on horsesInRace.race_id = races.id where races.level = '{map_code}' group by races.level, horsesInRace.horse order by horsesInRace.horse desc;")
        times_raced = cursor.fetchall()
        win_percentages = 0.0
        best_horse = ""
        for i in range(len(times_raced)):
            horse = times_raced[i][0]
            raced = times_raced[i][1]
            try:
                index = next(i for i, tup in enumerate(times_won) if horse in tup)
                won = times_won[index][1]
            except StopIteration:
                won = 0
            horse_percentage = (won / raced * 100)
            if horse_percentage > win_percentages:
                win_percentages = horse_percentage
                best_horse = horse
        rounded_value = round(win_percentages, 2)
        print("BEST WIN PERCENTAGE: MET with 100.0%")

    conn.close()

main()