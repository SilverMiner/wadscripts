#
# 6.9.2024 18:13 Sergey "SilverMiner" Burow
#
# A script to count Doom 2 item counts in a WAD.
# requires omgifol
# I tested it with Python 3.7.7
# Personally I used it in a batch file like this:
# python.exe ^
# wadcountitems.py plut3lev.wad > plut3levCI.txt
#

import sys
from omg import WAD, HeaderGroup
from omg.mapedit import MapEditor

COUNTITEMS = [2013,2014,2015,2022,2023,2024,2026,83,2045]

if (len(sys.argv) < 2):
    print("\n    Count items in a WAD script:\n")
    print("    Usage:")
    print("    wadcountitems.py input.wad\n")
else:
    wa = sys.argv[1]
    a = WAD(wa)
    if not isinstance(a.maps, HeaderGroup):
        raise Exception("No maps in the WAD")
    for maplump in a.maps:
        editor = MapEditor(a.maps[maplump])
        ice,icn,ich=0,0,0
        for thing in editor.things:
            if thing.type not in COUNTITEMS:
                continue
            if thing.easy:
                ice+=1
            if thing.medium:
                icn+=1
            if thing.hard:
                ich+=1
        print(maplump, ice, icn, ich)

