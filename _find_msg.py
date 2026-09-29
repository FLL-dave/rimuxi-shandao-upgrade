# -*- coding: utf-8 -*-
import io, re
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\scripts.txt"
with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()

toks = lines[7].split()
print("line7 script is 2nd opcode line; decl above:", lines[6][:120])
# find tokens containing 2055/2056
for j, t in enumerate(toks):
    if "2055" in t or "2056" in t:
        print("token", j, "=", t, "ctx:", toks[max(0,j-3):j+4])
# count negative tokens
negs = [t for t in toks if t.startswith("-") and t != "-1"]
print("negative tokens count:", len(negs), "samples:", negs[:10])
