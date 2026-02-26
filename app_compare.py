import sys
import sqlite3
horses = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD", "VOID"]
gen0 = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD"]
gen1 = ["DDD", "FLP", "LFS", "MET", "SFE", "WSY"]
gen2 = ["GUN", "LWN", "PSN", "SJU", "SUN", "VOD"]
generations = {"0": gen0, "1": gen1, "2": gen2}
map_codes = [1, 2, 3]
map_names = ["pools", "vyral_cbt", "reya_castle"]
map_dict = {"Pools": "1", "Vyral_CBT": "2", "Reya_Castle": "3"}
dict_map = {1: "Pools", 2: "Vyral_CBT", 3: "Reya_Castle"}

def compare(maps, horses_list):
    map_list = []
    # Convert map names to codes
    for map in maps:
        map_list.append(int(map_dict[map]))

    horse_list = [item.replace("VOID", "VOD") for item in horses_list]

    # If 0 horses are selected.
    if len(horse_list) == 0:
        if len(map_list) == 0:
            print("wahoo")
            longest_since = 0
            horse_ls = []
            conn = sqlite3.connect('./horseraces.db')
            cursor = conn.cursor()
            cursor.execute(f"select count(*) from races;")
            total_races = cursor.fetchone()[0]
            cursor.execute(f"select horse, count(*) as count from horsesInRace group by horse order by count desc;")
            horse_mp, most_participated = cursor.fetchone()
            cursor.execute(f"select horse, count(*) as count from horsesInRace where wonRace = 1 group by horse order by count desc;")
            horse_mw, most_wins = cursor.fetchone()
            cursor.execute(f"select horse, count(*) as count from horsesInRace where wonRace = 1 group by horse order by count asc limit 1;")
            horse_lw, least_wins = cursor.fetchone()

            cursor.execute(f"select horse, count(*) as count from horsesInRace where wonRace = 0 group by horse order by count desc;")
            horse_ml, most_losses = cursor.fetchone()
            for horse_code in gen0:
                cursor.execute(f"SELECT COUNT(*) FROM races WHERE horsesInRace LIKE '%{horse_code}%' and id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%');")
                since_win = cursor.fetchone()[0]
                if since_win > longest_since:
                    longest_since = since_win
                    horse_ls = [horse_code]
                elif since_win == longest_since:
                    horse_ls.append(horse_code)
            str1 = f"Total Races: {total_races}\n"
            str2 = f"Most Races Participated: {horse_mp} with {most_participated}\n"
            str3 = f"Most Wins: {horse_mw} with {most_wins}\n"
            str4 = f"Least Wins: {horse_lw} with {least_wins}\n"
            str5 = f"Most Losses: {horse_ml} with {most_losses}\n"
            str6 = f"Longest Since Win: {horse_ls} with {longest_since} races"
            return (str1 + str2 + str3 + str4 + str5 + str6)
        if len(map_list) == 1:
            return ("Cannot compare only 1 map.\nPlease select multiple or use List.")
        if len(map_list) > 1:
            most_races = 0
            most_mraces = []
            least_races = 99999
            least_mraces = []
            best_winpercentage = 0.0
            best_wphorse = []
            best_wpmap = []
            best_wp = []
            worst_winpercentage = 100.0
            worst_wphorse = []
            worst_wpmap = []
            worst_wp = []
            longest_race_time = 0.0
            longest_race_id = ""
            longest_race_horse = ""
            longest_race_date = ""
            longest_race_level = ""
            shortest_race_time = 99999.9
            shortest_race_id = ""
            shortest_race_horse = ""
            shortest_race_date = ""
            shortest_race_level = ""
            conn = sqlite3.connect('./horseraces.db')
            cursor = conn.cursor()
            for map in map_list:
                map_name = dict_map[map]
                cursor.execute(f"select count(*) from races where level = '{map}';")
                race_count = cursor.fetchone()[0]
                if race_count > most_races:
                    most_races = race_count
                    most_mraces = [map_name]
                elif race_count == most_races:
                    most_mraces.append(map_name)
                if race_count < least_races:
                    least_races = race_count
                    least_mraces = [map_name]
                elif race_count == least_races:
                    least_mraces.append(map_name)

                cursor.execute(f"select id, winningHorse, duration, date from races where level = '{map}' order by duration desc;")
                maplongest_ri, maplongest_rh, maplongest_rt, maplongest_rd = cursor.fetchone()

                rounded_maplongest_rt = round(maplongest_rt, 2)
                if rounded_maplongest_rt > longest_race_time:
                    longest_race_time = rounded_maplongest_rt
                    longest_race_id = maplongest_ri
                    longest_race_horse = maplongest_rh
                    longest_race_date = maplongest_rd
                    longest_race_level = map_name
                cursor.execute(f"select id, winningHorse, duration, date from races where level = '{map}' order by duration asc;")

                mapshortest_ri, mapshortest_rh, mapshortest_rt, mapshortest_rd = cursor.fetchone()

                mapshortest_rt = round(mapshortest_rt, 2)
                rounded_mapshortest_rt = round(mapshortest_rt, 2)
                if rounded_mapshortest_rt < shortest_race_time:
                    shortest_race_time = rounded_mapshortest_rt
                    shortest_race_id = mapshortest_ri
                    shortest_race_horse = mapshortest_rh
                    shortest_race_date = mapshortest_rd
                    shortest_race_level = map_name
                
                for horse_code in gen0:
                    #print(f"Calculating stats for {horse_code} on map {map_names[maps.index(map)]}...")
                    cursor.execute(f"select count(*) from races where level = '{map}' and winningHorse = '{horse_code}';")
                    win_count = cursor.fetchone()[0]
                    cursor.execute(f"select count(*) from races where level = '{map}' and horsesInRace LIKE '%{horse_code}%';")
                    race_count = cursor.fetchone()[0]
                    if race_count > 0:
                        win_percentage = (win_count / race_count * 100)
                        rounded_value = round(win_percentage, 2)
                    else:
                        rounded_value = 0.0
                    #print(f"{horse_code} on {map_names[maps.index(map)]}: win percentage = {rounded_value}% ({win_count} wins out of {race_count} races)")
                    if rounded_value > best_winpercentage:
                        best_winpercentage = rounded_value
                        best_wp = [f"{horse_code} on {map_name}"]
                        best_wphorse = [horse_code]
                        best_wpmap = [map_name]
                    elif rounded_value == best_winpercentage:
                        best_wphorse.append(horse_code)
                        best_wpmap.append(map_name)
                        best_wp.append(f"{horse_code} on {map_name}")
                    if rounded_value < worst_winpercentage:
                        worst_winpercentage = rounded_value
                        worst_wphorse = [horse_code]
                        worst_wpmap = [map]
                        worst_wp = [f"{horse_code} on {map_name}"]
                    elif rounded_value == worst_winpercentage:
                        worst_wphorse.append(horse_code)
                        worst_wpmap.append(map)
                        worst_wp.append(f"{horse_code} on {map_name}")
            conn.close()

            str1 = f"Map Raced on the Most: {most_mraces} with {most_races} races\n"
            str2 = f"Map Raced on the Least: {least_mraces} with {least_races} races\n"
            str3 = f"Best Win Percentage: {best_winpercentage}% by {best_wp}\n"
            str4 = f"Worst Win Percentage: {worst_winpercentage}% by {worst_wp}\n"
            str5 = f"Longest Race Time: {longest_race_time}s by {longest_race_horse} on {longest_race_date} in race {longest_race_id} on {longest_race_level}\n"
            str6 = f"Shortest Race Time: {shortest_race_time}s by {shortest_race_horse} on {shortest_race_date} in race {shortest_race_id} on {shortest_race_level}"

            return (str1 + str2 + str3 + str4 + str5 + str6)
        return ("Please contact customer support. I have no idea what you did.")

    # If 0 maps are selected.
    if len(map_list) == 0:
        # 0 horses and 0 maps are on line 21
        if len(horse_list) == 1:
                return ("Only one horse selected!\nSelect multiple horses, or use List.")
        if len(horse_list) < 1:
            #print(f"==== Comparing Stats for {horse_list} on all maps ====")
            best_wp = 0.0
            horse_bwp = []
            worst_wp = 100.0
            horse_wwp = []
            most_wins = 0
            horse_mw = []
            least_wins = 9999
            horse_lw = []
            most_totalraces = 0
            most_racehorse = []
            longest_since = 0
            horse_ls = []
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

                if rounded_map_value > best_wp:
                    best_wp = rounded_map_value
                    horse_bwp = [horse_code]
                elif rounded_map_value == best_wp:
                    horse_bwp.append(horse_code)
                if rounded_map_value < worst_wp:
                    worst_wp = rounded_map_value
                    horse_wwp = [horse_code]
                elif rounded_map_value == worst_wp:
                    horse_wwp.append(horse_code)
                if map_win_count > most_wins:
                    most_wins = map_win_count
                    horse_mw = [horse_code]
                elif map_win_count == most_wins:
                    horse_mw.append(horse_code)
                if map_win_count < least_wins:
                    least_wins = map_win_count
                    horse_lw = [horse_code]
                elif map_win_count == least_wins:
                    horse_lw.append(horse_code)
                if map_race_count > most_totalraces:
                    most_totalraces = map_race_count
                    most_racehorse = [horse_code]
                elif map_race_count == most_totalraces:
                    most_racehorse.append(horse_code)
                if since_win_count > longest_since:
                    longest_since = since_win_count
                    horse_ls = [horse_code]
                elif since_win_count == longest_since:
                    horse_ls.append(horse_code)
                conn.close()
            
            str1 = f"Most Wins: {most_wins} by {horse_mw}\n"
            str2 = f"Best Win Percentage: {best_wp}% by {horse_bwp}\n"
            str3 = f"Least Wins: {least_wins} by {horse_lw}\n"
            str4 = f"Worst Win Percentage: {worst_wp}% by {horse_wwp}\n"
            str5 = f"Most Races Participated: {most_totalraces} by {most_racehorse}\n"
            str6 = f"Longest Since Win: {longest_since} by {horse_ls}"

            return (str1 + str2 + str3 + str4 + str5 + str6)
        return ("Please contact customer support. I have no idea what you did.")

    # If 1 map is selected.
    if len(map_list) == 1:
        if len(horse_list) == 1:
            return ("Only one horse selected!\nSelect multiple horses, or use List.")
        if len(horse_list) > 1:
            #print(f"==== Calculating Stats for {horse_list} on map {map_names[maps.index(map_list)]} ====")
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
                cursor.execute(f"select count(*) from horsesInRace where horse = '{horse_code}' and race_id in (select id from races where level = '{map_list[0]}');")
                map_race_count = cursor.fetchone()[0]

                cursor.execute(f"select count(*) from races where winningHorse = '{horse_code}' and level = '{map_list[0]}';")
                map_win_count = cursor.fetchone()[0]

                cursor.execute(f"SELECT COUNT(*) FROM races WHERE level = '{map_list[0]}' and horsesInRace LIKE '%{horse_code}%' and id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%' and level = '{map_list[0]}'); ")
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
            
            best_winpercentage_str = f"Best Win Percentage: {best_winpercentage}% by {best_wphorse}\n"
            worst_winpercentage_str = f"Worst Win Percentage: {worst_winpercentage}% by {worst_wphorse}\n"
            most_wins_str = f"Most Wins: {most_wins} by {most_winhorse}\n"
            least_wins_str = f"Least Wins: {least_wins} by {least_winhorse}\n"
            most_races_str = f"Most Races Participated: {most_totalraces} by {most_racehorse}\n"
            longest_since_str = f"Longest Since Win: {most_sincewin} by {most_sincewinhorse}"
            return (best_winpercentage_str + worst_winpercentage_str + most_wins_str + least_wins_str + most_races_str + longest_since_str)
        return ("Please contact customer support. I have no idea what you did.")
    
    # If 2 or more maps are selected.
    if len(map_list) > 1:
        if len(horse_list) == 1:
            horse_code = horse_list[0]
            best_wp = 0.0
            horse_bwp = []
            worst_wp = 100.0
            horse_wwp = []
            most_wins = 0
            horse_mw = []
            least_wins = 9999
            horse_lw = []
            most_totalraces = 0
            most_racehorse = []
            longest_since = 0
            horse_ls = []
            for map_code in map_list:
                # Connect to the database
                conn = sqlite3.connect('./horseraces.db')
                cursor = conn.cursor()
                map_name = dict_map[map_code]

                #races_participated in
                cursor.execute(f"select count(*) from horsesInRace left join races on races.id = horsesInRace.race_id where horsesInRace.horse = '{horse_code}' and races.level = '{map_code}';")
                map_race_count = cursor.fetchone()[0]

                cursor.execute(f"select count(*) from races where winningHorse = '{horse_code}' and level = '{map_code}';")
                map_win_count = cursor.fetchone()[0]

                cursor.execute(f"SELECT COUNT(*) FROM races WHERE level = '{map_code}' and horsesInRace LIKE '%{horse_code}%' and id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%' and level = '{map_code}');")
                since_win_count = cursor.fetchone()[0]

                if map_race_count > 0:
                    map_win_percentage = (map_win_count / map_race_count * 100)
                    rounded_map_value = round(map_win_percentage, 4)
                else:
                    map_win_percentage = 0.0
                    rounded_map_value = 0.0

                if rounded_map_value > best_wp:
                    best_wp = rounded_map_value
                    horse_bwp = [map_name]
                elif rounded_map_value == best_wp:
                    horse_bwp.append(map_name)
                if rounded_map_value < worst_wp:
                    worst_wp = rounded_map_value
                    horse_wwp = [map_name]
                elif rounded_map_value == worst_wp:
                    horse_wwp.append(map_name)
                if map_win_count > most_wins:
                    most_wins = map_win_count
                    horse_mw = [map_name]
                elif map_win_count == most_wins:
                    horse_mw.append(map_name)
                if map_win_count < least_wins:
                    least_wins = map_win_count
                    horse_lw = [map_name]
                elif map_win_count == least_wins:
                    horse_lw.append(map_name)
                if map_race_count > most_totalraces:
                    most_totalraces = map_race_count
                    most_racehorse = [map_name]
                elif map_race_count == most_totalraces:
                    most_racehorse.append(map_name)
                if since_win_count > longest_since:
                    longest_since = since_win_count
                    horse_ls = [map_name]
                elif since_win_count == longest_since:
                    horse_ls.append(map_name)
                conn.close()
            
            str1 = f"Most Wins: {most_wins} on {horse_mw}\n"
            str2 = f"Best Win Percentage: {best_wp}% on {horse_bwp}\n"
            str3 = f"Least Wins: {least_wins} on {horse_lw}\n"
            str4 = f"Worst Win Percentage: {worst_wp}% on {horse_wwp}\n"
            str5 = f"Most Races Participated: {most_totalraces} on {most_racehorse}\n"
            str6 = f"Longest Since Win: {longest_since} on {horse_ls}"

            return (str1 + str2 + str3 + str4 + str5 + str6)  
        if len(horse_list) > 1:
            print("yippee but more")
            best_wp = 0.0
            horse_bwp = []
            worst_wp = 100.0
            horse_wwp = []
            most_wins = 0
            horse_mw = []
            least_wins = 9999
            horse_lw = []
            most_totalraces = 0
            most_racehorse = []
            longest_since = 0
            horse_ls = []
            for horse_code in horse_list:
                for map_code in map_list:
                    conn = sqlite3.connect('./horseraces.db')
                    cursor = conn.cursor()
                    # Connect to the database
                    map_name = dict_map[map_code]
                    horsemap_name = f"{horse_code} on {map_name}"

                    #races_participated in
                    cursor.execute(f"select count(*) from horsesInRace left join races on races.id = horsesInRace.race_id where horsesInRace.horse = '{horse_code}' and races.level = '{map_code}';")
                    map_race_count = cursor.fetchone()[0]

                    cursor.execute(f"select count(*) from races where winningHorse = '{horse_code}' and level = '{map_code}';")
                    map_win_count = cursor.fetchone()[0]

                    cursor.execute(f"SELECT COUNT(*) FROM races WHERE level = '{map_code}' and horsesInRace LIKE '%{horse_code}%' and id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%' and level = '{map_code}');")
                    since_win_count = cursor.fetchone()[0]

                    if map_race_count > 0:
                        map_win_percentage = (map_win_count / map_race_count * 100)
                        rounded_map_value = round(map_win_percentage, 4)
                    else:
                        map_win_percentage = 0.0
                        rounded_map_value = 0.0

                    if rounded_map_value > best_wp:
                        best_wp = rounded_map_value
                        horse_bwp = [horsemap_name]
                    elif rounded_map_value == best_wp:
                        horse_bwp.append(horsemap_name)
                    if rounded_map_value < worst_wp:
                        worst_wp = rounded_map_value
                        horse_wwp = [horsemap_name]
                    elif rounded_map_value == worst_wp:
                        horse_wwp.append(horsemap_name)
                    if map_win_count > most_wins:
                        most_wins = map_win_count
                        horse_mw = [horsemap_name]
                    elif map_win_count == most_wins:
                        horse_mw.append(horsemap_name)
                    if map_win_count < least_wins:
                        least_wins = map_win_count
                        horse_lw = [horsemap_name]
                    elif map_win_count == least_wins:
                        horse_lw.append(horsemap_name)
                    if map_race_count > most_totalraces:
                        most_totalraces = map_race_count
                        most_racehorse = [horsemap_name]
                    elif map_race_count == most_totalraces:
                        most_racehorse.append(horsemap_name)
                    if since_win_count > longest_since:
                        longest_since = since_win_count
                        horse_ls = [horsemap_name]
                    elif since_win_count == longest_since:
                        horse_ls.append(horsemap_name)
                conn.close()
            str1 = f"Most Wins: {most_wins} on {horse_mw}\n"
            str2 = f"Best Win Percentage: {best_wp}% on {horse_bwp}\n"
            str3 = f"Least Wins: {least_wins} on {horse_lw}\n"
            str4 = f"Worst Win Percentage: {worst_wp}% on {horse_wwp}\n"
            str5 = f"Most Races Participated: {most_totalraces} on {most_racehorse}\n"
            str6 = f"Longest Since Win: {longest_since} on {horse_ls}"
            return (str1 + str2 + str3 + str4 + str5 + str6)