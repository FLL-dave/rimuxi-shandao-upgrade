# -*- coding: utf-8 -*-
"""金融之道 mod 实改 B2：机制层最小件——商道季结触发器
simple_triggers.txt 追加：每 7 天给玩家 +100 两（复用 mod 自身 troop_add_gold 操作码 1528 与 trp_player 引用）。
只追加不改行；更新头部计数行；校验计数。"""
import io

MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\simple_triggers.txt"

# 追加行：interval=-7（每7天） num_ops=1  opcode 1528 (troop_add_gold) args(trp_player_ref=0x500000000000000, amount=100)
new_line = "-7.000000  1  1528 2 360287970189639680 100"

with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
    content = f.read()
if not content.endswith("\n"):
    content += "\n"
lines = content.splitlines(keepends=True)

# 更新计数行（第 1 行）
hdr = lines[1].rstrip("\r\n")
old = int(hdr.split()[0])
lines[1] = hdr.replace(str(old), str(old + 1), 1) + "\n"
lines.append(new_line + "\n")

with io.open(path, "w", encoding="utf-8", newline="") as f:
    f.writelines(lines)

# 校验
with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
    ls = f.read().splitlines()
n_decl = int(ls[1].split()[0])
entries = sum(1 for l in ls[2:] if l.strip())
print("decl:", n_decl, "entries:", entries, "ok:", n_decl == entries)
print("new trigger line:", ls[-1][:120])
print("lines total:", len(ls))
