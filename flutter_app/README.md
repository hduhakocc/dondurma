# Flutter Mobil Uygulama

Bu dizin, dondurma üreticisi yönetim platformunun Flutter tabanlı mobil istemcisi için ayrılmıştır.

## Temel Özellikler
- JWT ile giriş
- Müşteri ve sipariş listeleme
- Sipariş oluşturma
- Ürün ve stok görüntüleme
- Dashboard özetleri

## Backend ile Entegrasyon
- Tüm istekler `/api` ile başlayan endpointlere yapılır.
- Giriş sonrası alınan JWT token, Authorization header'ında taşınır.

## Kurulum
1. Flutter SDK kurulu olmalı.
2. Bu dizinde `flutter pub get` komutunu çalıştırın.
3. Geliştirme için:
   ```bash
   flutter run
   ```

## Notlar
- Kod örnekleri ve temel sayfa yapısı eklenecektir.
