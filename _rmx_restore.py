# -*- coding: utf-8 -*-
"""将 _rmx_finance_backup\*.bak 还原到原版 mod 目录（恢复改动前状态）。"""
import io, os, shutil
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
BAK = MOD + "\\_rmx_finance_backup"
CNS = MOD + "\\languages\\cns"

TOP = ["menus.txt", "strings.txt", "quick_strings.txt", "simple_triggers.txt",
       "scripts.txt", "module.ini"]
CSVS = ["dialogs", "factions", "game_menus", "game_strings", "hints", "info_pages",
        "item_kinds", "item_modifiers", "parties", "party_templates", "quests",
        "quick_strings", "skills", "skins", "troops", "ui"]

restored = []
for name in TOP:
    src = os.path.join(BAK, name + ".bak")
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(MOD, name))
        restored.append(name)
for name in CSVS:
    src = os.path.join(BAK, name + ".csv.bak")
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(CNS, name + ".csv"))
        restored.append(name + ".csv")
print("restored:", len(restored))
print("  ", ", ".join(restored))

# 校验原版计数
def head_count(path):
    with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = f.read().splitlines()
    return lines[1].split()[0]
print("menus:", head_count(os.path.join(MOD, "menus.txt")),
      "strings:", head_count(os.path.join(MOD, "strings.txt")),
      "quick:", head_count(os.path.join(MOD, "quick_strings.txt")),
      "triggers:", head_count(os.path.join(MOD, "simple_triggers.txt")))
