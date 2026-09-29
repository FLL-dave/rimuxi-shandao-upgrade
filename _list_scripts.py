# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\scripts.txt"
with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()

names = []
for i in range(2, len(lines), 2):
    decl = lines[i].split()
    if decl:
        names.append(decl[0])

print("scripts:", len(names))
keys = ("gold", "money", "pay", "reward", "gift", "msg", "notice", "event", "week", "day_", "season", "interest", "loan", "tax", "price", "merchant")
hits = [n for n in names if any(k in n.lower() for k in keys)]
print("hits:", len(hits))
for n in hits:
    print("  ", n)
