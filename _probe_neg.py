# -*- coding: utf-8 -*-
import io, re
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
for rel in ["scripts.txt", "simple_triggers.txt"]:
    p = MOD + "\\" + rel
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    toks = text.split()
    print("=" * 20, rel, "tokens:", len(toks))
    hits = 0
    for j in range(len(toks) - 3):
        if toks[j] == "1528" and toks[j+1] == "2" and toks[j+3].startswith("-"):
            print("  negative 1528 at", j, ":", toks[j:j+4])
            hits += 1
    print("negative-1528 hits:", hits)
    # also count 1529 (get gold) usages
    c = 0
    for j in range(len(toks) - 2):
        if toks[j] == "1529":
            c += 1
    print("1529 count:", c)
