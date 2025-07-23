# Dondurma Üreticisi Online Sipariş ve Yönetim Platformu

## Özellikler
- JWT ile güvenli giriş ve rol tabanlı yetkilendirme
- Müşteri, sipariş, ürün, dağıtım, ödeme, dashboard, log ve otomatik mesaj modülleri
- PostgreSQL desteği (veya SQLite ile hızlı başlatma)
- Modern, ölçeklenebilir ve güvenli mimari
- Docker ile kolay dağıtım

## Kurulum
1. Gerekli ortam değişkenlerini ayarlayın (örn. SECRET_KEY, DATABASE_URL, JWT_SECRET_KEY)
2. Geliştirme için:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```
3. Docker ile başlatmak için:
   ```bash
   docker build -t dondurma-backend .
   docker run -e SECRET_KEY=xxx -e JWT_SECRET_KEY=xxx -e DATABASE_URL=sqlite:///app.db -p 5000:5000 dondurma-backend
   ```

## API Endpointleri
- /api/login, /api/register
- /api/customers, /api/orders, /api/products, /api/delivery, /api/payments, /api/dashboard, /api/logs, /api/auto-message

## Notlar
- WhatsApp ve Google Maps API entegrasyonları için ilgili endpointler hazırdır, anahtarlarınızı ekleyerek kullanabilirsiniz.
- Frontend için React veya başka bir modern framework ile kolayca entegre edilebilir.

## Lisans ve Katkı
- Kodun bir kısmı açık kaynak projelerden ilham alınarak yazılmıştır. Ayrıntılar için CODE_CITATIONS.md dosyasına bakınız.
