# Fulfillment Guide (Internal)

Manual process until automated verification is production-ready.

## Steps

1. **Receive order message** (from buyer)
2. **Verify payment**
   - USDT ERC-20: check tx on Etherscan for address `0xfe94ddcc4799199cea5c4debb0e9d2ebfb7c813d`
   - BTC on-chain: check address `bc1q4xr3k7ygeyc7s8nmt0ek4gdcelp6emfudtv99u`
   - Lightning: confirm invoice paid
3. **Match amount** to product price (USD equivalent at time of payment)
4. **Deliver files** to buyer email
5. **Record order** (date, product, tx, email, status)

## Product files (map)

| Product | Suggested file |
|---------|----------------|
| Canvas | CONTENT_SCARCITY_CANVAS.md / PDF |
| Playbook | (expand from canvas + templates) |
| Bundle | package of all |
| Checklist | checklist extract |
| Templates | message templates |
| Decision Tool | decision matrix |

## Status values

- `pending` — waiting for payment proof
- `paid` — payment confirmed
- `delivered` — files sent
- `closed` — after 31 Jan 2027 no new orders

## Automation path

LocalStack stack under `localstack-terraform/` supports:
- `POST /orders` create order
- `GET /orders/{id}` status
- `POST /orders/verify` demo verification

Replace demo verify with real chain checks before production use.
