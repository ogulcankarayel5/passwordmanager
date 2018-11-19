import sys
import sqlite3
from PyQt5 import QtWidgets
import string
import random
import hashlib


class Baglanti:

    def __init__(self):
        self.baglanti1()

    def baglanti1(self):
        self.baglantı = sqlite3.connect("database.db")
        self.cursor = self.baglantı.cursor()
        self.cursor.execute("create table if not exists üyeler(kullanıcı_ID TEXT,anaşifre TEXT)")
        self.cursor.execute("create table if not exists şifreler(anaşifre TEXT,Uygulamalar TEXT,Şifre TEXT)")
        self.baglantı.commit()

    def register1(self):

        k_adı = str(anaekran.kullanici_girisi.text())
        par = str(anaekran.parola.text())
        k_adı_hashing = hashlib.md5(k_adı.encode('utf-8')).hexdigest()
        par_hashing = hashlib.md5(par.encode('utf-8')).hexdigest()
        self.cursor.execute("select * from üyeler where kullanıcı_ID=?", (k_adı_hashing,))
        data = self.cursor.fetchall()
        if (len(k_adı) == 0 or len(par) == 0):
            anaekran.yazi_alani.setText("Bilgileri doldurun")
        elif (len(par) < 6):
            anaekran.yazi_alani.setText("Şifre 6 karakterden az olamaz ")
        elif (len(data) != 0):
            anaekran.yazi_alani.setText("Boyle bır kullanıcı zaten var ")

        elif (len(k_adı) != 0 and len(par) != 0):
            self.cursor.execute("insert into üyeler values(?,?)", (k_adı_hashing, par_hashing))
            anaekran.yazi_alani.setText("Kayıt başarılı")
            self.baglantı.commit()

    def login(self):
        self.adi = str(anaekran.kullanici_girisi.text())
        self.anasifre = str(anaekran.parola.text())
        self.adi_hashing = hashlib.md5(self.adi.encode('utf-8')).hexdigest()
        self.anasifre_hashing = hashlib.md5(self.anasifre.encode('utf-8')).hexdigest()
        self.cursor.execute("select * from üyeler where anaşifre=?", (self.anasifre_hashing,))

        data = self.cursor.fetchall()

        if (len(self.adi) == 0 or len(self.anasifre) == 0):
            anaekran.yazi_alani.setText("Lütfen bilgileri doldurun")
        elif (len(data) == 0):
            anaekran.yazi_alani.setText("Giriş başarısız")
        else:
            anaekran.yazi_alani.setText("Hoşgeldiniz" + self.adi)
            ıslemler.show()

    def sifre_goster(self):

        self.cursor.execute("select Uygulamalar,Şifre from şifreler where anaşifre=?", (self.anasifre_hashing,))
        liste = self.cursor.fetchall()
        liste = dict(liste)
        if (len(liste) != 0):
            temp = ""
            temp2 = ""
            for i in liste.keys():
                temp += i + "\n"
            for j in liste.values():
                temp2 += j + "\n" + "\n"
            ıslemler.text_edit.setText(str(temp) + "\n" + str(temp2))

    def sifreyi_kaydet1(self):

        tanım = str(sifreuret.tanım_yeri.text())
        şifre = str(sifreuret.olusturulan_sifre_yeri.text())

        self.cursor.execute("select * from üyeler where anaşifre=?", (self.anasifre_hashing,))
        liste = self.cursor.fetchall()
        if (len(liste) != 0):

            self.cursor.execute("insert into şifreler values(?,?,?)", (self.anasifre_hashing, tanım, şifre))
            self.baglantı.commit()
            sifreuret.kaydedildi_yazisi.setText("Şifreniz kaydedildi")
        else:
            sifreuret.kaydedildi_yazisi.setText("Ana şifreniz yanlış.Lütfen tekrar deneyiniz.")

    def sifre_sakla1(self):

        sifre = str(sifresakla.sifre_yeri.text())
        tanım = str(sifresakla.uygulama_yeri.text())

        self.cursor.execute("select * from üyeler where anaşifre=?", (self.anasifre_hashing,))
        liste = self.cursor.fetchall()
        if (len(liste) != 0):

            self.cursor.execute("insert into şifreler values(?,?,?)", (self.anasifre_hashing, tanım, sifre))
            self.baglantı.commit()
            sifresakla.bilgi.setText("Şifreniz kaydedildi")
        else:
            sifresakla.bilgi.setText("Ana şifreniz yanlış tekrar deneyin")

    def sifre_degistir1(self):

        eski_sifre = str(sifredegistir.eski_sifre_yeri.text())
        yeni_sifre = str(sifredegistir.yeni_sifre_yeri.text())
        eski_sifre_hashing = hashlib.md5(eski_sifre.encode('utf-8')).hexdigest()
        yeni_sifre_hashing = hashlib.md5(yeni_sifre.encode('utf-8')).hexdigest()

        self.cursor.execute("select * from üyeler where anaşifre=?", (eski_sifre_hashing,))
        data = self.cursor.fetchall()

        if (len(data) != 0):
            self.cursor.execute("update üyeler set anaşifre=? where anaşifre=?",
                                (yeni_sifre_hashing, eski_sifre_hashing))
            self.cursor.execute("update şifreler set anaşifre=? where anaşifre=?",
                                (yeni_sifre_hashing, eski_sifre_hashing))
            self.baglantı.commit()
            sifredegistir.yazi.setText("Şifreniz başarıyla değiştirildi")
        else:
            sifredegistir.yazi.setText("İşlem başarısız")

    def baglanti_kes(self):
        self.baglantı.close()


