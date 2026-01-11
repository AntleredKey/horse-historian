import sys
import sqlite3
database = "horseraces.db"
horses = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD", "VOID"]

def main():
    if len(sys.argv) == 1:
        print("Usage: python3 singlehorse.py [HORSE_CODE]")
        sys.exit(1)
    horse_code = sys.argv[1].upper()
    if horse_code not in horses:
        print(f"{horse_code} is not a valid horse code.")
        sys.exit(1)
    if horse_code == "VOID":
        horse_code = "VOD"
    print("==== Calculating Stats for", horse_code, "====")

    # Connect to the database
    conn = sqlite3.connect('./horseraces.db')
    cursor = conn.cursor()

    # Number of races participated by the horse
    cursor.execute(f"select count(*) from horsesInRace where horse = '{horse_code}';")
    race_count = cursor.fetchone()[0]
    print("Races participated:", race_count)
    # Number of races won by the horse
    cursor.execute(f"select count(*) from horsesInRace where horse = '{horse_code}' and wonRace = 1;")
    win_count = cursor.fetchone()[0]
    print("Races won:", win_count)
    # Overall win percentage
    if race_count > 0:
        win_percentage = (win_count / race_count * 100)
        rounded_value = round(win_percentage, 4)
        print("Win percentage:", rounded_value, "%")
    # Last win X races ago
    cursor.execute(f"SELECT COUNT(*) FROM races WHERE id > (SELECT MAX(id) FROM races WHERE winningHorse LIKE '%{horse_code}%'); ")
    win_count = cursor.fetchone()[0]
    print("Last won", win_count, "races ago")


main()