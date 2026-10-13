# Katkıda Bulunma Rehberi (Contributing Guide)

**Kutsal Eşik** projesine katkıda bulunmak istediğiniz için teşekkür ederiz! Bu repo, insanlık tarihinin ortak mirası olan misafirperverlik, cömertlik ve yabancıya hürmet kültürünü belgeleyen açık kaynaklı bir dijital beşeri bilimler platformudur.

---

## Nasıl Katkı Sağlayabilirsiniz?

### 1. Yeni Felsefi veya Edebi Alıntı Ekleme (`data/quotes.json`)
Yeni bir alıntı eklerken şu alanların eksiksiz doldurulmasına özen gösterin:
- `id`: Benzersiz tanımlayıcı (örn: `q_yazaradi_01`)
- `author`: Yazar / Filozof / Metin adı
- `source`: Eser adı ve ilgili bölüm/bölümce
- `period`: Tarihsel dönem (örn: `Antik Çağ`, `Orta Çağ`, `20. Yüzyıl`)
- `culture`: Kültürel / coğrafi aidiyet (örn: `Antik Yunan`, `Anadolu İrfanı`, `Uzak Doğu`)
- `theme`: Tematik etiket
- `text`: Güvenilir Türkçe çeviri metni
- `context`: Tarihsel veya metinsel kısa açıklama

### 2. Kavram Dağarcığını Genişletme (`data/concepts.json`)
Yeni bir kültürel/felsefi konukseverlik kavramı önerirken:
- Kavramın orijinal dildeki adı ve telaffuzu
- Medeniyet ve dönem bilgisi
- 2-3 maddelik temel ilkeler
- Başlıca referans kaynakları

### 3. Akademik Monografiler (`docs/`)
Markdown formatındaki araştırma bölümlerine akademik atıflar, yeni alt başlıklar veya karşılaştırmalı analizler ekleyebilirsiniz.

### 4. Yazılım & Web Portalı (`kutsal_esik/` ve `web/`)
- Arayüz geliştirmeleri (CSS/JS)
- Yeni arama filtreleri veya görselleştirmeler
- CLI özellikleri

---

## Veri Güncelleme Adımları

Veri (`data/*.json`) veya monografi (`docs/*.md`) dosyalarında değişiklik yaptıktan sonra web arayüzü paketini güncellemek için:

```bash
python scripts/build_web_data.py
```

Testleri çalıştırmak için:

```bash
python -m unittest discover -s tests
```

---

## Çekme İsteği (Pull Request) Süreci

1. Bu depoyu çatallayın (Fork).
2. Yeni bir özellik dalı (feature branch) oluşturun: `git checkout -b ozellik/yeni-alinti`.
3. Değişikliklerinizi yapın ve testlerin geçtiğini doğrulayın (`python -m unittest discover -s tests`).
4. Anlaşılır bir commit mesajıyla kaydedin: `git commit -m "feat: Seneca'dan yeni alıntılar eklendi"`.
5. Dalınızı GitHub'a gönderin ve bir Pull Request (PR) açın.
