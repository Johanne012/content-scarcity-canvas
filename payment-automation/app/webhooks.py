"""Outgoing webhooks when order status changes."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import time
from typing import Any

import httpx

logger = logging.getLogger(__name__)


def webhook_url() -> str:
    return os.getenv("WEBHOOK_URL", "").strip()


def webhook_secret() -> str:
    return os.getenv("WEBHOOK_SECRET", "").strip()


def sign_payload(body: bytes, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()


async def emit_webhook(event: str, data: dict[str, Any]) -> dict[str, Any]:
    url = webhook_url()
    if not url:
        return {"sent": False, "reason": "WEBHOOK_URL not configured"}

    payload = {
        "event": event,
        "timestamp": int(time.time()),
        "data": data,
    }
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "ContentScarcity-Webhook/1.0",
        "X-Scarcity-Event": event,
    }
    secret = webhook_secret()
    if secret:
        headers["X-Scarcity-Signature"] = sign_payload(raw, secret)

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(url, content=raw, headers=headers)
        return {"sent": True, "status_code": r.status_code, "ok": 200 <= r.status_code < 300}
    except Exception as e:
        logger.exception("webhook failed")
        return {"sent": False, "error": str(e)}
