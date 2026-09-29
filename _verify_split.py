# -*- coding: utf-8 -*-
"""校验：副本 rimuxishan-finance 带全部改动；原版已还原干净。"""
import io, os, re
D = r"D:\steam\steamapps\common\MountBlade Warband\Modules"
FIN = D + "\\rimuxishan-finance"
ORG = D + "\\rimuxishan"

def count1(path, which):
    with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = f.read().splitlines()
    if which == "quick":
        return lines[0].split()[0]  # quick_strings.txt: count on FIRST line
    return lines[1].split()[0]

def menu_defs(path):
    with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        return sum(1 for l in f.read().splitlines()[2:] if l.split() and l.split()[0].startswith("menu_"))

def bom(p):
    with open(p, "rb") as f:
        b = f.read(3)
    return "BOM" if b == b"\xef\xbb\xbf" else "noBOM"

for tag, base in [("FINANCE", FIN), ("ORIGINAL", ORG)]:
    print("=" * 8, tag)
    print("  menus decl/defs:", count1(base + "\\menus.txt", "m"), menu_defs(base + "\\menus.txt"))
    print("  strings:", count1(base + "\\strings.txt", "s"))
    print("  quick(first line):", count1(base + "\\quick_strings.txt", "quick"))
    print("  triggers:", count1(base + "\\simple_triggers.txt", "t"))
    for c in ["game_strings", "quick_strings", "game_menus"]:
        print("  %s.csv:" % c, bom(base + "\\languages\\cns\\%s.csv" % c))
# finance has rmx content?
with io.open(FIN + "\\menus.txt", "r", encoding="utf-8", errors="replace") as f:
    fm = f.read()
print("FINANCE has mno_rmx_manual:", "mno_rmx_manual" in fm, "| chinese in menus:", bool(re.search(r"[\u4e00-\u9fff]", fm)))
with io.open(ORG + "\\menus.txt", "r", encoding="utf-8", errors="replace") as f:
    om = f.read()
print("ORIGINAL has mno_rmx_manual:", "mno_rmx_manual" in om, "| chinese in menus:", bool(re.search(r"[\u4e00-\u9fff]", om)))
with io.open(FIN + "\\strings.txt", "r", encoding="utf-8", errors="replace") as f:
    fs = f.read()
print("FINANCE has str_rmx_manual:", "str_rmx_manual" in fs)
with io.open(ORG + "\\strings.txt", "r", encoding="utf-8", errors="replace") as f:
    os_ = f.read()
print("ORIGINAL has str_rmx_manual:", "str_rmx_manual" in os_)
with io.open(FIN + "\\simple_triggers.txt", "r", encoding="utf-8", errors="replace") as f:
    ft = f.read()
print("FINANCE has B2 trigger:", "-7.000000  1  1528 2 360287970189639680 100" in ft)
print("backup dirs:", os.path.isdir(FIN + "\\_rmx_finance_backup"), os.path.isdir(ORG + "\\_rmx_finance_backup"))
