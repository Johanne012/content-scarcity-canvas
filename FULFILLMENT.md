# Fulfillment Guide

## Automated path (preferred when server is running)

1. Buyer creates order via API or you create it for them
2. Buyer pays USDT (ERC-20) or BTC on-chain
3. Call verify endpoint with tx id
4. System checks blockchain and issues download link
5. Buyer downloads file (token expires automatically)

See `payment-automation/README.md`.

## Manual fallback

1. Receive order message (`ORDER.md`)
2. Verify payment:
   - USDT: Etherscan → address `0xfe94ddcc4799199cea5c4debb0e9d2ebfb7c813d`
   - BTC: explorer → address `bc1q4xr3k7ygeyc7s8nmt0ek4gdcelp6emfudtv99u`
3. Match amount to product price
4. Send digital file to buyer email
5. Mark order delivered

## Status values

- `pending_payment`
- `verification_failed`
- `paid`
- `delivered`
- `closed` (after 31 Jan 2027)
