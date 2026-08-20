#!/usr/bin/env bash
set -euo pipefail

ENDPOINT="${LOCALSTACK_ENDPOINT:-http://localhost:4566}"
TABLE="${PRODUCTS_TABLE:-content-scarcity-catalog-local}"
BUCKET="${PRODUCTS_BUCKET:-content-scarcity-products-local}"

echo "Seeding products into $TABLE ..."

seed() {
  local id="$1"
  local name="$2"
  local price="$3"
  local key="$4"

  aws --endpoint-url="$ENDPOINT" dynamodb put-item \
    --table-name "$TABLE" \
    --item "{
      \"product_id\": {\"S\": \"$id\"},
      \"name\": {\"S\": \"$name\"},
      \"price_usd\": {\"S\": \"$price\"},
      \"s3_key\": {\"S\": \"$key\"},
      \"active\": {\"BOOL\": true}
    }"

  echo "Digital product placeholder for $name" > "/tmp/$key"
  aws --endpoint-url="$ENDPOINT" s3 cp "/tmp/$key" "s3://$BUCKET/$key" >/dev/null
  echo "  + $id ($name) \$$price"
}

seed "canvas" "Content Scarcity Canvas" "29" "canvas.pdf"
seed "playbook" "Scarcity Playbook" "79" "playbook.pdf"
seed "bundle" "Complete Scarcity Bundle" "129" "bundle.zip"
seed "checklist" "Content Scarcity Checklist" "19" "checklist.pdf"
seed "templates" "Scarcity Message Templates" "39" "templates.pdf"
seed "decision-tool" "Scarcity Decision Tool" "49" "decision-tool.pdf"

echo "Done."
