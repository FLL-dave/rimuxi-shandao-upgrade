# -*- coding: utf-8 -*-
import subprocess

content = (
    '<h1 seq="auto">实改进度（mod 文件已改动）</h1>'
    '<p><b>B0 备份：</b>全部目标文件已备份至 mod 目录 _rmx_finance_backup\\*.bak，回滚即还原。</p>'
    '<table><colgroup><col width="70"/><col width="260"/><col width="300"/><col width="190"/></colgroup>'
    '<thead><tr><th><p>轮次</p></th><th><p>内容</p></th><th><p>文件与校验</p></th><th><p>状态</p></th></tr></thead><tbody>'
    '<tr><td><p>B1</p></td><td><p>金融之道文本资产：8 季报、6 希勒卡、8 事件、6 体检点评、5 快速消息（str_rmx_*/qstr_rmx_*）</p></td>'
    '<td><p>strings.txt +28（计数 3580→3608 ✅）、quick_strings.txt +5（1132→1137 ✅）、game_strings.csv +28 汉化（key 无冲突）、quick_strings.csv +5 汉化</p></td><td><p>✅ 已完成</p></td></tr>'
    '<tr><td><p>B2</p></td><td><p>商道季结触发器：每 7 天给玩家 +100 两</p></td>'
    '<td><p>simple_triggers.txt +1（139→140 ✅）；操作码 1528（troop_add_gold）与玩家引用 360287970189639680 与 mod 既有第 140 行逐位一致</p></td><td><p>✅ 已完成</p></td></tr>'
    '</tbody></table>'
    '<p><b>待游戏内验证：</b>P0-3 青苗合约、P0-4 投保赔付、P0-5 国运事件价格冲击、P0-6 希勒课堂弹窗——txt 无编译期检查，需启动游戏逐项实测（消息操作码 2190 为三参数变体，语义确认后使用）；可复现实改包（_rmx_text_patch.py / _rmx_trigger_patch.py）已入 git 仓库。</p>'
)

cmd = ["lark-cli", "docs", "+update", "--doc", "Ms3XdtPKto1S1BxWJ7Vc45hynhd",
       "--command", "append", "--content", content]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
print("RC:", r.returncode)
print("STDOUT:", r.stdout[:800])
print("STDERR:", r.stderr[:300])
