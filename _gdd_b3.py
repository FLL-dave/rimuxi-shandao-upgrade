# -*- coding: utf-8 -*-
import subprocess
content = (
    '<p><b>B3 商道手册菜单：</b>营地（menu_camp）新增入口"商道手册"→ 跳转新菜单 menu_rmx_manual（menus.txt +2，275→276 ✅），打开时经 {s1} 注入课程要点总览 str_rmx_manual（strings.txt +1，3608→3609 ✅，9 概念×数值，双语汉化已同步）；操作码 2060（jump_to_menu）/ 2320（str_store_string）与既有 mno_continue / menu_morale_report 模式逐位同构；可复现包 _rmx_menu_patch.py / _rmx_manual_patch.py 已入 git（e0bcd5b）。</p>'
)
cmd = ["lark-cli", "docs", "+update", "--doc", "Ms3XdtPKto1S1BxWJ7Vc45hynhd",
       "--command", "block_insert_after",
       "--block-id", "doxcnKMsuv4XAzuplRbZK43sX7f",
       "--content", content]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
print("RC:", r.returncode)
print(r.stdout[:1200])
if r.stderr:
    print("ERR:", r.stderr[:400])
