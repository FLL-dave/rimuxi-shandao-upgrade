# -*- coding: utf-8 -*-
"""金融之道 mod 实改 B1：文本资产层追加（strings/quick_strings/汉化 csv）
追加式、不改既有行、同步头部计数行、末行校验。"""
import io, sys

MOD = r"D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan"

# ---------- 内容定义 ----------
# strings.txt 默认文本（英文，空格用下划线）
str_defs = [
    ("str_rmx_season_1",  "Season_1_Chongzhen_16_Spring:  You_begin_in_Beijing_with_1,000_taels."),
    ("str_rmx_season_2",  "Season_2_Chongzhen_16_Summer:  The_markets_shift._Watch_the_price_gaps."),
    ("str_rmx_season_3",  "Season_3_Chongzhen_16_Autumn:  Bandits_ravage_the_Central_Plains!"),
    ("str_rmx_season_4",  "Season_4_Chongzhen_16_Winter:  Prices_keep_moving._Manage_your_risk."),
    ("str_rmx_season_5",  "Season_5_Chongzhen_17_Spring:  Li_Zicheng_breaches_Beijing!_The_capital_collapses."),
    ("str_rmx_season_6",  "Season_6_Chongzhen_17_Summer:  The_dynasty_falters._A_merchant_must_endure."),
    ("str_rmx_season_7",  "Season_7_Chongzhen_17_Autumn:  The_Manchu_enter_the_pass!_North_assets_devalue."),
    ("str_rmx_season_8",  "Season_8_Chongzhen_17_Winter:  Final_assessment_of_your_trade_and_knowledge."),
    ("str_rmx_card_insurance",   "Risk_and_Insurance:_a_premium_turns_a_large_loss_into_a_small_cost._Ming_escort_guilds,_modern_insurance_companies."),
    ("str_rmx_card_riskpremium", "Risk_Premium:_a_riskier_trade_route_must_offer_higher_returns_to_compensate."),
    ("str_rmx_card_leverage",    "Leverage:_borrowing_amplifies_gains_and_losses._10%_seasonal_interest_is_the_price."),
    ("str_rmx_card_futures",     "Futures_and_Hedging:_sell_unripe_grain_forward_to_lock_price_and_transfer_risk."),
    ("str_rmx_card_diversify",   "Diversification:_war_in_the_north,_profit_in_the_south._Never_put_all_eggs_in_one_basket."),
    ("str_rmx_card_bubble",      "Bubble_and_Speculation:_buy_at_300,_sell_at_450,_worth_100_if_you_hold_two_seasons."),
    ("str_rmx_evt_liukou",   "Event:_Bandits_ravage_the_Central_Plains._Grain_prices_surge,_route_risk_rises."),
    ("str_rmx_evt_pojing",   "Event:_Beijing_has_fallen!_Capital_prices_collapse."),
    ("str_rmx_evt_ruguan",   "Event:_The_Manchu_enter_the_pass._Northern_prices_fall,_north_assets_devalue."),
    ("str_rmx_evt_sanxiang", "Event:_Three_Surtaxes_imposed._Sell_prices_x0.93_across_the_realm."),
    ("str_rmx_evt_baochao",  "Event:_Paper_money_crisis!_15%_of_your_silver_evaporates."),
    ("str_rmx_evt_chadi",    "Event:_Land_speculation_in_Jiangnan._Bubble,_crash_worth_100_after_two_seasons."),
    ("str_rmx_evt_yangqun",  "Event:_Herd_behavior_in_the_grain_market._Price_diverges_+/-25%."),
    ("str_rmx_evt_baiyin",   "Event:_Silver_outflow._Sell_prices_x0.95."),
    ("str_rmx_check_insurance", "Insurance_awareness:_you_survived_robbery_with_80%_coverage."),
    ("str_rmx_check_diversify", "Route_diversification:_multiple_routes_spread_your_risk."),
    ("str_rmx_check_leverage",  "Leverage_discipline:_your_debt_stayed_within_safe_limits."),
    ("str_rmx_check_futures",   "Hedging_awareness:_contracts_locked_your_price_risk."),
    ("str_rmx_check_bubble",    "Bubble_watch:_you_did_not_chase_the_land_bubble."),
    ("str_rmx_check_behavior",  "Behavioral_discipline:_you_avoided_the_herd."),
]

