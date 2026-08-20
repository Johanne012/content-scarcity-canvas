"""Content Scarcity Payment API with webhooks + API key admin routes."""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr

from . import orders as order_store
from .blockchain import verify_payment
from .config import BTC_ADDRESS, ETH_USDT_ADDRESS, FILES_DIR, PRODUCTS
from .security import require_api_key
from .webhooks import emit_webhook

app = FastAPI(
    title="Content Scarcity Payment Automation",
    version="1.1.0",
    description="On-chain verify, auto delivery, webhooks, API key admin",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateOrderRequest(BaseModel):
    product_id: str
    buyer_email: EmailStr
    payment_method: str = "usdt"


class VerifyRequest(BaseModel):
    tx_id: str
    payment_method: str | None = None


@app.get("/health")
def health():
    return {"status": "ok", "service": "content-scarcity-payments", "version": "1.1.0"}


@app.get("/products")
def list_products():
    return {
        "products": [
            {"id": k, **v, "payment_addresses": {"usdt_erc20": ETH_USDT_ADDRESS, "btc": BTC_ADDRESS}}
            for k, v in PRODUCTS.items()
        ],
        "deadline": "2027-01-31",
    }


@app.post("/orders")
async def create_order(body: CreateOrderRequest):
    if body.product_id not in PRODUCTS:
        raise HTTPException(400, f"Unknown product_id: {list(PRODUCTS)}")
    order = order_store.create_order(body.product_id, str(body.buyer_email), body.payment_method)
    await emit_webhook("order.created", {
        "order_id": order["order_id"],
        "product_id": order["product_id"],
        "product_name": order["product_name"],
        "price_usd": order["price_usd"],
        "buyer_email": order["buyer_email"],
        "payment_method": order["payment_method"],
    })
    return {
        "order_id": order["order_id"],
        "product_name": order["product_name"],
        "price_usd": order["price_usd"],
        "status": order["status"],
        "pay": {
            "usdt_erc20": {"address": ETH_USDT_ADDRESS, "network": "Ethereum ERC-20", "amount_hint_usd": order["price_usd"]},
            "btc_onchain": {"address": BTC_ADDRESS, "amount_hint_usd": order["price_usd"]},
        },
        "next_step": f"Pay then POST /orders/{order['order_id']}/verify with tx_id",
    }


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = order_store.get_order(order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    safe = dict(order)
    if safe.get("download_token"):
        safe["download_path"] = f"/download/{safe['download_token']}"
    return safe


@app.post("/orders/{order_id}/verify")
async def verify_order(order_id: str, body: VerifyRequest):
    order = order_store.get_order(order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    if order.get("status") in ("paid", "delivered") and order.get("download_token"):
        return {
            "message": "Already paid",
            "order_id": order_id,
            "status": order.get("status"),
            "download_path": f"/download/{order['download_token']}",
            "download_expires_at": order.get("download_expires_at"),
        }

    method = (body.payment_method or order.get("payment_method") or "usdt").lower()
    result = await verify_payment(method=method, tx_id=body.tx_id, expected_usd=float(order["price_usd"]))
    order_store.update_order(order_id, tx_id=body.tx_id.strip(), payment_method=method, verification=result)

    if not result.get("ok"):
        order_store.update_order(order_id, status="verification_failed")
        await emit_webhook("order.verification_failed", {"order_id": order_id, "verification": result})
        raise HTTPException(402, detail={"message": "Payment verification failed", "verification": result})

    token_info = order_store.issue_download_token(order_id)
    await emit_webhook("order.paid", {
        "order_id": order_id,
        "product_id": order.get("product_id"),
        "product_name": order.get("product_name"),
        "buyer_email": order.get("buyer_email"),
        "price_usd": order.get("price_usd"),
        "tx_id": body.tx_id.strip(),
        "payment_method": method,
        "download_path": f"/download/{token_info['download_token']}",
        "download_expires_at": token_info["download_expires_at"],
    })
    return {
        "message": "Payment verified. Download is ready.",
        "order_id": order_id,
        "status": "paid",
        "verification": result,
        "download_path": f"/download/{token_info['download_token']}",
        "download_expires_at": token_info["download_expires_at"],
    }


@app.get("/download/{token}")
async def download_file(token: str):
    order = order_store.validate_download_token(token)
    if not order:
        raise HTTPException(403, "Invalid or expired download token")
    filename = order.get("file") or "file.bin"
    path = FILES_DIR / filename
    if not path.exists():
        FILES_DIR.mkdir(parents=True, exist_ok=True)
        placeholder = FILES_DIR / f"_placeholder_{order['product_id']}.txt"
        placeholder.write_text(
            f"Content Scarcity product: {order.get('product_name')}\nOrder: {order.get('order_id')}\n",
            encoding="utf-8",
        )
        path = placeholder
        filename = placeholder.name
    order_store.update_order(order["order_id"], status="delivered")
    await emit_webhook("order.delivered", {
        "order_id": order["order_id"],
        "product_id": order.get("product_id"),
        "buyer_email": order.get("buyer_email"),
    })
    return FileResponse(path, filename=filename, media_type="application/octet-stream")


@app.get("/admin/orders")
def admin_list_orders(_: str = Depends(require_api_key)):
    return {"orders": order_store.load_orders()}


@app.post("/admin/webhooks/test")
async def admin_test_webhook(_: str = Depends(require_api_key)):
    return await emit_webhook("system.test", {"message": "webhook test from Content Scarcity API"})
