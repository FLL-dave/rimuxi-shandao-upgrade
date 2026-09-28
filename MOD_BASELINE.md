# 《日暮西山》mod 现状探查基线

探查日期：2026-09-29　|　目标目录：`D:\steam\steamapps\common\MountBlade Warband\Modules\rimuxishan`

## 一、构成与规模（编译成品，无 Module System 源码）

| 文件 | 规模 | 说明 |
|---|---|---|
| scripts.txt | 1.45 MB，722 个脚本 | 标准 Warband 脚本系统（操作码 txt） |
| conversation.txt | 1.21 MB | 对话系统 |
| parties.txt | 299 个队伍 | 城镇/商队/军队 |
| party_templates.txt | 133 个模板 | 商队/匪徒/英雄等 |
| item_kinds1.txt | 238 KB | 物品（含贸易货物） |
| languages\cns\* | 简中汉化齐全 | dialogs/factions/game_strings/item_kinds/troops 等 18 个 csv |
| module.ini | module_name=Calradia | 基于原版魔改 |

## 二、势力格局（22 个王国）

- 明系：大明王朝、弘光大明、隆武大明、永历大明、鲁监国
- 反明：大清、大顺、大西
- 周边：喀尔喀蒙古、叶尔羌汗国、大越、哈萨克汗国、朝鲜
- 西洋：荷兰东印度公司、葡萄牙东方贸易据点
- 文化组 19 种；商人阵营 fac_merchants 存在

## 三、经济系统现状（金融玩法的挂载点）

| 脚本 | 职能 |
|---|---|
| game_get_item_buy_price_factor / sell | 买卖价因子（玩家议价） |
| initialize_trade_routes / set_trade_route_between_centers | 贸易路线 |
| average_trade_good_prices / update_trade_good_prices | 货物价格波动 |
| average_trade_good_productions / good_price_affects_good_production | 生产与价格联动 |
| do_merchant_town_trade / do_party_center_trade | 商人与城镇交易 |
| refresh_village_merchant_inventory / update_village_market_towns | 村庄市场 |

贸易货物沿用原版体系：盐（itm_salt）、苎麻布（itm_linen）、棉布（itm_wool_cloth）、生铁（itm_iron）、米粮等。

## 四、实改入口与安全策略

1. **备份**：改动前对所有目标文件做 `.bak`。
2. **追加式**：新脚本/触发器/字符串/汉化全部追加到文件尾，同步更新文件头计数行；**绝不动既有行的索引与内容**（Warband txt 按行序编索引，追加不破坏现有引用）。
3. **校验**：每步后核对计数行与实际条目数一致。
4. **回滚**：还原 `.bak` 即完整恢复。

## 五、P0 实改清单（对应飞书 GDD 第 7 章）

| 编号 | 内容 | 涉及文件 |
|---|---|---|
| P0-1 | 季循环触发器（按天数模拟"季"：计息/合约差价/价格波动） | simple_triggers.txt、scripts.txt |
| P0-2 | 钱庄借贷（季利 10%、强制抛售、破产判定） | scripts.txt、menus.txt、game_strings.csv |
| P0-3 | 青苗预售合约（下季结算、盈亏=（锁定价−市价）×数量） | scripts.txt、strings.txt、languages csv |
| P0-4 | 镖局投保（保费 6%、被劫赔付 80%） | scripts.txt、conversation.txt |
| P0-5 | 国运事件（流寇/破京师/入关 + 随机事件池，价格因子真实生效） | scripts.txt、simple_triggers.txt、quick_strings.txt |
| P0-6 | 希勒小课堂与终局体检文本 | strings.txt、languages csv |
