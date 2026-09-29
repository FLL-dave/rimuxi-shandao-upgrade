# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
with io.open(MOD + "\\menus.txt", "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
for i, ln in enumerate(lines):
    toks = ln.split()
    if toks and toks[0] in ("menu_morale_report", "menu_party_size_report", "menu_courtship_relations"):
        print("line", i, ":", ln[:500])
        print("options line", i+1, ":", lines[i+1][:200])
        print()
