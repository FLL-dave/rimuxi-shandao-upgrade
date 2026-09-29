# -*- coding: utf-8 -*-
import io, re

MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\scripts.txt"

with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    text = f.read()

tokens = text.split()
assert tokens[0] == "scriptsfile" and tokens[1] == "version"
n = int(tokens[3])
print("script count:", n)

scripts = []
idx = 4
try:
    for i in range(n):
        name = tokens[idx]; idx += 1
        np = int(tokens[idx]); idx += 1
        params = tokens[idx:idx+np]; idx += np
        ops = []
        while idx < len(tokens):
            t = tokens[idx]
            if t == "0":
                idx += 1
                break
            ops.append(t)
            idx += 1
            if len(ops) > 5000:
                break
        scripts.append((name, np, params, ops))
except IndexError:
    print("BREAK at script index", i, "idx", idx, "name-so-far", name if 'name' in dir() else '?')
    raise
print("parsed:", len(scripts), "idx-end:", idx, "tokens-left:", len(tokens) - idx)
keys = ("merchant", "price", "trade", "gold", "denar", "player", "season", "day", "time", "msg", "message", "bank", "loan", "interest", "insurance", "rmx", "week")
for name, np, params, ops in scripts:
    low = name.lower()
    if any(k in low for k in keys):
        head = " ".join(ops[:14])
        print(f"  {name} params={np} {params} | {head}")
