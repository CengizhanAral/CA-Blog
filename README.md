# CA-Blog Blog Platformu
Bu proje, Django web çatısı kullanılarak oluşturulmuş, modern ve zengin özelliklere sahip, çok dilli bir blog platformudur. Kullanıcıların kayıt olup yazı yazabildiği, yetkilendirme sistemine sahip, yönetimi kolay ve kullanıcı dostu bir yapı sunar.
## Özellikler
Gelişmiş Yönetim Paneli: django-jazzmin ile güzelleştirilmiş, kullanımı kolay admin paneli.

Zengin Metin Editörü: django-ckeditor ile yazılara HTML destekli, zengin içerik (resim, video, formatlama) ekleyebilme.

Çoklu Dil Desteği: Türkçe ve İngilizce dillerinde tam site desteği (i18n).

Koyu/Açık Tema: Kullanıcıların tercihine göre değişen ve tarayıcıda saklanan tema desteği.

Yazılar için tahmini okuma süresi hesaplama.

Yazıların görüntülenme sayısını takip etme.

Gelişmiş arama özelliği.

E-posta Bülteni Aboneliği ve yönetim panelinden aboneleri dışa aktarma.

### Kullanıcı ve Yetki Yönetimi
Kullanıcı kayıt ve giriş sistemi.

Kullanıcıların profillerini (hakkında, sosyal medya linkleri... vb) düzenleyebilmesi.

Yazar, Editör ve istenilen farklı kullanıcı rolleri ve yetkileri.

Yazarların sadece kendi yazılarını görmesi ve düzenlemesi.

Yazıların yayınlanması için "Onay Bekliyor" süreci ve özel yayınlama yetkisi. 

Not: Yukarıda bahsedilen roller tanımlı bir şekilde gelmemektedir. Grup oluşturup yetki tanımlamaları yapılarak yukarıdaki sonuç elde edilebilir.

### İçerik Yönetimi
Yazarlar ve Kategoriler oluşturma.

Yazıları kategoriye ve yazara göre filtreleme.

SEO uyumlu URL yapıları (/kategori/web-gelistirme/, /yazar/kullanici-adi/).

### Kullanıcı Etkileşimi Özellikleri
Yazılara yorum yapabilme.
Yorumlara yanıt verebilme.

Ziyaretçi/Kayıtlı kullanıcı ayrımı.

Yazıların sosyal medyada (Twitter, Facebook, Reddit WhatsApp, Telegram) paylaşılabilmesi.

## 🚀 Kurulum
Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.
### 1. Projeyi Klonlayın (veya İndirin)
> git clone https://github.com/CengizhanAral/CA-Blog.git

> cd [proje-klasoru]

### 2. Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin
Sanal ortam oluşturma
> python -m venv venv
Sanal ortamı aktif etme
Windows için:
> venv\Scripts\activate
macOS / Linux için:
> source venv/bin/activate

###3. Gerekli Paketleri Yükleyin
Proje için gerekli tüm kütüphaneleri requirements.txt dosyasından yükleyin.
> pip install -r requirements.txt

### 4. Veritabanını Oluşturun
Modelleri veritabanına yansıtmak için migrate komutunu çalıştırın.

> python manage.py migrate
### 5. Süper Kullanıcı (Admin) Oluşturun
Yönetim paneline erişmek için bir süper kullanıcı oluşturun.

> python manage.py createsuperuser

Komut sizden bir kullanıcı adı, e-posta ve şifre isteyecektir.
### 6. Çeviri Dosyalarını Derleyin
Projedeki çevirilerin aktif olması için aşağıdaki komutu çalıştırın.

> python manage.py compilemessages

## 🖥️ Çalıştırma
Sunucuyu başlatmak için aşağıdaki komutu çalıştırın.

> python manage.py runserver

Artık tarayıcınızdan aşağıdaki adreslere erişebilirsiniz.

Ana Sayfa: http://127.0.0.1:8000/

Yönetim Paneli: http://127.0.0.1:8000/admin/

## 🛠️ Yönetim ve Kullanım
Yukarıda bahsedilen yazarlar ve editörler gruplarını oluşturmak için aşağıdaki adımları takip edebilirsiniz.

Proje bu iki kullanıcı rolü düşünülerek oluşturulmuştur. Yine de bu roller olmadan işlevli bir biçimde kullanılabilir.

Rolleri admin panelindeki Gruplar (Groups) bölümünden yönetebilirsiniz.

Bu bahsedilen iki rolün özellikleri aşağıda yazmaktadır. Buna göre kendiniz oluşturabilir ya da farklı roller de oluşturabilirsiniz.

### Yazarlar Grubu:
Sadece kendi yazılarını görebilir ve düzenleyebilir.

Yazı durumunu sadece "Taslak" veya "Onay Bekliyor" olarak ayarlayabilir.

Yeni yazı ekleyebilir (blog | post | Can add post yetkisi).

### Editörler Grubu:
Yazarların tüm yetkilerine sahiptir.
Ek olarak, yazıların durumunu "Yayınlandı" yapabilir (blog | post | Can publish post yetkisi).

Yazıların yazarını değiştirebilir (blog | post | Can change post author yetkisi).

Yeni bir kullanıcı kaydolduğunda, varsayılan olarak yazı yazma yetkisi yoktur. Bir kullanıcıya yazma yetkisi vermek için admin panelinden o kullanıcıyı Yazarlar veya Editörler grubuna eklemeniz gerekir.


### Bülten Yönetimi
Admin panelindeki Bülten Aboneleri bölümünden tüm aboneleri listeleyebilirsiniz.
Bu sayfadaki "Eylemler" (Actions) menüsünü kullanarak seçtiğiniz aboneleri CSV dosyası olarak dışa aktarabilirsiniz. Bu, e-posta pazarlama araçlarıyla entegrasyon için kullanışlıdır.
