# -*- coding: utf-8 -*-
import io, re
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
with io.open(MOD + "\\menus.txt", "r", encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
# find menu def lines with " none 0 " or ending " none 0"
for i in range(2, len(lines), 2):
    ln = lines[i]
    if re.search(r" none 0(\s|$)", ln):
        print("line", i, ":", ln[:260])
        if i > 100:
            break
