# RD：v1.3.0 现实资源与证据的第二次蒸馏

## 1. 更新目标

结合 eternity4719 的 HowToLiveBetter《高性价比人生指南》及其 life-decision-guide，深化现有情绪陪伴、边界与方向支持：让舒服既可以是当下被安顿，也可以得到现实资源、减少反复摩擦和增加选择的支撑。上游审阅于 2026-10-07，提交为 `20718eeab32cb8506971fb71b03e66a91077be07`。

本轮保留 v1.2.0 的五道门、舒—分—止—游—起、放—守—做和向心取样。新增模块深化现有现实门、能量门与行动门，不另建主路由，不扩张为通用医疗、法律、财务顾问。

## 2. 要解决的缺口

- 只缩小动作，仍可能让人每天支付同一种打断、解释和兜底成本；需要能改变环境或责任的选择。
- “免费”“只需几分钟”忽略维护、恢复、关系摩擦与退出成本；建议可能在纸面上很轻，实际很重。
- 强证据、作者排序和用户价值是不同判断；混在一起容易把建议写成命令或个人保证。
- 理想需要现实账本，但连接、创作、照料和游戏感不能只按金钱回报裁决。
- 能量比喻、等待时长和研究结果不能被误写成普适机制、固定恢复期限或治疗承诺。

## 3. 行为增量与保留

### 新增与深化

1. 用户要建议时，先辨认基本生活、安全与真实期限；资源断档优先接通现实支持。
2. 分别看钱、时间、身体负荷与选择权，并保留用户对非经济价值的判断。
3. 总成本包括设置、维护、切换、等待、解释、关系摩擦、恢复与退出，并说明谁承担。
4. 在可承受范围内优先考虑减少一次反复摩擦；动作带用户认可的触发、降级与停止条件。
5. 判断继续投入时看未来收益与成本，同时保留仍存在的照料、合同和共同承诺责任。
6. 具体事实要求读完整条目与限制，必要时核对当前原始/官方来源；查不到不编数字与归属。
7. 来源结果、作者判断和本项目适配分开；“低电量”不被解释为意志力储量定律。

### 保留

只倾诉时不夹带方案；只泄压时不追加作业；明确要方案时直接给有限选择。安全、医疗不确定性、哀伤、隐私、非触发边界继续优先。不承诺成功，不诊断，不制造排他依赖，不偷偷降低用户目标。

## 4. 责任与接入

| 责任 | 文件 | 验收方式 |
|---|---|---|
| 主路由与通用约束 | [SKILL.md](./comfortable-ones-act-up/SKILL.md) | 新模块按需入口，五道门与偏好保留 |
| 现实资源、成本与证据方法 | [resources-and-evidence.md](./comfortable-ones-act-up/references/resources-and-evidence.md) | 适用条件、查证流程、来源与许可齐全 |
| 可持续舒服的理论 | [theory.md](./comfortable-ones-act-up/references/theory.md) | 标明原创实践模型；陪坐也可形成闭环 |
| 最小行动接口 | [conversation-protocol.md](./comfortable-ones-act-up/references/conversation-protocol.md) | 触发、总成本、依据、降级、停止线；不强制完整输出 |
| 工具、人生与方向消费者 | [emotional-support.md](./comfortable-ones-act-up/references/emotional-support.md)、[life-guidance.md](./comfortable-ones-act-up/references/life-guidance.md)、[direction-and-ideals.md](./comfortable-ones-act-up/references/direction-and-ideals.md) | 使用共同接口，保留理想、照料与危机边界 |
| 来源记录 | [open-source-patterns.md](./comfortable-ones-act-up/references/open-source-patterns.md) | 固定上游提交，区分正文 CC BY 与代码/Skill MIT |
| 语气与行为合同 | [examples.md](./comfortable-ones-act-up/references/examples.md)、[cases.json](./evals/cases.json) | 新场景与已有场景共同维护，不匹配固定金句 |
| 结构与分发 | VERSION、README、agents/openai.yaml、scripts/validate_skill.py | v1.3.0 一致、本地链接、合法评测标识、ZIP 分发完整 |

## 5. 审阅取舍

来源材料的具体条目、采用与排除只维护在 resources-and-evidence.md。未照搬上游性价比公式、受益人价值排名、固定号码、建议条数、等待月份、临床宣称或正文大清单。固定提交用于来源追溯，不保证其中政策与数字在实际使用时仍有效。

改编参考页以 CC BY 4.0 提供，文件内保留 eternity4719、作品名、链接、许可证、审阅版本与改编说明；其他原创部分仍为 MIT。ZIP 包含该参考页的完整归属，无额外运行依赖。

## 6. 验证合同

基线为 9 个路由参考文件、34 个行为案例，结构校验通过。本轮增加 1 个参考文件和 12 个案例，合计 10 个参考文件、46 个案例。

实际验收命令：

```bash
python3 scripts/validate_skill.py
python3 scripts/package_skill.py --output-dir /tmp/comfortable-v1-3-package
python3 /Users/yangzi/.codex/skills/.system/skill-creator/scripts/quick_validate.py comfortable-ones-act-up
git diff --check
```

分发校验另比对 ZIP 全部成员与源码字节、校验 SHA-256，并用两个输出目录比较可重复构建。仓库 CI 使用原有结构校验与打包流程。绝对路径的 quick_validate 命令仅适用于本次本地环境。

行为案例覆盖：低余量与资源断档、反复通知与值班例外、免费方案的隐形成本、沉没成本与剩余责任、非经济理想、来源不可取、强证据不等于个人保证、重大打击中的及时事务、证据模板不侵入陪伴、仅问政策不误触。

这些案例定义预期行为；结构校验不会调用模型，不宣称 46 个真实回答已通过。模型执行与评分仍按 [evals/README.md](./evals/README.md) 独立进行。

## 7. GitHub 交付

用户已授权提交 PR 并合并 main。分支为 `codex/deepen-life-support-v1-3`，PR 以新增行为、兼容边界和实际校验结果描述。待 PR 检查通过且可合并后执行合并，再核对 GitHub 状态与本地 main；本轮不另建 Release 或改动全局已安装 Skill。
