# 飞书群接入检查清单

新建或更换**项目群**后，若机器人只在仪表盘有回复、飞书群收不到：

1. 在飞书开放平台 / 群设置中确认群 **`chat_id`**（形如 `oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）。
2. 编辑 **`~/.openclaw/openclaw.json`**（不入 git，以备份包为准）：
   - 在 **`channels.feishu.groupAllowFrom`** 数组中**追加**该 `oc_...`。
   - **必须同步**：在 **`channels.feishu.groups`** 下增加**同名** `oc_...` 键；仅写 `groupAllowFrom` 不写 `groups` 会导致**首条消息无回复、重复发才收到、或重复推送**等异常。
   - 在 **`channels.feishu.groups`** 下增加同名键，例如：
     ```json
     "oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx": {
       "allowFrom": ["*"],
       "requireMention": true
     }
     ```
   - 若希望仅部分成员可触发，将 `allowFrom` 改为对应用户的 `ou_...` 列表（勿用占位符）。
3. 执行 **`openclaw gateway restart`** 使配置生效。

当前已登记的群以 `openclaw.json` 为准；本文件仅作操作说明。
