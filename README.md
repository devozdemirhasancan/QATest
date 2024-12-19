# QA Test API

Bu proje, QA test senaryolarını test etmek için oluşturulmuş basit bir REST API'dir. Flask ve OpenAPI (Swagger) kullanılarak geliştirilmiştir.

## Özellikler

- RESTful API endpoints
- OpenAPI/Swagger dokümantasyonu
- Docker desteği
- Coolify deployment yapılandırması
- Mock veri desteği

## API Endpoints

- `/` - Swagger UI (API dokümantasyonu)
- `/api/users` - Kullanıcı işlemleri
  - `GET /api/users` - Tüm kullanıcıları listele
  - `POST /api/users` - Yeni kullanıcı oluştur
  - `GET /api/users/<id>` - Belirli bir kullanıcıyı getir
- `/api/products` - Ürün işlemleri
  - `GET /api/products` - Tüm ürünleri listele
  - `GET /api/products/<id>` - Belirli bir ürünü getir

## Kurulum

### Docker ile Kurulum

```bash
# Repository'yi klonlayın
git clone <repository-url>
cd qa-test-api

# Docker container'ı build edin ve çalıştırın
docker-compose up --build
```

### Manuel Kurulum

```bash
# Repository'yi klonlayın
git clone <repository-url>
cd qa-test-api

# Virtual environment oluşturun (opsiyonel)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
.\venv\Scripts\activate  # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
python app.py
```

## API Kullanımı

### Swagger UI

API'yi test etmek için tarayıcınızda `http://localhost:3000` adresine gidin. Burada tüm endpoint'leri görebilir ve test edebilirsiniz.

### Curl Örnekleri

```bash
# Tüm kullanıcıları getir
curl http://localhost:3000/api/users

# Yeni kullanıcı oluştur
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"Test User","email":"test@example.com"}' \
     http://localhost:3000/api/users

# Belirli bir ürünü getir
curl http://localhost:3000/api/products/1
```

## Coolify Deployment

Projeyi Coolify üzerinde deploy etmek için:

1. Coolify dashboard'unuza giriş yapın
2. Yeni bir servis ekleyin
3. Bu repository'yi bağlayın
4. Deploy butonuna tıklayın

Coolify, `.coolify/coolify.json` dosyasındaki yapılandırmayı kullanarak otomatik olarak deploy işlemini gerçekleştirecektir.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın. 