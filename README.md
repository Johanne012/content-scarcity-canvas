# Content Scarcity Canvas

**Limited Digital Products — Sales close permanently on 31 January 2027**

This is not an open-ended offer.  
After **31 January 2027**, no new purchases will be accepted.

---

## Paths

| Path | Purpose | Link |
|------|---------|------|
| **1. GitHub Sales** | Manual purchase + file delivery | This repository |
| **2. Visual Store** | Clean storefront for buyers | [Vercel Store](https://content-scarcity-store-zyntra.vercel.app) |
| **3. LocalStack** | Local AWS-like order stack | [`/localstack-terraform`](./localstack-terraform) |
| **4. Payment Automation** | **On-chain verify + auto download** | [`/payment-automation`](./payment-automation) |

---

## Products

| Product | Price |
|---------|-------|
| Content Scarcity Canvas | $29 |
| Scarcity Playbook | $79 |
| Complete Bundle | $129 |
| Scarcity Checklist | $19 |
| Message Templates | $39 |
| Decision Tool | $49 |

Details: [`PRODUCTS.md`](./PRODUCTS.md)

---

## How to Buy

### Automated (when payment server is running)
1. Create order → `POST /orders`
2. Pay USDT (ERC-20) or Bitcoin
3. Verify → `POST /orders/{id}/verify` with tx id
4. Download → `GET /download/{token}`

### Manual fallback
1. Pay
2. Send template from [`ORDER.md`](./ORDER.md)
3. Receive files after confirmation

### Payment addresses
- **USDT ERC-20:** `0xfe94ddcc4799199cea5c4debb0e9d2ebfb7c813d`
- **Bitcoin:** `bc1q4xr3k7ygeyc7s8nmt0ek4gdcelp6emfudtv99u`
- **Lightning:** request invoice after product choice

> USDT **only on Ethereum (ERC-20)**.

---

## Docs

| File | Purpose |
|------|---------|
| [`PRODUCTS.md`](./PRODUCTS.md) | Catalog |
| [`PAYMENT.md`](./PAYMENT.md) | Payment methods |
| [`ORDER.md`](./ORDER.md) | Buyer order template |
| [`FULFILLMENT.md`](./FULFILLMENT.md) | Seller checklist |
| [`STATUS.md`](./STATUS.md) | Live status |
| [`payment-automation/`](./payment-automation) | Blockchain verify + auto delivery |
| [`localstack-terraform/`](./localstack-terraform) | Local infra stack |

---

## Scarcity Rules

- Sales end permanently on **31 January 2027**
- No extensions
- Price fixed in USD equivalent at payment time

**Available until 31 January 2027**
