import sqlite3
database = "horseraces.db"
horses = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD"]

print("ran code!")

def main():
    conn = sqlite3.connect('./horseraces.db')
    cursor = conn.cursor()

    cursor.execute("SELECT max(id) FROM races;")
    races_max = cursor.fetchone()[0]
    print("max race id:", races_max)

    cursor.execute("SELECT max(race_id) from horsesInRace;")
    hir_max = cursor.fetchone()[0]
    print("max horsesInRace race_id:", hir_max)

    if races_max > hir_max:
        print("Missing Race!")
        for horse in horses:
            print(horse)
            cursor.execute(
                "INSERT INTO horsesInRace (race_id, horse) "
                "SELECT id, ? FROM races WHERE horsesInRace LIKE ? AND id > ?;",
                (horse, f"%{horse}%", hir_max)
            )
            conn.commit()

        cursor.execute(
            "UPDATE horsesInRace "
            "SET wonRace = 1 "
            "WHERE horse = (SELECT winningHorse FROM races WHERE races.id = horsesInRace.race_id);"
        )
        cursor.execute("UPDATE horsesInRace SET wonRace = 0 WHERE wonRace IS NULL;")
        conn.commit()

    conn.close()

main()