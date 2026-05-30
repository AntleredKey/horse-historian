import sys
import sqlite3
import datetime
horses = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD", "VOID"]
gen0 = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD"]
gen1 = ["DDD", "FLP", "LFS", "MET", "SFE", "WSY"]
gen2 = ["GUN", "LWN", "PSN", "SJU", "SUN", "VOD"]
generations = {"0": gen0, "1": gen1, "2": gen2}
map_codes = [1, 2, 3]
map_names = ["pools", "vyral_cbt", "reya_castle"]
map_dict = {"Pools": "1", "Vyral_CBT": "2", "Reya_Castle": "3"}
dict_map = {1: "Pools", 2: "Vyral_CBT", 3: "Reya_Castle"}

class Horse:
    def __init__(self, name, participate, won, winPercentage, since):
        self.name = name
        self.participate = participate
        self.won = won
        self.winPercentage = winPercentage
        self.since = since

    def __repr__(self):
        return f"{self.name}, {self.participate}, {self.won}, {self.winPercentage}, {self.since}"

class HorseMap:
    def __init__(self, name, mapName, participate, won, winPercentage, since):
        self.name = name
        self.mapName = mapName
        self.participate = participate
        self.won = won
        self.winPercentage = winPercentage
        self.since = since

    def __repr__(self):
        return f"{self.name}, {self.map}, {self.participate}, {self.won}, {self.winPercentage}, {self.since}"


def list(maps, horses_list, settings):
    final_result = []
    map_list = []
    # Convert map names to codes
    for map in maps:
        map_list.append(int(map_dict[map]))

    horse_list = [item.replace("VOID", "VOD") for item in horses_list]
    setYuri = not settings["CountYuri"]
    setMin = settings["MinHorses"]
    setMax = settings["MaxHorses"]

    if setYuri == False:
        final_result.append(f"Calculated with Released Yuri not allowed, between {setMin} and {setMax} Horses")
    else:
        final_result.append(f"Calculated with Released Yuri allowed, between {setMin} and {setMax} Horses")


    # If 0 horses are selected.
    if len(horse_list) == 0:
        # If there are no maps passed in, assume ALL maps.
        if len(maps) == 0:
            #print("no horses or maps selected")
            for map in map_codes:
                result = nohorse(final_result, map, settings)
                #final_result.append(result)
            return ("\n".join(final_result))
        
        # If there are maps passed in, only run those... 
        if len(maps) > 0:
            for map in map_list:
                result = nohorse(final_result, map, settings)
                #final_result.append(result)
            return ("\n".join(final_result))

    # If 0 maps are selected.
    if len(map_list) == 0:
        horse_collection = []
        for horse_code in horse_list:
            result = nomap(final_result, horse_code, settings)
            horse_collection.append(result)
        horse_collection.sort(key=lambda Horse: Horse.winPercentage, reverse=True)
        for horse in horse_collection:
            if horse.participate == 0:
                final_result.append(f"""==== Stats for {horse.name} ====
No races found for search results\n""")
            else:
                final_result.append(f"""==== Stats for {horse.name} ====
Races participated: {horse.participate}
Races won: {horse.won}
Win percentage: {horse.winPercentage}
Since last win: {horse.since} races ago\n""")
        return ("\n".join(final_result))

    # If 2 or more maps are selected.
    if len(map_list) > 0:
        horse_collection = []
        for map_code in map_list:
            for horse_code in horse_list:
                result = maphorse(final_result, map_code, horse_code, settings)
                horse_collection.append(result)
        horse_collection.sort(key=lambda HorseMap: HorseMap.winPercentage, reverse=True)
        for horse in horse_collection:
            if horse.participate == 0:
                final_result.append(f"""==== Stats for {horse.name} on {horse.mapName} ====
No races found for search results\n""")
            else:
                final_result.append(f"""==== Stats for {horse.name} on {horse.mapName} ====
Races participated: {horse.participate}
Races won: {horse.won}
Map Win percentage: {horse.winPercentage}
Since last win: {horse.since} races ago\n""")
        return ("\n".join(final_result))
    return ("Please contact customer support. I have no idea what you did.")

