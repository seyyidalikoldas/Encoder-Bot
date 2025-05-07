# 🎥 Encode Yapan Discord Botu

Bu Discord botu, kullanıcıdan gelen komutlarla anime bölümlerini magnet link üzerinden indirir, altyazı (.ass) dosyasıyla encode eder ve ardından Google Drive gibi platformlara yükler.

---

## 🚀 Özellikler

- 📥 Magnet link ile video indirme (`aria2c` kullanımı)
- 📝 .ass altyazı dosyasını videoya ekleme
- 🎬 Videoya intro ekleyerek encode işlemi yapma (`ffmpeg`)
- ⏳ Encode işlemi sırasında ilerleme takibi
- ☁️ Google Drive'a otomatik yükleme ve link paylaşımı

---

## 📂 Dosya Açıklamaları

| Dosya/Klasör         | Açıklama |
|----------------------|----------|
| `bot.py`             | Discord botunun ana komutlarını içerir |
| `downloader.py`      | Magnet linkten video indirir (`aria2c` ile) |
| `encoder.py`         | Videoyu intro + altyazı ile encode eder |
| `uploader.py`        | Encode edilen videoyu yükler |
| `credentials.json`   | Google API kimlik bilgileri |
| `token.pickle`       | Google Drive yetkilendirme tokeni |
| `downloads/`         | İndirilen ham videoların saklandığı klasör |
| `subs/`              | Altyazı dosyalarının bulunduğu klasör |
| `uploads/`           | Encode edilmiş videoların yüklendiği klasör |
| `intro.mp4`          | Videolara eklenen tanıtım/intro dosyası |
| `new.py`             | Test veya geliştirme amaçlı kod |

---

## 🛠️ Gereksinimler

- Python 3.10+
- `discord.py`
- `aria2c`
- `ffmpeg`
- `google-api-python-client`
- `google-auth`
- `google-auth-oauthlib`

---

## ⚙️ Kurulum

1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install discord.py google-api-python-client google-auth google-auth-oauthlib
   ```

2. `aria2c` ve `ffmpeg` kurulu olmalı (sistem PATH'ine eklenmiş olmalı).

3. `credentials.json` dosyasını Google Cloud Console'dan alarak proje klasörüne yerleştirin.

4. Botu başlatın:
   ```bash
   python bot.py
   ```

---

## 🔐 Gizli Anahtarlar ve Kimlik Dosyaları

Bu projede kullanılacak token ve kimlik bilgileri güvenlik nedeniyle GitHub'a dahil edilmemiştir.

Aşağıdaki dosyaları **kendiniz oluşturmalı veya temin etmelisiniz**:

- `credentials.json`: Google Drive API erişimi için Google Cloud Console üzerinden alınmalı.
- `token.pickle`: İlk yetkilendirme sırasında otomatik olarak oluşur.
- `DISCORD_TOKEN`: Discord geliştirici portalından alınmalı ve `bot.py` içinde belirtilmelidir.

> **UYARI:** Bu dosyalar GitHub'a yüklenmemelidir. `.gitignore` dosyasına şu satırlar eklenmelidir:
>
> ```
> credentials.json
> token.pickle
> ```

---

## 👤 Geliştirici

Bu bot **Seyyid Ali Koldaş** tarafından geliştirilmiştir.  
GitHub: [@seyyidalikoldas](https://github.com/seyyidalikoldas)

---

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
