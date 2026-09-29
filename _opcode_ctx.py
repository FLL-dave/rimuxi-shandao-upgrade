# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\scripts.txt"
with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
shown = 0
for ln in lines:
    toks = ln.split()
    for j, t in enumerate(toks):
        if t == "2190":
            print("ctx:", toks[max(0,j-6):j+4])
            shown += 1
            if shown >= 6:
                raise SystemExit
