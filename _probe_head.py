# -*- coding: utf-8 -*-
import io, sys

MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"

def lines(path, n):
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        return [f.readline().rstrip("\r\n") for _ in range(n)]

for f, cnt in [("scripts.txt", 4), ("simple_triggers.txt", 4), ("strings.txt", 3),
               ("quick_strings.txt", 3), ("menus.txt", 4), ("game_strings.csv", 3)]:
    p = MOD + "\\" + f
    ls = lines(p, cnt)
    print("=" * 20, f)
    for i, l in enumerate(ls):
        print(i, "|", l[:220])
