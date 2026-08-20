# Systems Overview

Three parallel systems for the Content Scarcity project.

## Path 1 — GitHub Manual Sales

- **Role:** Primary sales page + file distribution
- **Payment:** Manual BTC / USDT / Lightning
- **Delivery:** Manual after payment confirmation
- **Strength:** Simple, transparent, works now
- **Link:** Repository root README

## Path 2 — Visual Store (Vercel)

- **Role:** Buyer-friendly storefront
- **Payment:** Same crypto addresses
- **Delivery:** Manual (same process)
- **Strength:** Clean UI, easier for non-technical buyers
- **Link:** https://content-scarcity-store-zyntra.vercel.app

## Path 3 — LocalStack Technical Stack

- **Role:** Automated order backend (local development)
- **Stack:** Terraform + LocalStack + Lambda + DynamoDB + S3 + API Gateway
- **Endpoints:**
  - `POST /orders` — create order
  - `GET /orders/{id}` — get order
  - `POST /orders/verify` — demo payment verification
- **Strength:** Foundation for future automatic delivery
- **Link:** [`localstack-terraform/`](./localstack-terraform)

### Run Path 3 locally

```bash
cd localstack-terraform
make all
```

Requires: Docker, Terraform, AWS CLI.

---

## Recommended Use Today

1. Sell via **Path 1** or **Path 2**
2. Deliver files manually after confirming payment
3. Use **Path 3** only for development / learning automation

## Future Upgrade Path

Path 3 → replace demo `verify` with real BTC/USDT chain checks → automatic file delivery.
