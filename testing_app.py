import sys, os
from app_updatedb import updatedb
from app_compare import compare
from app_list import list

def main():
    listPassed = 0
    listFailed = []
    comparePassed = 0
    compareFailed = []
    settingsDict = {
            'CountYuri': True,
            'MinHorses': 1,
            'MaxHorses': 12
        }

    print("Running App Test...")
    m0h0L = list([], [], settingsDict)
    if m0h0L[15:20] == "Pools":
        listPassed += 1
    else:
        listFailed.append("m0h0")
    
    m2h0L = list(["Pools", "Vyral_CBT"], [], settingsDict)
    if m2h0L[15:20] == "Pools":
        listPassed += 1
    else:
        listFailed.append("m2h0")

    m2h2L = list(["Pools", "Vyral_CBT"], ["LFS", "VOID"], settingsDict)
    if m2h2L[5:10] == "Stats":
        listPassed += 1
    else:
        listFailed.append("m2h2")

    m0h2L = list([], ["LFS", "VOID"], settingsDict)
    if m0h2L[5:10] == "Stats":
        listPassed += 1
    else:
        listFailed.append("m0h2")
    
    print(f"List Functions Passed: {listPassed}/4")
    if len(listFailed) != 0:
        print(f"List Functions Failed: {listFailed}")

    m0h0C = compare([], [], settingsDict)
    if m0h0C[:5] == "Total":
        x = 1
        comparePassed += 1
    else:
        compareFailed.append("m0h0")

    m1h0C = compare(["Pools"], [], settingsDict)
    if m1h0C[:6] == "Cannot":
        x = 1
        comparePassed += 1
    else:
        compareFailed.append("m1h0")
    
    m2h0C = compare(["Pools", "Vyral_CBT"], [], settingsDict)
    if m2h0C[:3] == "Map":
        comparePassed += 1
    else:
        compareFailed.append("m2h0")

    m0h1C = compare([], ["MET"], settingsDict)
    if m0h1C[:6] == "Cannot":
        comparePassed += 1
    else:
        compareFailed.append("m0h1")
    
    m0h2C = compare([], ["LFS", "VOID"], settingsDict)
    if m0h2C[:4] == "Most":
        comparePassed += 1
    else:
        compareFailed.append("m0h2")

    m1h1C = compare(["Pools"], ["MET"], settingsDict)
    if m1h1C[:6] == "Cannot":
        x = 1
        comparePassed += 1
    else:
        compareFailed.append("m1h1")

    m1h2C = compare(["Pools"], ["LFS", "VOID"], settingsDict)
    if m1h2C[:4] == "Best":
        x = 1
        comparePassed += 1
    else:
        compareFailed.append("m1h2")

    m2h1C = compare(["Pools", "Vyral_CBT"], ["LFS"], settingsDict)
    if m2h1C[:4] == "Most":
        x = 1
        comparePassed += 1
    else:
        compareFailed.append("m2h1")

    m2h2C = compare(["Pools", "Vyral_CBT"], ["LFS", "VOID"], settingsDict)
    if m2h2C[:4] == "Most":
        x = 1
        comparePassed += 1
    else:
        compareFailed.append("m2h2")
    


    print(f"List Functions Passed: {comparePassed}/9")
    if len(compareFailed) != 0:
        print(f"List Functions Failed: {compareFailed}")

    

main()