def nohorse(final_result, map, settings):
    setYuri = not settings["CountYuri"]
    setMin = int(settings["MinHorses"])
    setMax = int(settings["MaxHorses"])
    conn = sqlite3.connect('./horseraces.db')
    cursor = conn.cursor()
    map_name = dict_map[map]
    cursor.execute(f"select count(*) from races where level = '{map}' and HorseCount between {setMin} and {setMax};")
    race_count = cursor.fetchone()[0]
    best_wc = 0
    best_wp = 0.0
    least_wc = 99999
    least_wchorse = []
    most_losses = 0
    longest_since_win = 0
    horse_longest_win = []
    best_wphorse = []
    best_wchorse = []
    most_lhorse = []
    for horse_code in gen0:
        cursor.execute(f"select count(winningHorse) as count from races where level = '{map}' and winningHorse like '{horse_code}' and HorseCount between {setMin} and {setMax};")
        winning_count = cursor.fetchone()[0]
        #print(f"{horse_code} has won {winning_count} times on {map_name}")
        cursor.execute(f"select count(*) as races from horsesInRace left join races on horsesInRace.race_id = races.id where races.level = '{map}' and horsesInRace.horse like '{horse_code}' and races.HorseCount between {setMin} and {setMax};")
        raced_count = cursor.fetchone()[0]
        #print(f"{horse_code} raced {raced_count} on {map_name}")
        cursor.execute(f"SELECT COUNT(*) FROM races WHERE level = '{map}' and horsesInRace LIKE '%{horse_code}%' and id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%' and level = '{map}') and HorseCount between {setMin} and {setMax};")
        since_win = cursor.fetchone()[0]
        loss_count = raced_count - winning_count

        if since_win > longest_since_win:
            longest_since_win = since_win
            horse_longest_win = horse_code
        if raced_count == 0 or winning_count == 0:
            rounded_value = 0.0
        else:
            win_percentage = (winning_count / raced_count * 100)
            rounded_value = round(win_percentage, 2)

        if rounded_value > best_wp:
            best_wp = rounded_value
            best_wphorse = [horse_code]
        elif rounded_value == best_wp:
            best_wphorse.append(horse_code)
            
        if winning_count < least_wc:
            least_wc = winning_count
            least_wchorse = [horse_code]
        elif winning_count == least_wc:
            least_wchorse.append(horse_code)
        if winning_count > best_wc:
            best_wc = winning_count
            best_wchorse = [horse_code]
        elif winning_count == best_wc:
            best_wchorse.append(horse_code)

        if loss_count > most_losses:
            most_losses = loss_count
            most_lhorse = [horse_code]
        elif loss_count == most_losses:
            most_lhorse.append(horse_code)

    if race_count == 0:
        final_result.append(f"""==== Stats for {map_name} ====
No races found for search results\n""")
        return(final_result)
    cursor.execute(f"select id, winningHorse, duration, date from races where level = '{map}' and HorseCount between {setMin} and {setMax} order by duration desc;")
    longest_race_id, longest_race_horse, longest_race_time, longest_race_date = cursor.fetchone()
    formatted_longest_race_time = datetime.timedelta(seconds=longest_race_time)
    str_lrt = str(formatted_longest_race_time)
    cursor.execute(f"select id, winningHorse, duration, date from races where level = '{map}' and HorseCount between {setMin} and {setMax} order by duration asc;")
    shortest_race_id, shortest_race_horse, shortest_race_time, shortest_race_date = cursor.fetchone()
    formatted_shortest_race_time = datetime.timedelta(seconds=shortest_race_time)
    str_srt = str(formatted_shortest_race_time)
    
    final_result.append(f"""==== Stats for {map_name} ====
Amount of Races: {race_count}
Highest Win Percentage: {best_wphorse} with {best_wp}%
Most Wins: {best_wchorse} with {best_wc}
Least Wins: {least_wchorse} with {least_wc}
Most Losses: {most_lhorse} with {most_losses}
Longest Since Win: {horse_longest_win} with {longest_since_win} races
Longest Race Time: {str_lrt[2:10]} by {longest_race_horse} on {longest_race_date} in race {longest_race_id}
Shortest Race Time: {str_srt[2:10]} by {shortest_race_horse} on {shortest_race_date} in race {shortest_race_id}\n""")
    return(final_result)

