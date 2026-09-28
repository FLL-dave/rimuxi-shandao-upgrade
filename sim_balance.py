# -*- coding: utf-8 -*-
"""《日暮西山·商道》数值模拟：从 HTML 提取同一 CONFIG（单一配置源），镜像 JS 引擎，
模拟稳健/赌徒/随机三策略 × N 局，输出达成率、破产率与均值；并做投保对比与期货对冲对比。
"""
import re, json, math, statistics, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, 'rimuxi-shandao.html')

def load_config(path=HTML):
    html = open(path, encoding='utf-8').read()
    m = re.search(r'/\*CONFIG_START\*/(.*?)/\*CONFIG_END\*/', html, re.S)
    raw = re.sub(r'^const CONFIG\s*=\s*', '', m.group(1).strip()).rstrip(';').strip()
    return json.loads(raw)

def mulberry32(seed):
    a = seed & 0xffffffff
    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xffffffff
        t = a
        t = (t ^ (t >> 15)) & 0xffffffff
        t = (t * (1 | a)) & 0xffffffff          # Math.imul(t, 1|a)
        imul2 = ((t ^ (t >> 7)) & 0xffffffff) * (61 | t)
        imul2 &= 0xffffffff                     # Math.imul(t^t>>>7, 61|t)
        t = ((t + imul2) & 0xffffffff) ^ t
        t &= 0xffffffff
        return ((t ^ (t >> 14)) & 0xffffffff) / 4294967296.0
    return nxt

def fmt(n): return f"{round(n):,}"

