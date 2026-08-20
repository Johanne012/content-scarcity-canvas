# Content Scarcity Canvas

**Limited Digital Products — Sales close permanently on 31 January 2027**

This is not an open-ended offer.  
After **31 January 2027**, no new purchases will be accepted.

---

## Three Parallel Paths

| Path | Purpose | Link |
|------|---------|------|
| **1. GitHub Sales** | Manual purchase + file delivery | This repository |
| **2. Visual Store** | Clean storefront for buyers | [content-scarcity-store-zyntra.vercel.app](https://content-scarcity-store-zyntra.vercel.app) |
| **3. LocalStack Stack** | Automated order system (dev/local) | [`/localstack-terraform`](./localstack-terraform) |

---

## Why This Exists

Most content advice tells you to publish more.  
This framework teaches the opposite: how to create value by making content **scarcer**, not more abundant.

Built on the same principle that made the Million Dollar Homepage work: limited supply + clear deadline + ownership.

---

## Products

| Product | Price | Description |
|---------|-------|-------------|
| **Content Scarcity Canvas** | $29 | One-page framework (5 scarcity levers) |
| **Scarcity Playbook** | $79 | Expanded guide + examples + templates |
| **Complete Bundle** | $129 | Canvas + Playbook + Checklist + Templates |
| **Scarcity Checklist** | $19 | Practical checklist for any content piece |
| **Message Templates** | $39 | Ready messages for emails, posts, offers |
| **Decision Tool** | $49 | Choose the right scarcity lever |

Full details: [`PRODUCTS.md`](./PRODUCTS.md)

---

## Payment Options

| Priority | Method | Notes |
|----------|--------|-------|
| 1 | **USDT (ERC-20)** | Preferred – stable value |
| 2 | **Bitcoin Lightning** | Fast & low fees |
| 3 | **Bitcoin On-chain** | Standard transfer |

**USDT / Ethereum:**  
`0xfe94ddcc4799199cea5c4debb0e9d2ebfb7c813d`

**Bitcoin (On-chain):**  
`bc1q4xr3k7ygeyc7s8nmt0ek4gdcelp6emfudtv99u`

**Bitcoin Lightning:**  
Request invoice after choosing the product.

> Send USDT **only on Ethereum (ERC-20)**. Other networks = permanent loss.

More details: [`PAYMENT.md`](./PAYMENT.md)

---

## How to Buy

1. Choose your product.
2. Send the exact amount (USD equivalent).
3. Message with: **Transaction ID** + **Product name** + **Email**.
4. Receive files after confirmation.

---

## Scarcity Rules

- Sales end permanently on **31 January 2027**.
- No extensions.
- No second edition of these packages after the deadline.
- Price fixed in USD equivalent at payment time.

---

## Technical Path (for developers)

Local automated delivery stack using LocalStack + Terraform:

```bash
cd localstack-terraform
make all
```

Includes S3, DynamoDB, Lambda, API Gateway for order creation and (demo) payment verification.

See [`localstack-terraform/README.md`](./localstack-terraform/README.md).

---

## Status

**Available until 31 January 2027**

After that date, this offer closes forever.
