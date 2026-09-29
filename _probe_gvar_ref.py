# -*- coding: utf-8 -*-
import io, collections
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\scripts.txt"
with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    text = f.read()
toks = text.split()
cnt = collections.Counter(toks)
# standard global var base 0x208000 = 2129920
print("2129920 count:", cnt.get("2129920", 0))
# sample tokens around 2129920
for j, t in enumerate(toks):
    if t == "2129920":
        print("ctx:", toks[max(0,j-3):j+4])
        break
# check presence of values 2129920..2129920+20
for v in range(2129920, 2129941):
    if cnt.get(str(v)):
        print("  var token found:", v)