class Game:
    def __init__(self, cfg, seed):
        self.cfg = cfg
        self.cityById = {c['id']: c for c in cfg['cities']}
        self.goodById = {g['id']: g for g in cfg['goods']}
        self.rng = mulberry32(seed)
        self.seed = seed
        self.city = cfg['start_city']; self.silver = cfg['start_silver']; self.debt = 0
        self.cargo = {}; self.avgCost = {}
        self.prices = {}; self.trend = {}
        self.season = 0; self.contracts = []
        self.seasonEvents = []
        self.bubbleOwned = False; self.bubbleTurns = 0
        self.traveled = False
        self.ended = False; self.bankrupt = False; self.final_wealth = 0
        self.metrics = {'robs':0, 'confiscated':0}
        self._init_prices()

    # ---------- 基础 ----------
    def R(self): return self.rng()
    def city_mods(self, city): return self.cityById[city]['mods']
    def base_price(self, city, good):
        return self.goodById[good]['base'] * self.city_mods(city)[good]
    def _init_prices(self):
        for c in self.cfg['cities']:
            self.prices[c['id']] = {}
            for g in self.cfg['goods']:
                t = self.base_price(c['id'], g['id'])
                self.prices[c['id']][g['id']] = round(max(0.5, t*(0.9+0.2*self.R()))*10)/10

    def modifiers(self):
        m = {'grainAll':1,'grainNorth':1,'grainSouth':1,'grainXian':1,'grainBeijing':1,
             'sellAll':1,'sellTax':1,'saltAll':1,'teaSaltDatong':1,'silkTeaSouth':1,
             'goodsShengjing':1,'goodsNorth':1,'riskNorth':0,'riskToBeijing':0,
             'riskToShengjing':0,'riskToDatong':0,'riskXianDatong':0,'ironBonus':0,
             'blockCity':None,'bubbleOffer':False}
        for ev in self.seasonEvents:
            if 'grain_all' in ev: m['grainAll']*=ev['grain_all']
            if 'grain_north' in ev: m['grainNorth']*=ev['grain_north']
            if 'grain_south' in ev: m['grainSouth']*=ev['grain_south']
            if 'grain_xian' in ev: m['grainXian']*=ev['grain_xian']
            if 'grain_beijing' in ev: m['grainBeijing']*=ev['grain_beijing']
            if 'sell_all' in ev: m['sellAll']*=ev['sell_all']
            if 'sell_tax' in ev: m['sellTax']*=ev['sell_tax']
            if 'salt_all' in ev: m['saltAll']*=ev['salt_all']
            if 'tea_salt_datong' in ev: m['teaSaltDatong']*=ev['tea_salt_datong']
            if 'silk_tea_south' in ev: m['silkTeaSouth']*=ev['silk_tea_south']
            if 'goods_shengjing' in ev: m['goodsShengjing']*=ev['goods_shengjing']
            if 'goods_north' in ev: m['goodsNorth']*=ev['goods_north']
            if 'risk_north' in ev: m['riskNorth']+=ev['risk_north']
            if 'risk_to_beijing' in ev: m['riskToBeijing']+=ev['risk_to_beijing']
            if 'risk_to_shengjing' in ev: m['riskToShengjing']+=ev['risk_to_shengjing']
            if 'risk_to_datong' in ev: m['riskToDatong']+=ev['risk_to_datong']
            if 'risk_xian_datong' in ev: m['riskXianDatong']+=ev['risk_xian_datong']
            if 'iron_confiscate_bonus' in ev: m['ironBonus']+=ev['iron_confiscate_bonus']
            if 'block_city' in ev: m['blockCity']=ev['block_city']
            if 'bubble_offer' in ev: m['bubbleOffer']=True
        for sd in self.cfg['scheduled']:
            if sd['season'] != self.season: continue
            for k in ('risk_bonus_north','risk_north'):
                if k in sd: m['riskNorth']+=sd[k]
            if 'risk_to_beijing' in sd: m['riskToBeijing']+=sd['risk_to_beijing']
            if 'grain_north' in sd: m['grainNorth']*=sd['grain_north']
            if 'grain_beijing' in sd: m['grainBeijing']*=sd['grain_beijing']
            if 'goods_north' in sd: m['goodsNorth']*=sd['goods_north']
        return m

    def price_mod(self, city, good, m):
        k = 1.0
        if good=='grain':
            k*=m['grainAll']
            if self.cityById[city]['region']=='north': k*=m['grainNorth']
            else: k*=m['grainSouth']
            if city=='xian': k*=m['grainXian']
            if city=='beijing': k*=m['grainBeijing']
        if good=='salt':
            k*=m['saltAll']
            if city=='datong': k*=m['teaSaltDatong']
        if good=='tea':
            if city=='datong': k*=m['teaSaltDatong']
            if city in ('yangzhou','hankou'): k*=m['silkTeaSouth']
        if good=='silk':
            if city in ('yangzhou','hankou'): k*=m['silkTeaSouth']
        if city=='shengjing': k*=m['goodsShengjing']
        if self.cityById[city]['region']=='north': k*=m['goodsNorth']
        k*=m['sellAll']
        k*=m['sellTax']
        return k

    def step_prices(self):
        m = self.modifiers()
        for c in self.cfg['cities']:
            for g in self.cfg['goods']:
                target = self.base_price(c['id'], g['id']) * self.price_mod(c['id'], g['id'], m)
                vol = [x for x in self.cfg['goods'] if x['id']==g['id']][0]['vol']
                noise = (self.R()+self.R()+self.R()-1.5)*vol*target
                p = self.prices[c['id']][g['id']] + (target-self.prices[c['id']][g['id']])*self.cfg['mean_revert'] + noise
                self.prices[c['id']][g['id']] = round(max(0.5, p)*10)/10

    def route_risk(self, r):
        m = self.modifiers(); risk = self.cfg['route_risk'][r['risk']]
        if r['a']=='beijing' or r['b']=='beijing': risk+=m['riskToBeijing']
        if r['a']=='shengjing' or r['b']=='shengjing': risk+=m['riskToShengjing']
        if r['a']=='datong' or r['b']=='datong': risk+=m['riskToDatong']+m['riskXianDatong']
        if r['a']=='xian' or r['b']=='xian': risk+=m['riskXianDatong']
        if self.cityById[r['a']]['region']=='north' and self.cityById[r['b']]['region']=='north':
            risk+=m['riskNorth']
        return max(0.02, min(0.85, risk))

    def used_cap(self): return sum(self.cargo.values())
    def cargo_value(self, city=None):
        city = city or self.city
        return sum(self.cargo.get(g,0)*self.prices[city][g] for g in self.goodById if self.cargo.get(g,0))
    def total_wealth(self): return self.silver + self.cargo_value()

    # ---------- 动作 ----------
    def routes_from(self, city):
        m = self.modifiers()
        out = []
        for r in self.cfg['routes']:
            if r['a']==city: dest = r['b']
            elif r['b']==city: dest = r['a']
            else: continue
            if m['blockCity'] in (city, dest): continue
            if m['blockCity']==city: continue
            out.append(r)
        return out

    def do_travel(self, insure):
        r = self.dest_route; dest = r['a'] if r['b']==self.city else r['b']
        cost = self.cfg['travel_base_cost'] + round(self.cfg['travel_per_unit']*self.used_cap())
        if self.silver < cost: self.silver = cost  # 至少付得起
        self.silver -= cost
        val = self.cargo_value()
        if insure:
            premium = round(val*self.cfg['insurance']['premium'])
            self.silver -= premium
        risk = self.route_risk(r)
        if self.R() < risk:
            self.metrics['robs'] += 1
            loss_rate = (1-self.cfg['insurance']['coverage']) if insure else self.cfg['insurance']['uninsured_loss']
            for g in list(self.cargo.keys()):
                q = int(self.cargo[g]*loss_rate)
                self.cargo[g] -= q
                if self.cargo[g] <= 0: del self.cargo[g]
        if self.cargo.get('iron',0):
            if self.R() < self.cfg['iron_confiscate'] + self.modifiers()['ironBonus']:
                self.metrics['confiscated'] += 1
                self.silver -= self.cfg['iron_fine']
                del self.cargo['iron']
        self.city = dest; self.traveled = True; self.dest_route = None

    def borrow_max(self):
        cap = min(int(self.silver*self.cfg['loan']['max_mult']), self.cfg['loan']['cap']) - self.debt
        if cap > 0:
            self.silver += cap; self.debt += cap
            return cap
        return 0

    def repay_all(self):
        pay = min(self.debt, self.silver)
        self.silver -= pay; self.debt -= pay
        return pay

    def sign_futures(self):
        if self.city != 'hankou': return False
        if len(self.contracts) >= self.cfg['futures']['contract_cap']: return False
        P = round(self.prices['hankou']['grain']*(1-self.cfg['futures']['lock_markup'])*10)/10
        self.contracts.append({'P':P,'Q':self.cfg['futures']['q_max'],'signedSeason':self.season})
        return True

    def settle_futures(self):
        if not self.contracts: return
        spot = self.prices['hankou']['grain']
        due = [ct for ct in self.contracts if ct['signedSeason'] < self.season]
        rest = [ct for ct in self.contracts if ct['signedSeason'] >= self.season]
        for ct in due:
            self.silver += round((ct['P']-spot)*ct['Q'])
        self.contracts = rest

    def buy_bubble(self):
        if self.silver < self.cfg['bubble']['cost']: return False
        self.silver -= self.cfg['bubble']['cost']
        self.bubbleOwned = True; self.bubbleTurns = 0
        return True

    def sell_bubble(self):
        if not self.bubbleOwned: return
        self.silver += self.cfg['bubble']['sell_next']
        self.bubbleOwned = False; self.bubbleTurns = 0

    # ---------- 季末 ----------
    def end_season(self):
        if self.debt > 0:
            self.debt += round(self.debt*self.cfg['loan']['rate'])
        self.settle_futures()
        # 偿付检查：强制抛货
        if (self.silver + self.cargo_value()) < self.debt - 1e-9:
            for g in list(self.cargo.keys()):
                self.silver += round(self.cargo[g]*self.prices[self.city][g]*self.cfg['loan']['forced_sell_price'])
                del self.cargo[g]
        if (self.silver + self.cargo_value()) < self.debt - 1e-9:
            self.ended = True; self.bankrupt = True
            self.final_wealth = 0
            return
        # 随机事件
        pool = self.cfg['events']; total = sum(e['weight'] for e in pool)
        picked = []
        r = self.R()*total
        for ev in pool:
            r -= ev['weight']
            if r < 0: picked.append(ev); break
        if self.R() < 0.3 and len(pool) > 1:
            for _ in range(8):
                ev = pool[int(self.R()*len(pool))]
                if ev not in picked: picked.append(ev); break
        self.seasonEvents = picked
        for ev in picked:
            if 'cash_loss' in ev:
                self.silver -= round(self.silver*ev['cash_loss'])
        # 炒地
        if self.bubbleOwned:
            self.bubbleTurns += 1
            if self.bubbleTurns >= self.cfg['bubble']['hold_seasons']:
                self.bubbleOwned = False; self.bubbleTurns = 0
                self.silver += self.cfg['bubble']['crash_value']
        self.season += 1
        if self.season >= self.cfg['seasons']:
            self.settle_futures()
            self.ended = True
            self.final_wealth = self.final_wealth_calc()
            return
        self.step_prices()

    def final_wealth_calc(self):
        w = self.total_wealth()
        if self.cityById[self.city]['region'] == 'north':
            w = round(w*self.cfg['north_discount'])
        return max(0, round(w - self.debt))

