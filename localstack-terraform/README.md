# Content Scarcity — LocalStack + Terraform

نظام محلي متكامل لمحاكاة تسليم المنتجات الرقمية عبر خدمات AWS باستخدام **LocalStack**.

## المعمارية

```
Buyer Request
     │
     ▼
API Gateway (HTTP)
     │
     ▼
Lambda (create / get / verify order)
     │
     ├── DynamoDB (orders)
     ├── DynamoDB (catalog)
     └── S3 (product files + presigned URLs)
```

## المسارات (API)

| Method | Path | الوظيفة |
|--------|------|---------|
| `POST` | `/orders` | إنشاء طلب + رابط تحميل مؤقت |
| `GET` | `/orders/{order_id}` | جلب حالة الطلب |
| `POST` | `/orders/verify` | تأكيد الدفع (وضع تجريبي) |

## التشغيل السريع

```bash
make up
make init
make apply
make seed
make test
```

أو دفعة واحدة:

```bash
make all
```

## ملاحظات الإنتاج

- `/orders/verify` حالياً **تجريبي**.
- قبل الإنتاج: تحقق حقيقي من معاملات Bitcoin / USDT.
- لا ترجع رابط التحميل للعميل إلا بعد `status = paid`.
