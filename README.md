# 日暮西山 · 商道 —— 金融之道 mod 升级（建模与原型仓库）

把耶鲁《金融市场》的风险管理智慧，融合进骑砍 1《日暮西山》mod 的明末乱世。
**核心设计：王朝会覆灭，但懂得风险管理的商人能活下来。**

## 仓库内容（建模与配置即代码）

| 文件 | 角色 |
|---|---|
| `rimuxi-shandao.html` | 可玩机制原型（单文件，内嵌唯一配置源 `CONFIG`，ruleset_id=`RMX-SHANDAO-V1`） |
| `sim_balance.py` | 数值模拟引擎：从 HTML 提取同一配置，镜像 JS 引擎，3000 局×5 策略批量验证 |
| `design-contract.json` | 游戏设计契约（规则/参数/断言/状态机/测试/原型门禁，PAR-SIM-* 实测值已回填） |
| `MOD_BASELINE.md` | 《日暮西山》mod 现状探查基线（势力/经济系统/脚本/实改入口） |
| `README.md` | 本文件 |

## 运行与验证

- 原型：浏览器直接打开 `rimuxi-shandao.html` 即玩（离线单文件）。
- 模拟：`python sim_balance.py`（依赖仅标准库），自动回填契约实测值。
- 契约校验：`python validate_design_contract.py design-contract.json`（doubao-game-designer skill 附带）。

## 平衡结论（模拟实测，6/6 断言 PASS）

| 策略 | 达成率（目标 4000 两） | 破产率 |
|---|---|---|
| 稳健（投保+分散+对冲） | 89.0% | 0.0% |
| 随机（会读方向、不用工具） | 31.6% | 13.4% |
| 赌徒（满杠杆+违禁品） | 0.0% | 99.97% |

投保优于裸奔 Δ+3,724 两；青苗合约对冲使谷物重仓波动 σ 105→89。

## mod 实改（第二阶段）

`MOD_BASELINE.md` 记录了追加式实改入口与实改日志：备份 → scripts.txt/simple_triggers.txt/strings/csv 尾部追加 → 校验计数行 → 可回滚。
已落地：金融之道文本资产层（季报/希勒卡/事件/体检文案，双语汉化）+ 商道季结触发器（每 7 天 +100 两，操作码与 mod 既有用法逐位一致）；待游戏内验证项见 MOD_BASELINE 第五节。
P0 实改清单与验收见飞书 GDD：https://my.feishu.cn/docx/Ms3XdtPKto1S1BxWJ7Vc45hynhd

## 在线试玩

https://fll-dave.github.io/rimuxi-shandao-upgrade/rimuxi-shandao.html