# ================= 策略 =================
def sell_all(g):
    for k in list(g.cargo.keys()):
        g.silver += round(g.cargo[k]*g.prices[g.city][k])
        del g.cargo[k]

def buy_max(g, good, frac=1.0):
    """按当前城市价格买入 max(可负担, 库容) 单位；frac 限制动用资金比例"""
    price = g.prices[g.city][good]
    if price <= 0: return 0
    qty = min(g.cfg['cargo_cap'] - g.used_cap(), int(g.silver*frac/price))
    if qty <= 0: return 0
    g.silver -= round(qty*price)
    g.cargo[good] = g.cargo.get(good,0) + qty
    return qty

def best_route(g, prefer_shengjing=False):
    """选择商路：按风险调整利差评分"""
    routes = g.routes_from(g.city)
    if not routes: return None
    if prefer_shengjing:
        to_sj = [r for r in routes if 'shengjing' in (r['a'],r['b'])]
        if to_sj: return to_sj[0]
    best=None; best_score=-1e9
    for r in routes:
        dest = r['a'] if r['b']==g.city else r['b']
        risk = g.route_risk(r)
        margin = 1.0
        for gd in g.cfg['goods']:
            buy = g.prices[g.city][gd['id']]; sell = g.prices[dest][gd['id']]
            if buy > 0: margin = max(margin, sell/buy)
        score = margin - risk*2.2
        if risk >= 0.3 and margin < 1.5: score -= 10  # 高风险低利差不碰
        if score > best_score: best_score=score; best=r
    return best

