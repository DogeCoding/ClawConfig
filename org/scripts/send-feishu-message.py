#!/usr/bin/env python3
import json
import sys
import uuid
from pathlib import Path
from urllib.request import Request, urlopen

CFG = Path.home() / ".openclaw" / "openclaw.json"


def token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    body = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    if data.get("code") != 0:
        raise SystemExit(data)
    return data["tenant_access_token"]


def send_chat(token: str, chat_id: str, text: str) -> dict:
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False),
        "uuid": str(uuid.uuid4()),
    }
    body = json.dumps(payload).encode()
    req = Request(
        url,
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main() -> None:
    if len(sys.argv) < 3:
        print("用法: send-feishu-message.py <chat_id oc_xxx> <文本>", file=sys.stderr)
        raise SystemExit(2)
    chat_id, message_text = sys.argv[1], sys.argv[2]
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    fei = cfg.get("channels", {}).get("feishu", {})
    da = fei.get("defaultAccount") or "default"
    acc = (fei.get("accounts") or {}).get(da) or {}
    app_id, app_secret = acc.get("appId"), acc.get("appSecret")
    if not app_id or not app_secret:
        raise SystemExit("openclaw.json 缺少飞书 default 账户凭证")
    t = token(str(app_id), str(app_secret))
    out = send_chat(t, chat_id, message_text)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if out.get("code") != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
