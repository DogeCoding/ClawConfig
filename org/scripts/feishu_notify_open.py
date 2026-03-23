#!/usr/bin/env python3
import json
import sys
import time
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

CFG = Path.home() / ".openclaw" / "openclaw.json"


def tenant_token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    body = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    if data.get("code") != 0:
        raise RuntimeError(data)
    return data["tenant_access_token"]


def send_p2p_text(token: str, open_id: str, text: str) -> dict:
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    payload = {
        "receive_id": open_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False),
        "uuid": str(uuid.uuid4()),
    }
    body = json.dumps(payload).encode()
    req = Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def load_default_account() -> tuple[str, str]:
    raw = json.loads(CFG.read_text(encoding="utf-8"))
    fei = raw.get("channels", {}).get("feishu", {})
    da = fei.get("defaultAccount") or "default"
    acc = (fei.get("accounts") or {}).get(da) or {}
    app_id = acc.get("appId")
    app_secret = acc.get("appSecret")
    if not app_id or not app_secret:
        raise SystemExit("missing channels.feishu.accounts.default appId/appSecret")
    return str(app_id), str(app_secret)


def main() -> None:
    if len(sys.argv) < 3:
        print("usage: feishu_notify_open.py <open_id> <text>", file=sys.stderr)
        raise SystemExit(2)
    open_id, text = sys.argv[1], sys.argv[2]
    app_id, app_secret = load_default_account()
    token = tenant_token(app_id, app_secret)
    try:
        out = send_p2p_text(token, open_id, text)
    except (HTTPError, URLError) as e:
        print(e, file=sys.stderr)
        raise SystemExit(1)
    if out.get("code") != 0:
        print(json.dumps(out, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
    print("ok", int(time.time()))


if __name__ == "__main__":
    main()
