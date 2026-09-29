# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
with io.open(MOD + "\\menus.txt", "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
print("menu_camp def line 48:")
print(lines[48][:400])
print()
print("menu_camp options line 49 (full, split by '.'):")
segs = lines[49].split(".")
for s in segs[:5]:
    print("  [", s.strip()[:120], "]")
print()
# game_menus.csv format
with io.open(MOD + "\\languages\\cns\\game_menus.csv", "r", encoding="utf-8-sig", errors="replace") as f:
    gls = f.read().splitlines()
print("game_menus.csv lines:", len(gls))
for i, l in enumerate(gls[:5]):
    print("  ", l[:120])
# find menu_camp / mno_camp entries
for l in gls:
    if "menu_camp" in l or "mno_camp_action_1" in l:
        print("CAMP ENTRY:", l[:160])
