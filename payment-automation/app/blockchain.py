"""On-chain payment verification using public blockchain APIs.
- Bitcoin: mempool.space
- Ethereum USDT (ERC-20): Etherscan API
"""

from __future__ import annotations

from typing import Any, Optional

import httpx

from .config import (
    AMOUNT_TOLERANCE_USD,
    BTC_ADDRESS,
    ETH_USDT_ADDRESS,
    ETHERSCAN_API_KEY,
    USDT_CONTRACT,
)


async def get_btc_price_usd() -> float:
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get("https://mempool.space/api/v1/prices")
        r.raise_for_status()
        data = r.json()
        return float(data.get("USD", 0))


async def verify_bitcoin_tx(
    txid: str,
    expected_usd: float,
    btc_address: str = BTC_ADDRESS,
) -> dict[str, Any]:
    txid = txid.strip().lower()
    if not txid or len(txid) < 64:
        return {"ok": False, "error": "Invalid Bitcoin txid"}

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"https://mempool.space/api/tx/{txid}")
        if r.status_code == 404:
            return {"ok": False, "error": "Transaction not found"}
        r.raise_for_status()
        tx = r.json()

    status = tx.get("status") or {}
    confirmed = bool(status.get("confirmed"))
    block_height = status.get("block_height")

    paid_sats = 0
    matched_outputs = []
    for vout in tx.get("vout") or []:
        addr = (vout.get("scriptpubkey_address") or "").strip()
        if addr.lower() == btc_address.lower():
            value = int(vout.get("value") or 0)
            paid_sats += value
            matched_outputs.append({"address": addr, "sats": value})

    if paid_sats <= 0:
        return {
            "ok": False,
            "error": f"No output to expected BTC address {btc_address}",
            "txid": txid,
        }

    btc_price = await get_btc_price_usd()
    paid_btc = paid_sats / 1e8
    paid_usd = paid_btc * btc_price if btc_price else 0
    amount_ok = paid_usd + AMOUNT_TOLERANCE_USD >= expected_usd

    result = {
        "ok": bool(amount_ok),
        "chain": "bitcoin",
        "txid": txid,
        "confirmed": confirmed,
        "block_height": block_height,
        "paid_sats": paid_sats,
        "paid_btc": paid_btc,
        "paid_usd_estimate": round(paid_usd, 2),
        "expected_usd": expected_usd,
        "amount_ok": amount_ok,
        "to_address": btc_address,
        "matched_outputs": matched_outputs,
        "error": None if amount_ok else f"Amount too low: ~${paid_usd:.2f} < ${expected_usd}",
    }
    if amount_ok and not confirmed:
        result["warning"] = "Transaction not yet confirmed on-chain"
    return result


async def verify_usdt_erc20_tx(
    tx_hash: str,
    expected_usd: float,
    to_address: str = ETH_USDT_ADDRESS,
) -> dict[str, Any]:
    tx_hash = tx_hash.strip().lower()
    if not tx_hash.startswith("0x"):
        tx_hash = "0x" + tx_hash
    if len(tx_hash) != 66:
        return {"ok": False, "error": "Invalid Ethereum tx hash"}

    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": USDT_CONTRACT,
        "address": to_address,
        "page": 1,
        "offset": 100,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY or "YourApiKeyToken",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get("https://api.etherscan.io/api", params=params)
        r.raise_for_status()
        payload = r.json()

    if str(payload.get("status")) != "1":
        return {
            "ok": False,
            "error": payload.get("result") or payload.get("message") or "Etherscan query failed",
            "hint": "Add a free ETHERSCAN_API_KEY for better reliability",
        }

    results = payload.get("result") or []
    match: Optional[dict] = None
    for item in results:
        if (item.get("hash") or "").lower() == tx_hash:
            match = item
            break

    if not match:
        return {
            "ok": False,
            "error": "USDT transfer to our address not found for this tx hash",
            "tx_hash": tx_hash,
            "checked_address": to_address,
        }

    raw = int(match.get("value") or 0)
    decimals = int(match.get("tokenDecimal") or 6)
    amount = raw / (10 ** decimals)
    to_addr = (match.get("to") or "").lower()
    from_addr = (match.get("from") or "").lower()
    confirmations = int(match.get("confirmations") or 0)

    if to_addr != to_address.lower():
        return {"ok": False, "error": "Transfer not sent to our USDT address"}

    amount_ok = amount + AMOUNT_TOLERANCE_USD >= expected_usd

    return {
        "ok": amount_ok,
        "chain": "ethereum",
        "asset": "USDT",
        "tx_hash": tx_hash,
        "from": from_addr,
        "to": to_addr,
        "amount_usdt": amount,
        "expected_usd": expected_usd,
        "amount_ok": amount_ok,
        "confirmations": confirmations,
        "confirmed": confirmations >= 1,
        "error": None if amount_ok else f"Amount too low: {amount} USDT < ${expected_usd}",
    }


async def verify_payment(
    method: str,
    tx_id: str,
    expected_usd: float,
) -> dict[str, Any]:
    method = (method or "").strip().lower()
    if method in ("btc", "bitcoin", "btc-onchain", "onchain"):
        return await verify_bitcoin_tx(tx_id, expected_usd)

    if method in ("usdt", "usdt-erc20", "erc20", "ethereum"):
        return await verify_usdt_erc20_tx(tx_id, expected_usd)

    if method in ("lightning", "btc-lightning", "ln"):
        return {
            "ok": False,
            "error": "Lightning verification requires your node/invoice system. Use on-chain BTC or USDT for automatic verify.",
            "method": "lightning",
        }

    return {"ok": False, "error": f"Unsupported payment method: {method}"}
