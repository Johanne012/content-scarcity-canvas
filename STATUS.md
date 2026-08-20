# Project Status

Last update: 2026-08-20

## Sales

- **Status:** OPEN
- **Closes:** 31 January 2027 (permanent)
- **Channels:** GitHub + Vercel storefront
- **Payment:** USDT ERC-20 / BTC / Lightning

## Systems

| System | Status | Notes |
|--------|--------|-------|
| GitHub sales repo | Live | Manual + order templates |
| Vercel storefront | Live | https://content-scarcity-store-zyntra.vercel.app |
| LocalStack + Terraform | Ready (local) | Order API demo |
| **Payment Automation** | Ready (code) | On-chain verify + auto download |
| Wix / Whop | Blocked | Account limits |

## Payment Automation

Path: [`payment-automation/`](./payment-automation)

- Verifies **USDT ERC-20** via Etherscan
- Verifies **Bitcoin** via mempool.space
- Issues time-limited download tokens
- Serves product files automatically after `paid`

Run locally:

```bash
cd payment-automation
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --port 8080
```

## Buyer flow (automated)

1. `POST /orders`
2. Pay on-chain
3. `POST /orders/{id}/verify` with tx id
4. `GET /download/{token}`

## Buyer flow (manual fallback)

1. Pay
2. Send [`ORDER.md`](./ORDER.md) template
3. Manual delivery
