#!/usr/bin/env bash
set -euo pipefail

API_URL="${1:-}"
if [[ -z "$API_URL" ]]; then
  if command -v terraform >/dev/null 2>&1 && [[ -f terraform.tfstate || -d .terraform ]]; then
    API_URL=$(terraform output -raw create_order_url 2>/dev/null || true)
  fi
fi

if [[ -z "$API_URL" ]]; then
  echo "Usage: $0 <create_order_url>"
  exit 1
fi

BASE_URL="${API_URL%/orders}"

echo "1) Creating order..."
CREATE_RESP=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "canvas",
    "buyer_email": "buyer@example.com",
    "tx_hash": "",
    "payment_method": "btc"
  }')
echo "$CREATE_RESP" | python3 -m json.tool

ORDER_ID=$(echo "$CREATE_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('order_id',''))")
if [[ -z "$ORDER_ID" ]]; then
  echo "Failed to create order"
  exit 1
fi

echo
echo "2) Getting order $ORDER_ID ..."
curl -s "$BASE_URL/orders/$ORDER_ID" | python3 -m json.tool

echo
echo "3) Verifying payment (demo)..."
curl -s -X POST "$BASE_URL/orders/verify" \
  -H "Content-Type: application/json" \
  -d "{\"order_id\": \"$ORDER_ID\", \"tx_hash\": \"demo-btc-tx-abc123\", \"force_approve\": true}" \
  | python3 -m json.tool

echo
echo "Flow completed."
