# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
for rel in ["game_variables.txt", "variables.txt"]:
    p = MOD + "\\" + rel
    with io.open(p, "r", encoding="utf-8-sig", errors="replace") as f:
        ls = f.read().splitlines()
    print("=" * 20, rel, "| lines:", len(ls))
    for i, l in enumerate(ls[:8]):
        print(i, "|", l[:120])
    if len(ls) > 10:
        print("...last:")
        for i, l in enumerate(ls[-5:]):
            print(len(ls)-5+i, "|", l[:120])