class AnaEkran(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        baglanti.baglanti1()

    def init_ui(self):
        self.setWindowTitle("şifre yöneticisi")
        self.setGeometry(400, 40, 680, 680)
        self.setFixedSize(680, 680)

        self.hosgeldiniz = QtWidgets.QLabel("Şifre Yöneticisine Hoşgeldiniz.")

        self.kullanici_yeri = QtWidgets.QLabel("Kullanıcı ID: ")
        self.şifre_yeri = QtWidgets.QLabel("Şifre: ")
        self.kullanici_girisi = QtWidgets.QLineEdit()
        self.parola = QtWidgets.QLineEdit()
        self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
        self.giris = QtWidgets.QPushButton("Giriş")
        self.kayıt_ol = QtWidgets.QPushButton("Kayıt Ol")
        self.yazi_alani = QtWidgets.QLabel("")
        self.sifremi_degistir = QtWidgets.QPushButton("Ana Şifremi degistir")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.hosgeldiniz)
        v_box.addWidget(self.kullanici_yeri)
        v_box.addWidget(self.kullanici_girisi)
        v_box.addWidget(self.şifre_yeri)
        v_box.addWidget(self.parola)
        v_box.addWidget(self.yazi_alani)
        v_box.addStretch()
        v_box.addWidget(self.giris)
        v_box.addWidget(self.kayıt_ol)
        v_box.addWidget(self.sifremi_degistir)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setStyleSheet("background-color:lightblue")
        self.giris.setStyleSheet("background-color:green")
        self.kayıt_ol.setStyleSheet("background-color:yellow")
        self.sifremi_degistir.setStyleSheet("background-color:gray")

        self.setLayout(h_box)
        self.giris.clicked.connect(self.login)
        self.kayıt_ol.clicked.connect(self.register)
        self.sifremi_degistir.clicked.connect(self.sifre_degistir)
        self.show()

    def sifre_degistir(self):
        sifredegistir.show()
        self.close()

    def register(self):
        baglanti.register1()

    def login(self):
        baglanti.login()


class Islemler(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.gorsel()
        baglanti.baglanti1()

    def gorsel(self):
        self.setWindowTitle("İşlemler")
        self.setGeometry(400, 40, 680, 680)
        self.setFixedSize(680, 680)

        self.sifre_buton = QtWidgets.QPushButton("Şifrelerimi sakla ")
        self.sifreleri_goster = QtWidgets.QPushButton("Şifrelerimi göster")
        self.sifre_uret = QtWidgets.QPushButton("Şifre üret")
        self.text_edit = QtWidgets.QTextEdit()
        self.cikis=QtWidgets.QPushButton("Çıkış")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.sifreleri_goster)
        v_box.addWidget(self.text_edit)
        v_box.addStretch()
        v_box.addWidget(self.sifre_uret)
        v_box.addWidget(self.sifre_buton)
        v_box.addWidget(self.cikis)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        self.setLayout(h_box)

        self.setStyleSheet("background-color:lightblue")
        self.sifreleri_goster.setStyleSheet("background-color:turquoise")
        self.sifre_uret.setStyleSheet("background-color:grey")
        self.sifre_buton.setStyleSheet("background-color:green")
        self.cikis.setStyleSheet("background-color:gold")

        self.cikis.clicked.connect(self.cikis_yap)
        self.sifre_uret.clicked.connect(self.sifre_uret2)
        self.sifre_buton.clicked.connect(self.sifre_sakla2)
        self.sifreleri_goster.clicked.connect(self.sifre_goster)

    def cikis_yap(self):
        self.close()
        anaekran.close()

    def sifre_goster(self):
        baglanti.sifre_goster()

    def sifre_uret2(self):
        sifreuret.show()
        self.text_edit.clear()
        self.close()

    def sifre_sakla2(self):
        sifresakla.show()
        self.text_edit.clear()
        self.close()


