# -*- coding: utf-8 -*-
"""修复骑砍未识别 mod：恢复被改写 csv 的 UTF-8 BOM；menus.txt 中文字段改英文（汉化走 csv）。
被改过的文件：strings.txt/quick_strings.txt/simple_triggers.txt/menus.txt（原状无 BOM，保持）、
game_strings.csv/quick_strings.csv/game_menus.csv（原状带 BOM，恢复）。
"""
import io

MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"

# ---- 1) menus.txt: 中文字段 -> 英文 ----
p = MOD + "\\menus.txt"
with io.open(p, "r", encoding="utf-8", errors="replace") as f:
    c = f.read()
r1 = c.replace("menu_rmx_manual 0 商道手册·金融之道 none 0 0",
               "menu_rmx_manual 0 Merchant's_Manual_-_The_Way_of_Finance none 0 0")
r2 = c.replace(" mno_rmx_manual  0  商道手册  1 2060 1", " mno_rmx_manual  0  Merchant_Manual  1 2060 1")
r3 = c.replace("mno_rmx_manual_back  0  返回  1 2060 1", "mno_rmx_manual_back  0  Back  1 2060 1")
assert r1 != c or r2 != c, "menus.txt chinese not found"
c = c.replace("menu_rmx_manual 0 商道手册·金融之道 none 0 0", "menu_rmx_manual 0 Merchant's_Manual_-_The_Way_of_Finance none 0 0")
c = c.replace(" mno_rmx_manual  0  商道手册  1 2060 1", " mno_rmx_manual  0  Merchant_Manual  1 2060 1")
c = c.replace("mno_rmx_manual_back  0  返回  1 2060 1", "mno_rmx_manual_back  0  Back  1 2060 1")
with io.open(p, "w", encoding="utf-8", newline="") as f:
    f.write(c)
print("menus.txt chinese -> english")

# ---- 2) 恢复三个 csv 的 UTF-8 BOM ----
for rel in ["languages\\cns\\game_strings.csv", "languages\\cns\\quick_strings.csv",
            "languages\\cns\\game_menus.csv"]:
    pp = MOD + "\\" + rel
    with io.open(pp, "r", encoding="utf-8", errors="replace") as f:
        body = f.read()
    with io.open(pp, "w", encoding="utf-8-sig", newline="") as f:
        f.write(body)
    print(rel, "-> UTF-8+BOM restored")

# ---- 3) 校验 ----
def bom(p):
    with io.open(p, "rb") as f:
        b = f.read(3)
    return "UTF8+BOM" if b == b"\xef\xbb\xbf" else "NO-BOM"
for rel in ["menus.txt", "strings.txt", "simple_triggers.txt", "quick_strings.txt",
            "languages\\cns\\game_strings.csv", "languages\\cns\\quick_strings.csv",
            "languages\\cns\\game_menus.csv"]:
    print(rel, bom(MOD + "\\" + rel))

with io.open(MOD + "\\menus.txt", "r", encoding="utf-8", errors="replace") as f:
    mls = f.read().splitlines()
print("menus decl:", mls[1].split()[0], "defs:", sum(1 for l in mls[2:] if l.split() and l.split()[0].startswith("menu_")))
print("rmx menu line:", [l for l in mls if "menu_rmx_manual" in l][0][:110])
print("camp entry:", [l for l in mls if "mno_rmx_manual" in l][0][:110])