def best_good_for(g, route, allow_iron=True):
    dest = route['a'] if route['b']==g.city else route['b']
    best=None; ratio=1.0
    for gd in g.cfg['goods']:
        if not allow_iron and gd['id']=='iron': continue
        buy = g.prices[g.city][gd['id']]; sell = g.prices[dest][gd['id']]
        if buy > 0 and sell/buy > ratio: ratio=sell/buy; best=gd['id']
    return best

# ---- 稳健 ----
def run_steady(g):
    for _ in range(g.cfg['seasons']):
        if g.ended: break
        m = g.modifiers()
        sell_all(g)
        # 炒地：稳健不参与
        if g.bubbleOwned and g.bubbleTurns >= 1: g.sell_bubble()
        if g.city=='hankou' and g.prices['hankou']['grain'] > 2.2: g.sign_futures()
        route = best_route(g, prefer_shengjing=False)
        if not route:
            g.end_season(); continue
        g.dest_route = route
        risk = g.route_risk(route)
        insure = risk >= 0.13
        good = best_good_for(g, route, allow_iron=False)
        if good: buy_max(g, good)
        g.do_travel(insure)
        sell_all(g)
        g.end_season()

# ---- 赌徒 ----
def run_gambler(g):
    for _ in range(g.cfg['seasons']):
        if g.ended: break
        m = g.modifiers()
        sell_all(g)
        g.borrow_max()
        if g.city=='hankou':
            while g.sign_futures(): pass
        route = best_route(g, prefer_shengjing=True)
        if not route:
            g.end_season(); continue
        g.dest_route = route
        # 优先买兵甲（利差最大）+ 人参
        for good in ('iron','ginseng'):
            if g.used_cap() < g.cfg['cargo_cap'] and g.silver > 0:
                buy_max(g, good)
        if g.used_cap() < g.cfg['cargo_cap']:
            gd = best_good_for(g, route)
            if gd: buy_max(g, gd)
        g.do_travel(False)
        sell_all(g)
        g.end_season()

