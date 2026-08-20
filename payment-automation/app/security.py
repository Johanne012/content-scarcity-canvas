"""API key authentication for admin/protected routes."""

from __future__ import annotations

import hmac
import os
from fastapi import Header, HTTPException


def get_api_key() -> str:
    return os.getenv("API_KEY", "").strip()


def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    expected = get_api_key()
    if not expected:
        return ""
    if not x_api_key or not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")
    return x_api_key
