import sys
import sqlite3
import datetime
file_path = "weekly.txt"
result = []
dict_map = {1: "Pools", 2: "Vyral_CBT", 3: "Reya_Castle"}

def main():
    if len(sys.argv) == 1 or sys.argv[1] == "help":
        print("Usage: python3 weekly.py [yyyy-mm-dd]")
        sys.exit(1)
    
    date_input = sys.argv[1]

    conn = sqlite3.connect('./horseraces.db')
    cursor = conn.cursor()
    cursor.execute(f"select id, date, winningHorse, duration, level from races where date >= '{date_input}';")
    races = cursor.fetchall()
    for id, date, horse, duration, level in races:
        cursor.execute(f"select duration from races where level = {level} and id < {id} order by duration asc limit 1;")
        shortest_historical = cursor.fetchone()[0]
        if duration < shortest_historical:
            td = datetime.timedelta(seconds=duration)
            formatted_time = str(td)
            result.append(f"{date} - {horse} with a time of {formatted_time[2:10]} on {dict_map[level]}, WORLD RECORD!!\n")
        else:
            td = datetime.timedelta(seconds=duration)
            formatted_time = str(td)
            result.append(f"{date} - {horse} with a time of {formatted_time[2:10]} on {dict_map[level]}\n")
    print(f"Pulled {len(result)} races")

    try:
        # Open the file in 'w' (write) mode; creates the file if it doesn't exist.
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("".join(result))
        print(f"File '{file_path}' created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

main()