# ---- 随机 ----
def run_random(g):
    for _ in range(g.cfg['seasons']):
        if g.ended: break
        m = g.modifiers()
        sell_all(g)
        if g.bubbleOwned and g.bubbleTurns >= 1:
            if g.R() < 0.5: g.sell_bubble()
        if g.R() < 0.2: g.borrow_max()
        if g.city=='hankou' and g.R() < 0.3 and g.prices['hankou']['grain'] < 2.0: g.sign_futures()
        routes = g.routes_from(g.city)
        if not routes:
            g.end_season(); continue
        # 按利差加权随机挑商路（普通玩家会倾向去有利可图的方向）
        scored = []
        for r in routes:
            dest = r['a'] if r['b']==g.city else r['b']
            best_margin = 1.0
            for gd in g.cfg['goods']:
                buy = g.prices[g.city][gd['id']]; sell = g.prices[dest][gd['id']]
                if buy > 0: best_margin = max(best_margin, sell/buy)
            scored.append((r, best_margin))
        scored.sort(key=lambda x: -x[1])
        pool = [s[0] for s in scored[:3]]
        route = pool[int(g.R()*len(pool))]
        g.dest_route = route
        dest = route['a'] if route['b']==g.city else route['b']
        # 买该路线利差最大的货（铁器半概率避开）
        good = best_good_for(g, route, allow_iron=(g.R() < 0.4))
        if good and g.R() < 0.95: buy_max(g, good)
        g.do_travel(g.R() < (0.8 if g.debt > 0 else 0.55))
        sell_all(g)
        if m['bubbleOffer'] and g.city=='yangzhou' and g.silver >= g.cfg['bubble']['cost'] and g.R() < 0.3:
            g.buy_bubble()
        g.end_season()

# ---- 高风险投保对比（盛京线路） ----
def run_highrisk(g, insure):
    for _ in range(g.cfg['seasons']):
        if g.ended: break
        sell_all(g)
        route = best_route(g, prefer_shengjing=True)
        if not route:
            g.end_season(); continue
        g.dest_route = route
        # 只做人参/丝绸
        dest = route['a'] if route['b']==g.city else route['b']
        good = 'ginseng' if g.city=='shengjing' else 'silk'
        buy_max(g, good)
        g.do_travel(insure)
        sell_all(g)
        g.end_season()

# ---- 期货对冲对比（谷物重仓） ----
def run_grainheavy(g, hedge):
    # 汉口囤粮商：不旅行，每季买入米粮、下季卖出，完全暴露于汉口米价风险
    g.city = 'hankou'
    for _ in range(g.cfg['seasons']):
        if g.ended: break
        sell_all(g)
        if hedge: g.sign_futures()
        buy_max(g, 'grain')
        g.end_season()

