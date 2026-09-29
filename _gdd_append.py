# -*- coding: utf-8 -*-
import subprocess

content = (
    '<h1 seq="auto">知识融合图谱与在线试玩</h1>'
    '<p>课程概念、大明机制与 mod 挂载点的三层对应链见下图；本图数值均来自原型权威配置与模拟实测。</p>'
    '<p><b>在线试玩入口：</b>'
    '<a href="https://fll-dave.github.io/rimuxi-shandao-upgrade/rimuxi-shandao.html">日暮西山 · 商道（原型 Demo）</a>'
    '　|　'
    '<a href="https://fll-dave.github.io/rimuxi-shandao-upgrade/zhishi-graph.html">知识融合图谱</a></p>'
    '<p><b>源码仓库：</b>'
    '<a href="https://github.com/FLL-dave/rimuxi-shandao-upgrade">github.com/FLL-dave/rimuxi-shandao-upgrade</a>'
    '（原型、模拟引擎、设计契约、mod 基线全部托管，建模内容即代码）</p>'
    '<p>同验收版本单文件原型与图谱附于本页：</p>'
    '<source path="@./zhishi-graph.html" name="知识融合图谱.html"/>'
    '<source path="@./rimuxi-shandao.html" name="日暮西山·商道原型.html"/>'
)

cmd = ["lark-cli", "docs", "+update", "--doc", "Ms3XdtPKto1S1BxWJ7Vc45hynhd",
       "--command", "append", "--content", content]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
print("RC:", r.returncode)
print("STDOUT:", r.stdout[:1200])
print("STDERR:", r.stderr[:600])
