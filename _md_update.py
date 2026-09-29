# -*- coding: utf-8 -*-
import io
p = r"C:\Users\Administrator\DoubaoWork\chats\2026-09-29\new-chat\rimuxi-shandao\MOD_BASELINE.md"
with io.open(p, "r", encoding="utf-8") as f:
    c = f.read()
old = "| B2 | 商道季结触发器：每 7 天给玩家 +100 两（操作码 1528=troop_add_gold、引用 360287970189639680=trp_player，与 simple_triggers.txt 既有第 140 行用法逐位一致） | simple_triggers.txt（+1，139→140 校验 ✅） | ✅ |"
new = old + "\n| B3 | 商道手册菜单：营地（menu_camp）追加入口\"商道手册\"→ 跳转 menu_rmx_manual（新菜单 id=275，菜单引用 0xC000000000000000+id；操作码 2060=jump_to_menu、2320=str_store_string，与既有 mno_continue/menu_morale_report 模式一致），打开时经 `{s1}` 注入课程要点总览（str_rmx_manual，9 概念×数值，字符串引用编码 0x16000000000000000−str_id） | menus.txt（+2 行，275→276 校验 ✅）、strings.txt（+1，3608→3609 ✅）、game_strings.csv（+1 汉化） | ✅ |"
assert old in c, "anchor not found"
c = c.replace(old, new, 1)
with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(c)
print("MOD_BASELINE.md updated, B3 row added")
