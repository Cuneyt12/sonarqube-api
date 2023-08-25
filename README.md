# Kullanım Talimatları
##### [Pyton 3.10](https://www.python.org/downloads/) kurun
##### [SonarQube 9.6.1](https://www.sonarqube.org/downloads/) versiyonunu indirip klasöre çıkartın
##### [Sonar-scanner](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/) indirip SonarQube 9.6.1 klasörünün içine kopyalayın
##### [JDK 11](https://www.oracle.com/tr/java/technologies/javase/jdk11-archive-downloads.html) kurup .\Program Files\Java\jdk11\bin klasörünü [ortam değişkenlerine](https://www.youtube.com/watch?v=z0nVc4lD9QI) ekleyin
##### .\sonarqube-9.6.1.59531\bin\windows-x86-64 klasörü içinden StartSonar.bat dosyasını çalıştırın.
##### Sonar başlatıldıktan sonra localhost:9000 adresine gidip kullanıcı adı ve şifre belirleyin
##### Proje dosyası içindeki sonar.py ve GetDetails.py dosyalarında bulunan username ve password alanlarını kendinize göre doldurun
##### `requirements.txt` dosyası içindeki kütüphaneleri yükleyin
```bash
  pip install -r requirements.txt
```
##### Bilgisayarınızdaki bir projenin analizini yapmak istiyorsanız, bu(sonarqube-api) proje klasörünün içinde 'repos' adında bir klasör oluşturun
##### Analizini yapmak istediğiniz projeyi 'repos' klasörünün içine kopyalayın ve uygulamayı başlattıktan sonra adımları takip edin.
##### Github projelerinin analizini gerçekleştirmek istiyorsanız, istediğiniz projelerin master branchlerinin clone linklerini repos.txt dosyasına kaydedin.
##### `sonar.py` dosyasını çalıştırdıktan sonra proje klasörü içindeki `rapor` klasöründen analiz sonuçlarını görebilirsiniz.
