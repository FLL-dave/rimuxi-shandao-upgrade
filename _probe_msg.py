# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
with io.open(MOD + "\\scripts.txt", "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
# scripts: line0 version, line1 count, then pairs (decl line, opcode line)
print("scripts decl:", lines[1][:20])
candidates = []
for i in range(2, len(lines), 2):
    decl = lines[i]
    name = decl.split()[0]
    low = name.lower()
    if any(k in low for k in ("message", "notif", "inform", "report", "talk", "dialog", "conversation")):
        candidates.append((i, name, decl.split()[1] if len(decl.split()) > 1 else "", lines[i+1]))
print("message-related scripts:", len(candidates))
for i, name, nops, ops in candidates[:12]:
    toks = ops.split()
    print(" ", name, "num:", nops, "ops[:14]:", toks[:14])
