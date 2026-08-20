"""Content Scarcity — Payment verification + automated file delivery API"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, Field

from . import orders as order_store
from .blockchain import verify_payment
from .config import BTC_ADDRESS, ETH_USDT_ADDRESS, FILES_DIR, PRODUCTS

app = FastAPI(
    title="Content Scarcity Payment Automation",
    version="1.0.0",
    description="On-chain payment verification (BTC + USDT ERC-20) and automated file delivery",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateOrderRequest(BaseModel):
    product_id: str = Field(..., examples=["canvas", "bundle"])
    buyer_email: EmailStr
    payment_method: str = Field(default="usdt", examples=["usdt", "btc"])


class VerifyRequest(BaseModel):
    tx_id: str = Field(..., description="Bitcoin txid or Ethereum tx hash")
    payment_method: str | None = Field(default=None, description="Override method: usdt | btc")


@app.get("/health")
def health():
    return {"status": "ok", "service": "content-scarcity-payments"}


@app.get("/products")
def list_products():
    return {
        "products": [
            {
                "id": k,
                **v,
                "payment_addresses": {
                    "usdt_erc20": ETH_USDT_ADDRESS,
                    "btc": BTC_ADDRESS,
                },
            }
            for k, v in PRODUCTS.items()
        ],
        "deadline": "2027-01-31",
    }


@app.post("/orders")
def create_order(body: CreateOrderRequest):
    if body.product_id not in PRODUCTS:
        raise HTTPException(400, f"Unknown product_id. Choose one of: {list(PRODUCTS)}")
    try:
        order = order_store.create_order(
            product_id=body.product_id,
            buyer_email=str(body.buyer_email),
            payment_method=body.payment_method,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

    return {
        "order_id": order["order_id"],
        "product_name": order["product_name"],
        "price_usd": order["price_usd"],
        "status": order["status"],
        "pay": {
            "usdt_erc20": {
                "address": ETH_USDT_ADDRESS,
                "network": "Ethereum ERC-20",
                "amount_hint_usd": order["price_usd"],
            },
            "btc_onchain": {
                "address": BTC_ADDRESS,
                "amount_hint_usd": order["price_usd"],
            },
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
    expected = float(order["price_usd"])
    result = await verify_payment(method=method, tx_id=body.tx_id, expected_usd=expected)

    order_store.update_order(
        order_id,
        tx_id=body.tx_id.strip(),
        payment_method=method,
        verification=result,
    )

    if not result.get("ok"):
        order_store.update_order(order_id, status="verification_failed")
        raise HTTPException(
            402,
            detail={
                "message": "Payment verification failed",
                "verification": result,
            },
        )

    token_info = order_store.issue_download_token(order_id)
    updated = order_store.get_order(order_id)

    return {
        "message": "Payment verified. Download is ready.",
        "order_id": order_id,
        "status": "paid",
        "verification": result,
        "download_path": f"/download/{token_info['download_token']}",
        "download_expires_at": token_info["download_expires_at"],
        "buyer_email": updated.get("buyer_email") if updated else None,
        "note": "Share download_path with the buyer. Link expires automatically.",
    }


@app.get("/download/{token}")
def download_file(token: str):
    order = order_store.validate_download_token(token)
    if not order:
        raise HTTPException(403, "Invalid or expired download token")

    filename = order.get("file") or "file.bin"
    path = FILES_DIR / filename
    if not path.exists():
        FILES_DIR.mkdir(parents=True, exist_ok=True)
        placeholder = FILES_DIR / f"_placeholder_{order['product_id']}.txt"
        placeholder.write_text(
            f"Content Scarcity product: {order.get('product_name')}\n"
            f"Order: {order.get('order_id')}\n"
            f"Replace this file with the real digital product at: {path}\n",
            encoding="utf-8",
        )
        path = placeholder
        filename = placeholder.name

    order_store.update_order(order["order_id"], status="delivered")
    return FileResponse(path, filename=filename, media_type="application/octet-stream")
