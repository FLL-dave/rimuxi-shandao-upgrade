# -*- coding: utf-8 -*-
import io, re
from collections import Counter
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
with io.open(MOD + "\\simple_triggers.txt", "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
# header: line0 version, line1 count; triggers from line2
ivs = Counter()
for ln in lines[2:]:
    t = ln.split()
    if t:
        ivs[t[0]] += 1
print("interval distribution (top):")
for k, v in ivs.most_common(15):
    print("  ", k, v)
# does mod have negative intervals?
neg = [k for k in ivs if k.startswith("-")]
print("negative intervals:", neg)
# print last trigger (B2 added) to verify
print("last line:", lines[-1][:80])
# menus: verify mno_rmx_manual entry text
with io.open(MOD + "\\menus.txt", "r", encoding="utf-8", errors="replace") as f:
    m = f.read()
i = m.find("mno_rmx_manual")
print("menus mno_rmx_manual ctx:", m[i-60:i+100].replace("\n", " | "))
