# Şifreli Mesajlaşma Uygulaması (İstemci Bölümü)

## Proje Hakkında

Şifreli Mesajlaşma Uygulaması'nın istemci kısmıdır.
Bu proje Dündar Çiloğlu Programlama Takımı'nın kodları incelemesi ve geliştirilmesi için Github'a yüklenmiştir.

**Not: _Bu projenin kaynak kodlarını bu grup dışında başka bir kişi ile paylaşmak yasaktır._**

_Not: Şifreli Mesajlaşma Uygulaması'nın sunucu kodlarına [buradan ulaşabilirsiniz.](https://www.google.com)_

## Katkıda Bulunma

### 1) Projeyi İndirmek

Not: Projeye katkıda bulunabilmeniz için Git programının sizde yüklü olması gerekir. [Programı buradan yükleyebilirsiniz.](https://git-scm.com/)

Kaynak kodlarını indirmek için şu komutları sırasıyla girin ve bu kodları kendinize göre ayarladıktan sonra ENTER tuşuna basın:

```sh
git init
git clone https://github.com/berkakkaya/chatapp-client.git
git config --global user.name "Adınız Soyadınız" #Kendi adınızı ve soyadınızı tırnak içerisine girin.
git config --global user.email "e-postanız@gmail.com" #Kendi ana e-posta adresinizi tırnak içerisine girin.
```

Artık projeye katkıda bulunmak için hazırsınız.

### 2) Düzenlemeler için bir dal açmak

Git sisteminde düzenli bir çalışma yapabilmeniz ve projede karmaşa olmaması için Git sistemi üzerinden bir dal oluşturmanız ve düzenlemeleri onun üzerinden yapmanız daha iyi olacaktır.

Şimdi şu komutları sırasıyla girin ve bu kodları kendinize göre ayarladıktan sonra ENTER tuşuna basın:

*Not: Kendi dalınızın adını girmeniz gereken yerler `dal-adi` olarak belirtilmiştir. Buralardaki `dal-adi` belirteçlerinin yerine kendi dalınızın adını giriniz.*

```sh
git branch dal-adi
git checkout dal-adi
```

Artık düzenleme yapmak için hazırsınız.

### 3) Düzenlemeleri incelenmesi için paylaşmak

Düzenlemeniz bittiğinde düzenlemelerinizi yaptığınız dalı master (git sisteminde ana dal) ile birleştirmek (merge) gerekir.
Bu işlemi şöyle gerçekleştirebiliriz:

```sh
git checkout master
```
