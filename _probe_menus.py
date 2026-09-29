# -*- coding: utf-8 -*-
import io
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\menus.txt"
with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
print("menus.txt lines:", len(lines), "header:", lines[1][:40])

# menu blocks: a menu-def line starts with "menu_"; option lines start with "mno_"/"mno_castle_" etc.
# Menu id = order of menu-def lines (0-based) after header lines.
menu_defs = []
for i, ln in enumerate(lines[2:], start=2):
    toks = ln.split()
    if toks and toks[0].startswith("menu_"):
        menu_defs.append((len(menu_defs), i, toks[0], toks[1] if len(toks) > 1 else ""))
print("menu count:", len(menu_defs))
for mid, lineno, name, flags in menu_defs:
    if name in ("menu_camp", "menu_start_game_0", "menu_town"):
        print("  id:", mid, "line:", lineno, name, "flags:", flags[:40])

# locate menu_camp block lines to append option after its options
for mid, lineno, name, flags in menu_defs:
    if name == "menu_camp":
        # print option lines of camp menu
        print("--- menu_camp block (options):")
        j = lineno + 1
        while j < len(lines):
            toks = lines[j].split()
            if toks and toks[0].startswith("menu_"):
                break
            print("   line", j, ":", lines[j][:110])
            j += 1
        print("next menu line:", j)