class Sifreuret(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        baglanti.baglanti1()
        self.islemler()

    def islemler(self):
        self.setWindowTitle("Şifre üret")
        self.setGeometry(400, 40, 680, 680)
        self.setFixedSize(680, 680)

        self.sifre_uret = QtWidgets.QPushButton("Şifre üret")
        self.uzunluk_yazisi = QtWidgets.QLabel("Şifre Uzunluğunu belirtiniz")
        self.uzunluk_yeri = QtWidgets.QLineEdit()
        self.kucuk_harf = QtWidgets.QCheckBox("Küçük harf")
        self.buyuk_harf = QtWidgets.QCheckBox("Büyük harf")
        self.karakter = QtWidgets.QCheckBox("Özel karakter")
        self.sayı = QtWidgets.QCheckBox("Sayı")
        self.olusturulan_sifre = QtWidgets.QLabel("Oluşturulan şifre")
        self.olusturulan_sifre_yeri = QtWidgets.QLineEdit()
        self.kaydet_buton = QtWidgets.QPushButton("Şifreyi Kaydet")
        self.tanım = QtWidgets.QLabel("Şifreyi ne için kaydetmek istiyorsunuz ?")
        self.tanım_yeri = QtWidgets.QLineEdit()

        self.kaydedildi_yazisi = QtWidgets.QLabel("")
        self.geri_dön = QtWidgets.QPushButton("Geri dön")
        self.cikis=QtWidgets.QPushButton("Çıkış")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.uzunluk_yazisi)
        v_box.addWidget(self.uzunluk_yeri)
        v_box.addWidget(self.kucuk_harf)
        v_box.addWidget(self.buyuk_harf)
        v_box.addWidget(self.karakter)
        v_box.addWidget(self.sayı)
        v_box.addWidget(self.sifre_uret)
        v_box.addWidget(self.olusturulan_sifre)
        v_box.addWidget(self.olusturulan_sifre_yeri)
        v_box.addStretch()

        v_box.addWidget(self.tanım)
        v_box.addWidget(self.tanım_yeri)
        v_box.addWidget(self.kaydet_buton)
        v_box.addWidget(self.kaydedildi_yazisi)
        v_box.addStretch()
        v_box.addWidget(self.cikis)
        v_box.addWidget(self.geri_dön)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v_box)

        self.setStyleSheet("background-color:lightblue")
        self.sifre_uret.setStyleSheet("background-color:yellow")
        self.kaydet_buton.setStyleSheet("background-color:orange")

        self.setLayout(h_box)
        self.cikis.clicked.connect(self.cikis_yap)

        self.geri_dön.clicked.connect(self.geri1)
        self.kaydet_buton.clicked.connect(self.sifreyi_kaydet1)
        self.sifre_uret.clicked.connect(lambda: self.sifre_uret1(self.buyuk_harf.isChecked(), self.kucuk_harf.isChecked(),self.karakter.isChecked(), self.sayı.isChecked(), self.olusturulan_sifre_yeri))
    def cikis_yap(self):
        self.close()
        ıslemler.close()
        anaekran.close()


    def geri1(self):
        ıslemler.show()
        self.uzunluk_yeri.clear()
        self.olusturulan_sifre_yeri.clear()
        self.close()

    def sifre_uret1(self, buyuk, kucuk, karakter, sayı, yazı):

        chars = ""
        uzunluk = int(self.uzunluk_yeri.text())

        if kucuk:
            chars += string.ascii_lowercase
        if buyuk:
            chars += string.ascii_uppercase
        if karakter:
            ozel_karakterler = ("!#$/%&*+-:;?@\_")
            chars += ozel_karakterler
        if sayı:
            chars += string.digits

        temp = ""

        for i in range(uzunluk):
            temp += random.choice(chars)
        self.olusturulan_sifre_yeri.setText(str(temp))

    def sifreyi_kaydet1(self):

        baglanti.sifreyi_kaydet1()


