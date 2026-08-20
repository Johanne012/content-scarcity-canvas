# Content Scarcity — Blockchain Payment + Auto Delivery

نظام تحقق دفع عبر البلوكتشين + تسليم ملفات تلقائي.

## التدفق

1. `POST /orders` — إنشاء طلب
2. المشتري يدفع USDT (ERC-20) أو Bitcoin
3. `POST /orders/{id}/verify` — تحقق على السلسلة
4. `GET /download/{token}` — تحميل الملف تلقائياً

## التشغيل

```bash
cd payment-automation
pip install -r requirements.txt
cp .env.example .env
# ضع ملفات المنتجات في ./files/
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

API docs: http://localhost:8080/docs

## التحقق المدعوم

| الطريقة | المصدر |
|---------|--------|
| USDT ERC-20 | Etherscan |
| Bitcoin on-chain | mempool.space |
| Lightning | يدوي (غير آلي بعد) |

## عناوين الدفع

- USDT ERC-20: `0xfe94ddcc4799199cea5c4debb0e9d2ebfb7c813d`
- BTC: `bc1q4xr3k7ygeyc7s8nmt0ek4gdcelp6emfudtv99u`
