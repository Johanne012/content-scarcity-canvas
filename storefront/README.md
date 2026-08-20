# Integrated Checkout Storefront

واجهة شراء مربوطة بـ `payment-automation` API.

## التدفق

1. اختيار منتج
2. إنشاء طلب عبر `POST /orders`
3. عرض عناوين الدفع
4. إدخال Tx Hash
5. `POST /orders/{id}/verify`
6. رابط تحميل تلقائي

## الاستخدام

1. شغّل الـ API:
```bash
cd payment-automation
uvicorn app.main:app --port 8080
```

2. افتح `index.html` أو انشره على Vercel
3. ضع رابط الـ API في الحقل أعلى الصفحة
