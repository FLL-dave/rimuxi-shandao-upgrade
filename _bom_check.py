# -*- coding: utf-8 -*-
import io, os
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
BAK = MOD + "\\_rmx_finance_backup"
files = ["strings.txt", "quick_strings.txt", "simple_triggers.txt", "menus.txt",
         "languages\\cns\\game_strings.csv", "languages\\cns\\quick_strings.csv",
         "module.ini"]
def bom(p):
    if not os.path.exists(p):
        return "MISSING"
    with io.open(p, "rb") as f:
        b = f.read(3)
    if b == b"\xef\xbb\xbf":
        return "UTF8+BOM"
    if b == b"\xff\xfe":
        return "UTF16LE"
    if b == b"\xfe\xff":
        return "UTF16BE"
    return "NO-BOM(%s)" % b.hex()
for rel in files:
    cur = MOD + "\\" + rel
    bak = BAK + "\\" + rel.replace("languages\\cns\\", "languages_cns_") + ".bak"
    # backup naming may differ; list backup dir
    print(rel, "-> current:", bom(cur), "| backup:", bom(bak))
print()
print("backup dir listing:")
for n in sorted(os.listdir(BAK))[:40]:
    print("  ", n, bom(os.path.join(BAK, n)))