# ================= 运行与报告 =================
def simulate(cfg, policy, n=3000, base_seed=1000):
    finals=[]; surv=0; bankrupt=0
    for i in range(n):
        g = Game(cfg, base_seed+i)
        policy(g)
        w = g.final_wealth
        finals.append(w)
        if g.bankrupt: bankrupt+=1
        elif w >= cfg['targets']['survive']: surv+=1
    return {'n':n, 'mean':statistics.mean(finals), 'median':statistics.median(finals),
            'std':statistics.pstdev(finals), 'survive_rate':surv/n, 'bankrupt_rate':bankrupt/n}

def main():
    cfg = load_config()
    N = 3000
    res = {}
    for name, fn in [('稳健', run_steady), ('赌徒', run_gambler), ('随机', run_random)]:
        r = simulate(cfg, fn, n=N)
        res[name] = r
        print(f"[{name}] 达成率 {r['survive_rate']:.1%}  破产率 {r['bankrupt_rate']:.1%}  "
              f"均值 {fmt(r['mean'])}两  中位 {fmt(r['median'])}两  σ {fmt(r['std'])}")
    # 投保对比（高风险盛京线）
    ins_res = simulate(cfg, lambda g: run_highrisk(g, True), n=N)
    noins_res = simulate(cfg, lambda g: run_highrisk(g, False), n=N)
    delta = ins_res['mean'] - noins_res['mean']
    print(f"[投保对比·盛京线] 投保均值 {fmt(ins_res['mean'])} (σ {fmt(ins_res['std'])})  vs  裸奔均值 {fmt(noins_res['mean'])} (σ {fmt(noins_res['std'])})  → Δ {fmt(delta)}")
    # 期货对冲对比（谷物重仓）
    hedge_res = simulate(cfg, lambda g: run_grainheavy(g, True), n=N)
    nohedge_res = simulate(cfg, lambda g: run_grainheavy(g, False), n=N)
    std_delta = nohedge_res['std'] - hedge_res['std']
    print(f"[对冲对比·谷物重仓] 对冲 σ {fmt(hedge_res['std'])} vs 不对冲 σ {fmt(nohedge_res['std'])} → σ差 {fmt(std_delta)}")
    # 判定
    ok = True
    checks = [
        ('稳健达成率≥70%', res['稳健']['survive_rate'] >= 0.7, res['稳健']['survive_rate']),
        ('赌徒达成率≤15%', res['赌徒']['survive_rate'] <= 0.15, res['赌徒']['survive_rate']),
        ('随机达成率30-60%', 0.3 <= res['随机']['survive_rate'] <= 0.6, res['随机']['survive_rate']),
        ('赌徒破产率≥30%', res['赌徒']['bankrupt_rate'] >= 0.3, res['赌徒']['bankrupt_rate']),
        ('投保≥裸奔(盛京线)', delta >= 0, delta),
        ('对冲降低波动', std_delta >= 0, std_delta),
    ]
    print('\n=== 判定 ===')
    for name, passed, val in checks:
        print(('PASS ' if passed else 'FAIL ') + name + f" ({val:.3f})")
        ok = ok and passed
    print('总体:', 'PASS' if ok else 'FAIL')
    # 回填模拟结果供契约更新
    import json as _json
    contract_path = os.path.join(HERE, 'design-contract.json')
    if os.path.exists(contract_path):
        cj = _json.load(open(contract_path, encoding='utf-8'))
        mapping = {'PAR-SIM-STEADY': res['稳健']['survive_rate'], 'PAR-SIM-GAMBLER': res['赌徒']['survive_rate'],
                   'PAR-SIM-RANDOM': res['随机']['survive_rate'], 'PAR-SIM-INS-DELTA': delta,
                   'PAR-SIM-FUTURE-STD-DELTA': std_delta, 'PAR-SIM-GAMBLER-BANKRUPT': res['赌徒']['bankrupt_rate']}
        for p in cj['parameters']:
            if p['id'] in mapping:
                p['value'] = round(mapping[p['id']], 4)
        _json.dump(cj, open(contract_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print('模拟结果已回填 design-contract.json')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