# quick_strings.txt 默认文本
qstr_defs = [
    ("qstr_rmx_week",     "Business_weekly:_a_new_season_begins._Read_prices_and_risks."),
    ("qstr_rmx_loan",     "Bank_notice:_10%_seasonal_interest,_borrow_up_to_2x_silver_(cap_3,000)."),
    ("qstr_rmx_contract", "Hankou_grain_house:_forward_contract_at_0.95_of_spot,_settled_next_season."),
    ("qstr_rmx_insure",   "Escort_guild:_premium_6%_of_cargo_value,_80%_payout_if_robbed."),
    ("qstr_rmx_check",    "Merchant_checkup:_your_knowledge_report_awaits_in_town."),
]

# game_strings.csv 汉化（key|中文）
str_cn = [
    ("str_rmx_season_1",  "崇祯十六年春：你在京师开张，本银一千两。"),
    ("str_rmx_season_2",  "崇祯十六年夏：市场在变，留意各城价差与商路风险。"),
    ("str_rmx_season_3",  "崇祯十六年秋：流寇乱中原！"),
    ("str_rmx_season_4",  "崇祯十六年冬：价格继续波动，管好你的风险。"),
    ("str_rmx_season_5",  "崇祯十七年春：李自成破京师！京城物价崩塌。"),
    ("str_rmx_season_6",  "崇祯十七年夏：王朝飘摇，商人必须撑住。"),
    ("str_rmx_season_7",  "崇祯十七年秋：清军入关！北方资产大幅贬值。"),
    ("str_rmx_season_8",  "崇祯十七年冬：终局知识体检——你的商道与学道。"),
    ("str_rmx_card_insurance",   "风险与保险：保费把大损失变成小成本。大明镖局，正是现代保险公司。"),
    ("str_rmx_card_riskpremium", "风险溢价：风险越高的商路，回报必须越高，才有人肯走。"),
    ("str_rmx_card_leverage",    "杠杆：借钱放大收益，也放大破产。季利一成就是代价。"),
    ("str_rmx_card_futures",     "期货与对冲：青苗未熟先卖，锁住米价，把风险转给市场。"),
    ("str_rmx_card_diversify",   "分散化：北方战火，南方照赚。鸡蛋不要放在一个篮子里。"),
    ("str_rmx_card_bubble",      "泡沫与投机：炒地三百买入四百五卖出，两季不卖只剩一百。"),
    ("str_rmx_evt_liukou",   "事件：流寇乱中原，米价大涨，商路风险上升。"),
    ("str_rmx_evt_pojing",   "事件：京师告破！京城物价崩塌。"),
    ("str_rmx_evt_ruguan",   "事件：清军入关，北方物价下跌，北方资产贬值。"),
    ("str_rmx_evt_sanxiang", "事件：三饷加派，天下卖价下降（×0.93）。"),
    ("str_rmx_evt_baochao",  "事件：宝钞风波，现银蒸发一成五。"),
    ("str_rmx_evt_chadi",    "事件：江南炒地成风，泡沫终破，两季不卖只剩百两。"),
    ("str_rmx_evt_yangqun",  "事件：米市羊群效应，米价背离基本面±25%。"),
    ("str_rmx_evt_baiyin",   "事件：白银外流，卖价×0.95。"),
    ("str_rmx_check_insurance", "保险意识：被劫时你保住八成货物。"),
    ("str_rmx_check_diversify", "商路分散：多条商路分散了你的风险。"),
    ("str_rmx_check_leverage",  "杠杆纪律：负债控制在安全范围。"),
    ("str_rmx_check_futures",   "对冲意识：合约帮你锁住了价格风险。"),
    ("str_rmx_check_bubble",    "泡沫警惕：你没有追高地价泡沫。"),
    ("str_rmx_check_behavior",  "行为纪律：你没有在羊群里盲目跟风。"),
]

