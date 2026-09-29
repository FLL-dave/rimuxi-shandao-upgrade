# -*- coding: utf-8 -*-
"""金融之道 mod 实改 B3：商道手册菜单（营地入口 + 手册页）
menus.txt 追加 menu_rmx_manual（id=275）+ 在 menu_camp 选项行尾部插入入口选项。
操作码 2060=jump_to_menu(1参, menu 引用 0xC000000000000000+i)，与既有 mno_continue 逐位同构。
"""
import io

MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
menus_path = MOD + "\\menus.txt"
csv_path = MOD + "\\languages\\cns\\game_menus.csv"

MENU_CAMP_ID = 23
NEW_MENU_ID = 275
BASE = 864691128455135488  # 0xC000000000000000
camp_ref = BASE + MENU_CAMP_ID
new_ref = BASE + NEW_MENU_ID

# ---- 1) menus.txt ----
with io.open(menus_path, "r", encoding="utf-8-sig", errors="replace") as f:
    content = f.read()
if not content.endswith("\n"):
    content += "\n"
lines = content.splitlines(keepends=True)

# 更新计数行（第 1 行 " 275"）
hdr = lines[1].rstrip("\r\n")
old = int(hdr.split()[0])
assert old == 275, "unexpected menu count %d" % old
lines[1] = hdr.replace(str(old), str(old + 1), 1) + "\n"

# 在 menu_camp 选项行（紧跟 menu_camp 定义行之后）行尾插入入口选项
camp_def_idx = None
for i, ln in enumerate(lines):
    if ln.rstrip("\r\n").split()[:1] == ["menu_camp"]:
        camp_def_idx = i
        break
assert camp_def_idx is not None, "menu_camp not found"
opt_idx = camp_def_idx + 1
entry = " mno_rmx_manual  0  商道手册  1 2060 1 %d ." % new_ref
lines[opt_idx] = lines[opt_idx].rstrip("\r\n") + entry + "\n"

# 文件尾追加新菜单块（menu 定义行 + 选项行）
lines.append("menu_rmx_manual 0 商道手册·金融之道 none 0 0\n")
lines.append("mno_rmx_manual_back  0  返回  1 2060 1 %d .\n" % camp_ref)

with io.open(menus_path, "w", encoding="utf-8", newline="") as f:
    f.writelines(lines)
print("menus.txt patched")

# ---- 2) game_menus.csv 汉化 ----
with io.open(csv_path, "r", encoding="utf-8-sig", errors="replace") as f:
    ccontent = f.read()
if not ccontent.endswith("\n"):
    ccontent += "\n"
clines = ccontent.splitlines(keepends=True)
clines.append("menu_rmx_manual|商 道 · 金 融 之 道\n")
clines.append("mno_rmx_manual|商 道 手 册\n")
clines.append("mno_rmx_manual_back|返 回\n")
with io.open(csv_path, "w", encoding="utf-8", newline="") as f:
    f.writelines(clines)
print("game_menus.csv patched")

# ---- 3) 校验 ----
with io.open(menus_path, "r", encoding="utf-8-sig", errors="replace") as f:
    mls = f.read().splitlines()
n_decl = int(mls[1].split()[0])
menu_defs = sum(1 for l in mls[2:] if l.split() and l.split()[0].startswith("menu_"))
print("menus decl:", n_decl, "menu_defs:", menu_defs, "ok:", n_decl == menu_defs)
print("camp option line tail:", mls[camp_def_idx + 1][-120:])
print("new menu block:", mls[-2][:80], "||", mls[-1][:80])
