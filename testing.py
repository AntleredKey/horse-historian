import sys
import sqlite3
database = "horseraces.db"
horses = ["FLP", "DDD", "WSY", "MET", "LFS", "SFE", "GUN", "LWN", "SUN", "PSN", "SJU", "VOD", "VOID"]

def main():
    if len(sys.argv) == 1:
        print("Usage: python3 singlehorse.py [HORSE_CODE]")
        sys.exit(1)
    print(sys.argv[1])
    print(sys.argv[2])

main()