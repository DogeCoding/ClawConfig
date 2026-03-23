# 组织编制 · 枢衡堂

| agentId | 花名   | 职责 |
|---------|--------|------|
| `main`  | 枢衡   | 总枢：主人 Graves 唯一主入口；分拣；**在计府输入下分配任务并控成本**；协调绳墨缺口上报；**司驳通过后向主人回奏** |
| `jifu`  | 计府   | **拆解需求**；**市场/价值/成本**（区间与假设） |
| `sibo`  | 司驳   | 交付 **测试与验收**（准奏/封驳）；安全合规清单 |
| `shengmo` | 绳墨 | **能力缺口**判断；建议增 skill/agent；**须经主人审批** |
| `jiangzuo` | 匠作 | 工程实现 |
| `danqing` | 丹青 | 界面与体验 |
| `jingyu` | 镜语 | 漫剧/短剧叙事 |

## 正式需求怎么走

见 **`RUNBOOK.md`**（阶段 1～7）；自动推进、止损、备份见 **`AUTOPILOT.md`**。

## 协作

- 任务单：`tasks/TASK-*.md`
- 跨 agent：`sessions_send` / `sessions_spawn`（若网关开启）或任务单 + 本目录

## 飞书

- **主人** = Graves：本地用户 + 飞书管理员（机器人应用由其创建/发布）。
- 当前已接入：`main` ↔ `accounts.default`
- 其余六职：在 `openclaw.json` 的 `channels.feishu.accounts` 增加应用凭证，并在 `bindings` 中为每个 `accountId` 绑定对应 `agentId`
