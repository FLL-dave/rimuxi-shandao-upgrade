# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
for rel in ["hints.txt", "languages\\cns\\hints.csv"]:
    p = MOD + "\\" + rel
    with io.open(p, "r", encoding="utf-8-sig", errors="replace") as f:
        ls = f.read().splitlines()
    print("=" * 20, rel, "| lines:", len(ls))
    for i, l in enumerate(ls[:4]):
        print(i, "|", l[:150])
    print("...last:")
    for i, l in enumerate(ls[-3:]):
        print(len(ls)-3+i, "|", l[:150])
