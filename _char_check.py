# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
# check & and ^^ usage in original strings (backup = pristine) vs current
for rel in ["strings.txt", "quick_strings.txt"]:
    bak = MOD + "\\_rmx_finance_backup\\" + rel + ".bak"
    with io.open(bak, "r", encoding="utf-8", errors="replace") as f:
        b = f.read()
    with io.open(MOD + "\\" + rel, "r", encoding="utf-8", errors="replace") as f:
        c = f.read()
    print(rel, "backup amp:", b.count("&"), "caret2:", b.count("^^"), "| current amp:", c.count("&"), "caret2:", c.count("^^"))
    print("  backup has double-caret sample:", "^^" in b)
# my added strings
with io.open(MOD + "\\strings.txt", "r", encoding="utf-8", errors="replace") as f:
    c = f.read()
i = c.find("str_rmx_manual")
print("my str_rmx_manual:", c[i:i+80].replace("\n", "\\n"))
