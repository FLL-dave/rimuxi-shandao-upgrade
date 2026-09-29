# -*- coding: utf-8 -*-
import io, collections
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
with io.open(MOD + "\\languages\\cns\\game_strings.csv", "r", encoding="utf-8-sig", errors="replace") as f:
    ls = f.read().splitlines()
keys = [l.split("|")[0] for l in ls if l.strip() and "|" in l]
c = collections.Counter(keys)
dups = [k for k, v in c.items() if v > 1]
print("duplicate keys:", len(dups))
for k in dups[:20]:
    print("  ", k, "x", c[k])
rmx = [k for k in dups if "rmx" in k]
print("rmx dup:", rmx)
