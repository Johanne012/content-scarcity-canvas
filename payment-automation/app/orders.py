from __future__ import annotations

import json
import secrets
import time
import uuid
from typing import Any, Optional

from .config import DOWNLOAD_TTL_SECONDS, ORDERS_FILE, PRODUCTS


def _ensure_store() -> None:
    ORDERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not ORDERS_FILE.exists():
        ORDERS_FILE.write_text("[]", encoding="utf-8")


def load_orders() -> list[dict[str, Any]]:
    _ensure_store()
    try:
        return json.loads(ORDERS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_orders(orders: list[dict[str, Any]]) -> None:
    _ensure_store()
    ORDERS_FILE.write_text(json.dumps(orders, indent=2, ensure_ascii=False), encoding="utf-8")


def get_order(order_id: str) -> Optional[dict[str, Any]]:
    for o in load_orders():
        if o.get("order_id") == order_id:
            return o
    return None


def create_order(product_id: str, buyer_email: str, payment_method: str = "usdt") -> dict[str, Any]:
    product = PRODUCTS.get(product_id)
    if not product:
        raise ValueError(f"Unknown product_id: {product_id}")

    order = {
        "order_id": str(uuid.uuid4()),
        "product_id": product_id,
        "product_name": product["name"],
        "price_usd": product["price_usd"],
        "file": product["file"],
        "buyer_email": buyer_email.strip().lower(),
        "payment_method": payment_method.strip().lower(),
        "tx_id": "",
        "status": "pending_payment",
        "created_at": time.time(),
        "updated_at": time.time(),
        "verification": None,
        "download_token": None,
        "download_expires_at": None,
    }
    orders = load_orders()
    orders.append(order)
    save_orders(orders)
    return order


def update_order(order_id: str, **fields: Any) -> Optional[dict[str, Any]]:
    orders = load_orders()
    for i, o in enumerate(orders):
        if o.get("order_id") == order_id:
            o.update(fields)
            o["updated_at"] = time.time()
            orders[i] = o
            save_orders(orders)
            return o
    return None


def issue_download_token(order_id: str) -> dict[str, Any]:
    token = secrets.token_urlsafe(24)
    expires = int(time.time()) + DOWNLOAD_TTL_SECONDS
    update_order(
        order_id,
        download_token=token,
        download_expires_at=expires,
        status="paid",
    )
    return {"download_token": token, "download_expires_at": expires}


def validate_download_token(token: str) -> Optional[dict[str, Any]]:
    if not token:
        return None
    now = time.time()
    for o in load_orders():
        if o.get("download_token") == token:
            exp = o.get("download_expires_at") or 0
            if now > exp:
                return None
            if o.get("status") not in ("paid", "delivered"):
                return None
            return o
    return None
