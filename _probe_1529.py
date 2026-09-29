# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\simple_triggers.txt"
with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
for i, ln in enumerate(lines):
    toks = ln.split()
    for j, t in enumerate(toks):
        if t == "1529":
            print("line", i, "interval:", toks[0], "num_ops:", toks[1])
            print("   ctx:", toks[max(0,j-8):j+10])
            print()