# quick_strings.csv 汉化
qstr_cn = [
    ("qstr_rmx_week",     "商道周报：新的季节开始了。读一读价差与风险再上路。"),
    ("qstr_rmx_loan",     "钱庄告示：季利一成，可借银两两倍，封顶三千两。"),
    ("qstr_rmx_contract", "汉口粮行：青苗预售，锁价=市价九五折，下季结算。"),
    ("qstr_rmx_insure",   "镖局告示：保费=货值六分，被劫赔付八成。"),
    ("qstr_rmx_check",    "掌柜体检：你的知识体检报告在城镇菜单中。"),
]

# ---------- 追加函数 ----------
def append_lines(path, add_lines, count_header_index=None, add_n=0):
    """追加行；add_n>0 时把头部第 count_header_index 行的计数 +add_n。"""
    with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        content = f.read()
    # 按行拆分，保留行尾符
    if not content.endswith("\n"):
        content += "\n"
    lines = content.splitlines(keepends=True)
    for al in add_lines:
        lines.append(al + "\n")
    if add_n:
        # 更新计数行（第 count_header_index 行，从 0 计）
        hdr = lines[count_header_index].rstrip("\r\n")
        old = int(hdr.split()[0])
        lines[count_header_index] = hdr.replace(str(old), str(old + add_n), 1) + "\n"
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.writelines(lines)
    return len(add_lines)

def verify(path, count_line, is_qstr=False):
    """校验：计数行 == 实际条目数（跳过版本行/空行）。"""
    with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        ls = f.read().splitlines()
    n_decl = int(ls[count_line].split()[0])
    # 条目行：从 count_line+1 起，非空行
    entries = 0
    for l in ls[count_line+1:]:
        if l.strip():
            entries += 1
    ok = (n_decl == entries)
    return n_decl, entries, ok

# ---------- 执行 ----------
results = []

# 1) strings.txt
n = append_lines(MOD + "\\strings.txt", ["%s %s" % (k, v) for k, v in str_defs],
                 count_header_index=1, add_n=len(str_defs))
results.append(("strings.txt", n))

# 2) quick_strings.txt（头部第 0 行即数量）
n = append_lines(MOD + "\\quick_strings.txt", ["%s %s" % (k, v) for k, v in qstr_defs],
                 count_header_index=0, add_n=len(qstr_defs))
results.append(("quick_strings.txt", n))

# 3) game_strings.csv 汉化
n = append_lines(MOD + "\\languages\\cns\\game_strings.csv",
                 ["%s|%s" % (k, v) for k, v in str_cn])
results.append(("game_strings.csv", n))

# 4) quick_strings.csv 汉化
n = append_lines(MOD + "\\languages\\cns\\quick_strings.csv",
                 ["%s|%s" % (k, v) for k, v in qstr_cn])
results.append(("quick_strings.csv", n))

for r in results:
    print("appended:", r[0], "+%d" % r[1])

# ---------- 校验 ----------
s1 = verify(MOD + "\\strings.txt", 1)
s2 = verify(MOD + "\\quick_strings.txt", 0)
print("verify strings.txt        decl/entries/ok:", s1)
print("verify quick_strings.txt  decl/entries/ok:", s2)
# csv 无计数行，检查 key 唯一性
def csv_check(rel):
    with io.open(MOD + "\\" + rel, "r", encoding="utf-8-sig", errors="replace") as f:
        ls = f.read().splitlines()
    keys = [l.split("|")[0] for l in ls if l.strip() and "|" in l]
    dup = len(keys) - len(set(keys))
    return len(keys), dup
c1 = csv_check("languages\\cns\\game_strings.csv")
c2 = csv_check("languages\\cns\\quick_strings.csv")
print("csv game_strings keys/dup:", c1)
print("csv quick_strings keys/dup:", c2)
