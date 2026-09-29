# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\scripts.txt"
with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()

targets = {"troop_add_gold", "cf_random_political_event", "game_get_money_text", "transfer_gold"}
for i in range(2, len(lines), 2):
    decl = lines[i].split()
    if decl and decl[0] in targets:
        print("=" * 30, decl[0])
        print("decl:", " ".join(decl))
        ops = lines[i+1]
        print("ops len tokens:", len(ops.split()))
        print("ops:", ops[:2600])
