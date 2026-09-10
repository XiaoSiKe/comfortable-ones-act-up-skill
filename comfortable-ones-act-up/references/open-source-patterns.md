# 开源 Skills 调研与适配记录

本文件记录 v1.0.0 深化时参考的开源 Agent Skills。调研于 2026-09-10 使用 GitHub CLI 完成；链接固定到当时审阅的提交，避免上游更新后来源含义漂移。

这些项目提供设计启发，而不是本 Skill 的运行时依赖。本项目没有复制它们的长段提示词、模板或专用领域流程；采用的都是重新表达后的通用交互原则。

## 已采用的模式

| 来源 | 许可证 | 吸收的模式 | 在本项目中的适配 |
|---|---|---|---|
| [`okooo5km/life-coach-skill`](https://github.com/okooo5km/life-coach-skill/blob/5e592bcf748376c8b5cf453d8c471167a77a9bef/SKILL.md) | MIT | 先理解后建议；明确求方案时不扣住答案；一次一个关键问题；挑战前征得同意 | 写入“帮助偏好”和“提问/挑战协议”，保留本项目的放—守—做与道家表达 |
| [`github/awesome-copilot` Tugboat](https://github.com/github/awesome-copilot/blob/419c37e80b90dc49d9049a5d3e36c5f8256d1208/skills/tugboat/SKILL.md) | MIT | 同理心要改变工作；保护用户的目标；用证据而非保证处理任务焦虑；回答长度不等于关心 | 写入“同理心转化检查”和“目标—当前方法双轨”，不引入软件项目专用诊断流程 |
| [`pm-claude-skills` Spoon Planner](https://github.com/mohitagw15856/pm-claude-skills/blob/b89e14bfc6acbb7e85f370aa826c47af2a5a2812/skills/spoon-planner/SKILL.md) | MIT | 按能量范围和低点规划；计算隐形成本；休息前置；避免旺盛日透支 | 泛化为非医疗的“能量门”和最低可行日；不借用慢性病评分或提供医疗建议 |
| [`pm-claude-skills` Rabbit Hole Rescue](https://github.com/mohitagw15856/pm-claude-skills/blob/b89e14bfc6acbb7e85f370aa826c47af2a5a2812/skills/rabbit-hole-rescue/SKILL.md) | MIT | 先理解表面行为满足的需要；设现实的阶段目标；保护关系同时保护自己 | 用于分析讨好、反刍和冲突背后的安全/确定/归属需要；不引入阴谋论专用流程 |
| [`joozio/agent-wellbeing-kit` Wellbeing Boundaries](https://github.com/joozio/agent-wellbeing-kit/blob/0d9279970b9fa2e51e56c3b6ee627c4b53cf7086/skills/wellbeing-boundaries/SKILL.md) | MIT | 边界必须改变实际路由；被拦截后不通过改名绕过；真正紧急情况单独处理 | 泛化为“边界要有可执行后果”；不引入通知系统、脚本或自动化依赖 |

## 来源强度与使用限制

- `github/awesome-copilot` 是 GitHub 维护的社区资源库，适合参考 Agent 协作与表达纪律，但其内容不等同于临床证据。
- `pm-claude-skills` 是大型社区技能集合，适合观察专用 Skill 如何写出明确产物、反模式与质量检查；其中任何健康相关细节仍需回到专业来源核对。
- `life-coach-skill` 与 `agent-wellbeing-kit` 规模较小，采用的是可独立审查的交互设计，不把星标数或作者声明当成效果证据。
- 所有上表仓库在调研时由 GitHub 标记为 MIT License；固定文件链接用于说明具体审阅版本。

## 主动排除的模式

调研中还出现了一批自称“心理学家”“治疗模式”或包含临床量表的 Skills。本项目没有吸收以下做法：

- 让通用 Agent 扮演持证治疗师或进行疾病诊断；
- 用未经上下文校验的固定分数宣布临床状态；
- 把生理机制、疗效百分比或单一练习写成确定事实；
- 默认要求长期打卡、记录敏感心理档案或制造依赖；
- 用积极话术覆盖哀伤、贫困、歧视、暴力和真实资源问题；
- 把任何一个框架强制用于所有用户。

## 非仓库基础来源

本 Skill 的现代压力管理仍以 [WHO《Doing What Matters in Times of Stress》](https://www.who.int/publications/i/item/9789240003927) 为主要公共健康桥梁；哲学原典使用中国哲学书电子化计划、Perseus Digital Library 与 SuttaCentral，具体链接见 [philosophy.md](philosophy.md)。

## 许可证与再表达

本项目以 MIT License 发布。开源仓库仅作为设计参考；文案、中文比喻、双义理论、舒—分—止—游—起、放—守—做及四层观察均由本项目重新组织和表达。若未来直接复用第三方代码、模板或较长文本，应在合并前单独核对许可证并补充明确归属。
