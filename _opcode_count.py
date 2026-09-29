# -*- coding: utf-8 -*-
import io, collections
MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
path = MOD + "\\scripts.txt"
with io.open(path, "r", encoding="utf-8", errors="replace") as f:
    text = f.read()
toks = text.split()
# count candidate message/call opcodes as standalone tokens
cands = ["2050","2051","2052","2053","2054","2055","2056","2057","2058","2059","2060","2138","2139","2190","2320","2321","2322","2323","1528","1529","600"]
cnt = collections.Counter(toks)
for c in cands:
    if cnt[c]:
        print(c, "x", cnt[c])
