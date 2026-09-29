# -*- coding: utf-8 -*-
import io, collections, re

MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\simple_triggers.txt"
with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()

print("total lines:", len(lines))
print("header0:", lines[0][:80])
print("header1:", lines[1][:80])

# collect opcode-ish tokens (first token per line is interval; second maybe num_ops or delay)
samples = []
for i in range(2, min(2 + 30, len(lines))):
    toks = lines[i].split()
    if toks:
        samples.append((i, toks))
for i, toks in samples[:12]:
    print(f"line {i}: len={len(toks)} first={toks[:8]}")