class Sifresakla(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        baglanti.baglanti1()

        self.islemler()

    def islemler(self):
        self.setWindowTitle("Şifreleri sakla")
        self.setGeometry(400, 40, 680, 680)
        self.setFixedSize(680, 680)

        self.sifre = QtWidgets.QLabel("Şifreniz")
        self.sifre_yeri = QtWidgets.QLineEdit()

        self.uygulama = QtWidgets.QLabel("Şifrenizi ne için kaydetmek istiyorsunuz ? ")
        self.uygulama_yeri = QtWidgets.QLineEdit()

        self.kaydet = QtWidgets.QPushButton("Şifremi Kaydet")
        self.bilgi = QtWidgets.QLabel("")
        self.geri_dön = QtWidgets.QPushButton("Geri Dön")

        self.cikis=QtWidgets.QPushButton("Çıkış")

        v_box = QtWidgets.QVBoxLayout()

        v_box.addWidget(self.uygulama)
        v_box.addWidget(self.uygulama_yeri)
        v_box.addWidget(self.sifre)
        v_box.addWidget(self.sifre_yeri)
        v_box.addWidget(self.kaydet)
        v_box.addWidget(self.bilgi)
        v_box.addStretch()
        v_box.addWidget(self.geri_dön)
        v_box.addWidget(self.cikis)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v_box)
        h_box.addStretch()
    
        self.setStyleSheet("background-color:lightblue")
        self.cikis.setStyleSheet("background-color:silver")
        self.kaydet.setStyleSheet("background-color:yellow")
        self.geri_dön.setStyleSheet("background-color:grey")

        self.geri_dön.clicked.connect(self.geri1)
        self.cikis.clicked.connect(self.cikis_yap)

        self.setLayout(h_box)
        self.kaydet.clicked.connect(self.sifre_sakla1)
    def cikis_yap(self):
        self.close()
        ıslemler.close()
        anaekran.close()
    def geri1(self):
        ıslemler.show()
        self.sifre_yeri.clear()
        self.uygulama_yeri.clear()
        self.close()



    def sifre_sakla1(self):
        baglanti.sifre_sakla1()


class Sifredegistir(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        baglanti.baglanti1()

        self.islemler()

    def islemler(self):
        self.eski_sifre = QtWidgets.QLabel("Eski şifrenizi girin")
        self.eski_sifre_yeri = QtWidgets.QLineEdit()
        self.eski_sifre_yeri.setEchoMode(QtWidgets.QLineEdit.Password)
        self.yeni_sifre = QtWidgets.QLabel("Yeni şifrenizi girin")
        self.yeni_sifre_yeri = QtWidgets.QLineEdit()
        self.yeni_sifre_yeri.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sifreyi_degistir = QtWidgets.QPushButton("Şifremi değiştir")
        self.yazi = QtWidgets.QLabel("")
        self.girise_don = QtWidgets.QPushButton("Girişe dön")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.eski_sifre)
        v_box.addWidget(self.eski_sifre_yeri)
        v_box.addWidget(self.yeni_sifre)
        v_box.addWidget(self.yeni_sifre_yeri)
        v_box.addWidget(self.sifreyi_degistir)
        v_box.addWidget(self.yazi)
        v_box.addWidget(self.girise_don)
        v_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()

        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)
        self.setWindowTitle("Şifremi degistir")
        self.setGeometry(400, 40, 680, 680)
        self.setFixedSize(680, 680)

        self.setStyleSheet("background-color:lightblue")
        self.sifreyi_degistir.setStyleSheet("background-color:grey")

        self.girise_don.clicked.connect(self.giris1)
        self.sifreyi_degistir.clicked.connect(self.sifre_degistir1)

    def giris1(self):
        anaekran.show()
        self.eski_sifre_yeri.clear()
        self.yeni_sifre_yeri.clear()
        self.close()

    def sifre_degistir1(self):
        baglanti.sifre_degistir1()


app = QtWidgets.QApplication(sys.argv)

baglanti = Baglanti()
anaekran = AnaEkran()
ıslemler = Islemler()
sifreuret = Sifreuret()
sifresakla = Sifresakla()
sifredegistir = Sifredegistir()

sys.exit(app.exec_())


baglanti.baglanti_kes()