def nomap(final_result, horse_code, settings):
    setYuri = not settings["CountYuri"]
    setMin = int(settings["MinHorses"])
    setMax = int(settings["MaxHorses"])
    conn = sqlite3.connect('./horseraces.db')
    cursor = conn.cursor()

    #final_result.append(f"==== Stats for {horse_code} ====")

    # Number of races participated by the horse
    cursor.execute(f"select count(*) from horsesInRace left join races on horsesInRace.race_id = races.id where horsesInRace.horse = '{horse_code}' and races.HorseCount between {setMin} and {setMax};")
    race_count = cursor.fetchone()[0]
    #final_result.append(f"Races participated: {race_count}")

    # Number of races won by the horse
    cursor.execute(f"select count(*) from horsesInRace left join races on horsesInRace.race_id = races.id where horsesInRace.horse = '{horse_code}' and horsesInRace.wonRace = 1 and races.HorseCount between {setMin} and {setMax};")
    win_count = cursor.fetchone()[0]
    #final_result.append(f"Races won: {win_count}")

    # Overall win percentage
    if race_count > 0:
        win_percentage = (win_count / race_count * 100)
        rounded_value = round(win_percentage, 2)
        #final_result.append(f"Win percentage: {rounded_value}%")
    else:
        rounded_value = 0

    # Last win X races ago
    cursor.execute(f"SELECT COUNT(*) FROM races WHERE id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%') and HorseCount between {setMin} and {setMax}; ")
    since_count = cursor.fetchone()[0]
    #final_result.append(f"Since last win: {since_count} races ago\n")
    conn.close()
    return Horse(horse_code, race_count, win_count, rounded_value, since_count)

def maphorse(final_result, map_code, horse_code, settings):
    setYuri = not settings["CountYuri"]
    setMin = int(settings["MinHorses"])
    setMax = int(settings["MaxHorses"])
    conn = sqlite3.connect('./horseraces.db')
    cursor = conn.cursor()

    map_name = dict_map[map_code]
    #final_result.append(f"==== Calculating Stats for {horse_code} on {map_name} ====")

    cursor.execute(f"select count(*) from horsesInRace left join races on horsesInRace.race_id = races.id where horsesInRace.horse = '{horse_code}' and horsesInRace.race_id in (select id from races where level = '{map_code}') and races.HorseCount between {setMin} and {setMax};")
    map_race_count = cursor.fetchone()[0]
    #final_result.append(f"Races participated: {map_race_count}")

    cursor.execute(f"select count(*) from races where winningHorse = '{horse_code}' and level = '{map_code}' and HorseCount between {setMin} and {setMax};")
    map_win_count = cursor.fetchone()[0]
    #final_result.append(f"Races won: {map_win_count}")

    # Win percentage on this specific map
    if map_race_count > 0:
        map_win_percentage = (map_win_count / map_race_count * 100)
        rounded_value = round(map_win_percentage, 4)
        #final_result.append(f"Map Win Percentage: {rounded_value}%")
    else:
        rounded_value = 0

    cursor.execute(f"SELECT COUNT(*) FROM races WHERE level = '{map_code}' and horsesInRace LIKE '%{horse_code}%' and id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%' and level = '{map_code}') and HorseCount between {setMin} and {setMax}; ")
    since_win_count = cursor.fetchone()[0]
    #final_result.append(f"Since last win: {since_win_count} races ago\n")
    conn.close()
    return HorseMap(horse_code, map_name, map_race_count, map_win_count, rounded_value, since_win_count)