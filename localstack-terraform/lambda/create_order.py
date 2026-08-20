import json
import os
import uuid
from datetime import datetime, timezone, timedelta

import boto3
from botocore.exceptions import ClientError

ORDERS_TABLE = os.environ["ORDERS_TABLE"]
PRODUCTS_TABLE = os.environ["PRODUCTS_TABLE"]
PRODUCTS_BUCKET = os.environ["PRODUCTS_BUCKET"]
DOWNLOAD_TTL_SECONDS = int(os.environ.get("DOWNLOAD_TTL_SECONDS", "3600"))

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

orders_table = dynamodb.Table(ORDERS_TABLE)
products_table = dynamodb.Table(PRODUCTS_TABLE)


def handler(event, context):
    method = (event.get("requestContext") or {}).get("http", {}).get("method", "POST")
    path = event.get("rawPath") or event.get("path") or "/orders"

    try:
        if method == "POST" and path.endswith("/orders"):
            return create_order(event)
        if method == "GET" and "/orders/" in path:
            order_id = path.rstrip("/").split("/")[-1]
            return get_order(order_id)
        if method == "POST" and path.endswith("/verify"):
            return verify_order(event)
        return response(404, {"error": "Route not found"})
    except Exception as e:
        return response(500, {"error": str(e)})


def create_order(event):
    data = parse_body(event)
    product_id = (data.get("product_id") or "").strip()
    buyer_email = (data.get("buyer_email") or "").strip().lower()
    tx_hash = (data.get("tx_hash") or "").strip()
    payment_method = (data.get("payment_method") or "btc").strip().lower()

    if not product_id or not buyer_email:
        return response(400, {"error": "product_id and buyer_email are required"})

    product = products_table.get_item(Key={"product_id": product_id}).get("Item")
    if not product:
        return response(404, {"error": f"Product not found: {product_id}"})
    if not product.get("active", True):
        return response(400, {"error": "Product is not available"})

    order_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=DOWNLOAD_TTL_SECONDS)

    s3_key = product.get("s3_key") or f"{product_id}.zip"
    download_url = None
    try:
        download_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": PRODUCTS_BUCKET, "Key": s3_key},
            ExpiresIn=DOWNLOAD_TTL_SECONDS,
        )
    except ClientError:
        download_url = f"s3://{PRODUCTS_BUCKET}/{s3_key}"

    order = {
        "order_id": order_id,
        "product_id": product_id,
        "product_name": product.get("name", product_id),
        "price_usd": product.get("price_usd", "0"),
        "buyer_email": buyer_email,
        "tx_hash": tx_hash,
        "payment_method": payment_method,
        "status": "pending_verification",
        "download_url": download_url,
        "download_expires_at": expires_at.isoformat(),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }
    orders_table.put_item(Item=order)

    return response(201, {
        "message": "Order created. Payment verification required before delivery in production.",
        "order_id": order_id,
        "status": "pending_verification",
        "product_name": order["product_name"],
        "price_usd": order["price_usd"],
        "download_url": download_url,
        "download_expires_at": order["download_expires_at"],
        "next_step": "Send tx_hash then call POST /orders/verify",
    })


def get_order(order_id):
    item = orders_table.get_item(Key={"order_id": order_id}).get("Item")
    if not item:
        return response(404, {"error": "Order not found"})
    return response(200, item)


def verify_order(event):
    data = parse_body(event)
    order_id = (data.get("order_id") or "").strip()
    tx_hash = (data.get("tx_hash") or "").strip()
    force_approve = bool(data.get("force_approve", False))

    if not order_id:
        return response(400, {"error": "order_id is required"})

    item = orders_table.get_item(Key={"order_id": order_id}).get("Item")
    if not item:
        return response(404, {"error": "Order not found"})

    now = datetime.now(timezone.utc).isoformat()
    approved = force_approve or bool(tx_hash) or bool(item.get("tx_hash"))
    new_status = "paid" if approved else "pending_verification"

    update_expr = "SET #s = :s, updated_at = :u"
    expr_names = {"#s": "status"}
    expr_values = {":s": new_status, ":u": now}

    if tx_hash:
        update_expr += ", tx_hash = :tx"
        expr_values[":tx"] = tx_hash

    orders_table.update_item(
        Key={"order_id": order_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_values,
    )

    updated = orders_table.get_item(Key={"order_id": order_id}).get("Item")
    return response(200, {
        "message": "Order verification processed (demo mode)",
        "order": updated,
        "note": "Replace this logic with real blockchain verification before production use",
    })


def parse_body(event):
    body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        import base64
        body = base64.b64decode(body).decode("utf-8")
    if isinstance(body, dict):
        return body
    return json.loads(body or "{}")


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, default=str),
    }
