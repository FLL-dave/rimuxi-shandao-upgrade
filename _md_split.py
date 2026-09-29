# -*- coding: utf-8 -*-
import io
p = r"C:\Users\Administrator\DoubaoWork\chats\2026-09-29\new-chat\rimuxi-shandao\MOD_BASELINE.md"
with io.open(p, "r", encoding="utf-8") as f:
    c = f.read()
anchor = "## 六、P0 实改清单（对应飞书 GDD 第 7 章）"
add = (
    "## 五·五、副本化（用户要求：不改原版）\n\n"
    "所有实改（B1 文本 / B2 季结触发器 / B3 商道手册菜单）已整体迁移至独立副本 "
    "`D:\\steam\\steamapps\\common\\MountBlade Warband\\Modules\\rimuxishan-finance`：\n\n"
    "- 原版 `rimuxishan` 已从 `_rmx_finance_backup\\*.bak` 完整还原（menus 275 / strings 3580 / quick 1132 / triggers 139，无任何 rmx 改动）；原版备份目录已清除。\n"
    "- 副本 `rimuxishan-finance`：menus 276 / strings 3609 / quick 1137 / triggers 140，三个汉化 csv 带 UTF-8 BOM，含全部金融之道改动；module.ini 更名 `module_name = Calradia - Finance Way`（启动器显示新名，存档独立，需新开档）；副本自带 `_rmx_finance_backup`（22 个原文件快照，回滚源）。\n"
    "- 教训：直接改原版 txt 有 BOM 丢失风险（csv 必须 UTF-8 BOM）；menus.txt 内直接写中文字段也可能引发引擎解析问题，中文字段一律走 csv 汉化。\n\n"
)
assert anchor in c
c = c.replace(anchor, add + anchor, 1)
with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(c)
print("MOD_BASELINE.md updated with 副本化 section")
