# -*- coding: utf-8 -*-
"""副本 mod 改名：module_name = Calradia -> Calradia - Finance Way（二进制替换，不动其他字节）。"""
import os
P = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan-finance\module.ini"
with open(P, "rb") as f:
    b = f.read()
old = b"module_name = Calradia"
new = b"module_name = Calradia - Finance Way"
assert old in b, "module_name anchor not found"
b2 = b.replace(old, new, 1)
with open(P, "wb") as f:
    f.write(b2)
print("module.ini renamed")
print(b2.split(b"\n")[0][:80])
