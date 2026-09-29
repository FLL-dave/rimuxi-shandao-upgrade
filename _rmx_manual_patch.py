# -*- coding: utf-8 -*-
"""金融之道 mod 实改 B3 增强：商道手册页显示课程要点总览
1) strings.txt 追加 str_rmx_manual（id 3608）
2) game_strings.csv 追加汉化
3) menus.txt 更新 menu_rmx_manual 行：{s1} + ops 2320 2 1 <str_ref>
字符串引用编码 = 0x16000000000000000 - str_id（与既有 2320 用法一致）
"""
import io

MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"
STR_BASE = 1585267068834415616  # 0x16000000000000000
MANUAL_ID = 3608
MANUAL_REF = STR_BASE - MANUAL_ID

manual_en = ("Merchant's_Manual_-_The_Way_of_Finance:^^"
             "1._Risk_&_Insurance:_escort_premium_6%,_payout_80%.^^"
             "2._Risk_Premium:_route_risks_8%/15%/30%.^^"
             "3._Leverage:_bank_interest_10%_per_season.^^"
             "4._Futures_&_Hedging:_forward_contract_at_0.95_of_spot.^^"
             "5._Diversification:_north_assets_devalue_to_60%.^^"
             "6._Bubble_&_Speculation:_land_300_buy_/450_sell_/100_crash.^^"
             "7._Inflation:_paper_money_crisis_-15%_silver.^^"
             "8._Behavioral_Finance:_grain_market_herd_+/-25%.^^"
             "9._Fiscal_Crisis:_three_surtaxes_sell_price_x0.93.^^"
             "Rule:_The_dynasty_will_fall,_but_a_merchant_who_manages_risk_survives.")

manual_cn = ("掌柜手册·金融之道：^"
             "1. 风险与保险：镖局保费六分，被劫赔付八成。^"
             "2. 风险溢价：商路风险低8%/中15%/高30%。^"
             "3. 杠杆：钱庄借贷季利一成。^"
             "4. 期货与对冲：青苗预售锁价=市价九五折。^"
             "5. 分散化：北方资产终局按六成折算。^"
             "6. 泡沫与投机：炒地300买450卖，两季崩盘只剩100。^"
             "7. 货币与通胀：宝钞风波现银损失一成五。^"
             "8. 行为金融：米市羊群效应，米价背离±25%。^"
             "9. 财政危机：三饷加派，天下卖价×0.93。^"
             "记住：王朝会覆灭，但懂得风险管理的商人能活下来。")

# ---- 1) strings.txt ----
p = MOD + "\\strings.txt"
with io.open(p, "r", encoding="utf-8-sig", errors="replace") as f:
    content = f.read()
if not content.endswith("\n"):
    content += "\n"
lines = content.splitlines(keepends=True)
hdr = lines[1].rstrip("\r\n")
old = int(hdr.split()[0])
assert old == 3608, "unexpected strings count %d" % old
lines[1] = hdr.replace(str(old), str(old + 1), 1) + "\n"
lines.append("str_rmx_manual %s\n" % manual_en)
with io.open(p, "w", encoding="utf-8", newline="") as f:
    f.writelines(lines)
print("strings.txt +str_rmx_manual id=%d" % MANUAL_ID)

# ---- 2) game_strings.csv ----
p = MOD + "\\languages\\cns\\game_strings.csv"
with io.open(p, "r", encoding="utf-8-sig", errors="replace") as f:
    c = f.read()
if not c.endswith("\n"):
    c += "\n"
clines = c.splitlines(keepends=True)
clines.append("str_rmx_manual|%s\n" % manual_cn)
with io.open(p, "w", encoding="utf-8", newline="") as f:
    f.writelines(clines)
print("game_strings.csv +str_rmx_manual")

# ---- 3) menus.txt update menu_rmx_manual def line ----
p = MOD + "\\menus.txt"
with io.open(p, "r", encoding="utf-8-sig", errors="replace") as f:
    m = f.read()
if not m.endswith("\n"):
    m += "\n"
mlines = m.splitlines(keepends=True)
target = None
for i, ln in enumerate(mlines):
    if ln.rstrip("\r\n").split()[:1] == ["menu_rmx_manual"]:
        target = i
        break
assert target is not None
mlines[target] = "menu_rmx_manual 0 {s1} none 0 1 2320 2 1 %d\n" % MANUAL_REF
with io.open(p, "w", encoding="utf-8", newline="") as f:
    f.writelines(mlines)
print("menus.txt menu_rmx_manual updated")

# ---- 4) 校验 ----
with io.open(MOD + "\\strings.txt", "r", encoding="utf-8-sig", errors="replace") as f:
    sls = f.read().splitlines()
s_decl = int(sls[1].split()[0])
s_entries = sum(1 for l in sls[2:] if l.strip())
print("strings decl/entries/ok:", s_decl, s_entries, s_decl == s_entries)
print("last string:", sls[-1][:80])
with io.open(MOD + "\\menus.txt", "r", encoding="utf-8-sig", errors="replace") as f:
    mls = f.read().splitlines()
m_decl = int(mls[1].split()[0])
m_defs = sum(1 for l in mls[2:] if l.split() and l.split()[0].startswith("menu_"))
print("menus decl/defs/ok:", m_decl, m_defs, m_decl == m_defs)
print("rmx menu line:", [l for l in mls if l.split()[:1] == ["menu_rmx_manual"]][0][:120])
