#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
!              Şifreli Mesajlaşma Uygulaması - İstemci
!            Hazırlayanlar: Berk Akkaya ve Ozan Alptekin

?=================== YAPILACAKLAR LİSTESİ =========================?
* Şu anlık bir şey yok.
"""

import socketio #? Sunucu ile iletişimi sağlamaya yarayan modül.
import sys #? İşletim sisteminden bilgi almamızı sağlayacak modül.
from src.cheaserDecrypt import decrypt #? Sezar şifreleme yönteminde kullanılacak şifre çözme metodu.
from src.cheaserEncrypt import encrypt #? Sezar şifreleme yönteminde kullanılacak şifreleme metodu.
import src.rsa as rsa #? RSA şifrelemede kullanılacak bir moduül.
from PyQt5.QtWidgets import * #? PyQT uygulamamızda kullanacağımız Widgetler
from PyQt5.QtGui import * #? PyQT arayüz bileşenleri
from PyQt5.QtCore import * #? PyQT sinyalizasyon fonksiyonları ve gerekli ana fonksiyonlar
from plyer import notification #? Bildirim göndermemizi sağlayan modül.
import random #? Rastgele renk seçiminde kullanılacak olan modül.

#? Sunucuyla bağlantı sağlayacak olan socketi yapılandırır.
websocket = socketio.Client()

class App(QMainWindow):
    """
    ? Uygulama arayüz kısmında PyQT altyapısını kullanıyor.
    ? Uygulamamızı oluştururken PyQT'ye oluşturacağımız uygulama ile ilgili bilgileri bu sınıfta veririz ve arayüzü hazırlarız.
    """

    def __init__(self, monitor):
        """
        ? Belirli uygulama özelliklerinin belirtildiği fonksiyondur. Ayrıca arayüzü hazırlar.
        """
        super().__init__()
        self.title = 'Şifreli Mesajlaşma Programı'
        self.left = 0
        self.top = 0
        self.width = 450
        self.height = 650
        self.monitor = monitor
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Durum: Kullanıcı bekleniyor...")

        self.table_widget = Widgets(self, monitor=self.monitor, statusBar=self.statusBar)
        self.setCentralWidget(self.table_widget)

        self.setWindowIcon(QIcon("./speech-bubble.png"))

        self.show()

class Widgets(QWidget):
    """
    ? Arayüz bileşenlerinin tanıtıldığı ve hazırlandığı sınıftır.
    """
    def __init__(self, parent, monitor, statusBar):
        """
        ? Bu fonksiyon arayüzün bütün bileşenlerini tanıtır ve uygulamayı kullanıma hazırlar.
        """

        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.monitor = monitor

        self.connectionStatus = statusBar

        self.isLogined = False
        self.isReady = False

        self.messageHistory = "" #? Mesaj geçmişi bu değişkende saklanır.

        self.adminCommands = [] #? Yönetici komutları burada belirtilir. Şu anlık olmadığı için boştur.
        self.commands = ["!renkdeğiştir"] #? Kullanıcıların kullanabileceği komutlar burada belirtilir.
        
        #? Sekme ekranını hazırla
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tabs.resize(450, 700)
        
        #? Sekmeleri uygulamada tanımla
        self.tabs.addTab(self.tab1, "Giriş Yap")
        self.tabs.addTab(self.tab2, "Sohbet")
        self.tabs.addTab(self.tab3, "Şifreleme Ayarları")
        self.tabs.addTab(self.tab4, "Yönetici Paneli")
        self.tabs.addTab(self.tab5, "Program Hakkında")
        
        #? Birinci Sekmeyi oluştur. - Giriş Yap
        self.tab1.layout = QVBoxLayout(self)

        self.inputContainer = QWidget()
        self.inputContainerLayout = QGridLayout()
        self.tab1.layout.setSpacing(1)
        
        self.loginTitle = QLabel("Hoş geldiniz!")
        self.loginTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.loginTitleFont = QFont("Droid Sans", 24, QFont.Bold)
        self.loginTitle.setAlignment(Qt.AlignCenter)
        self.loginTitle.setFont(self.loginTitleFont)

        self.nameBoxLabel = QLabel("Kullanıcı adınız:")
        self.nameBox = QLineEdit()
        self.nameBox.textChanged.connect(self.usernameChanged)

        self.serverBoxLabel = QLabel("Bağlanacağınız sunucu adresi:")
        self.serverBox = QLineEdit()
        self.serverBox.setText("http://localhost:8080")

        self.loginButton = QPushButton("Giriş Yap")
        self.loginButton.clicked.connect(self.login)
        
        self.inputContainerLayout.addWidget(self.nameBoxLabel, 0, 0)
        self.inputContainerLayout.addWidget(self.nameBox, 0, 1)
        self.inputContainerLayout.addWidget(self.serverBoxLabel, 1, 0)
        self.inputContainerLayout.addWidget(self.serverBox, 1, 1)
        self.inputContainer.setLayout(self.inputContainerLayout)

        self.tab1.layout.addWidget(self.loginTitle)
        self.tab1.layout.addWidget(self.inputContainer)
        self.tab1.layout.addWidget(self.loginButton)
        self.tab1.setLayout(self.tab1.layout)

        #? İkinci sekmeyi oluştur - Sohbet
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.setSpacing(1)

        self.chatContainer = QWidget()
        self.chatContainerLayout = QGridLayout()

        self.chatBox = QTextBrowser()
        self.chatBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chatBox.setReadOnly(True)

        self.messageBox = QLineEdit()
        self.messageBox.setEnabled(False)

        self.sendButton = QPushButton("Gönder")
        self.sendButton.setEnabled(False)
        self.sendButton.clicked.connect(self.sendMessage)

        self.chatContainerLayout.addWidget(self.messageBox, 0, 0)
        self.chatContainerLayout.addWidget(self.sendButton, 0, 1)
        self.chatContainer.setLayout(self.chatContainerLayout)

        self.tab2.layout.addWidget(self.chatBox)
        self.tab2.layout.addWidget(self.chatContainer)

        self.tab2.setLayout(self.tab2.layout)

        #? Üçüncü sekmeyi oluştur - Şifreleme Ayarları
        self.tab3.layout = QGridLayout(self)
        self.tab3.layout.setSpacing(1)
        
        self.setEncryptType = QWidget()
        self.setEncryptTypeLayout = QGridLayout()
        self.setEncryptTypeLabel = QLabel("Şifreleme yöntemi (diğer kullanıcıları etkilemez):")
        self.cheaserTypeButton = QRadioButton("Sezar Şifreleme")
        self.cheaserTypeButton.setChecked(True)
        self.encryptType = "cheaser"
        self.cheaserTypeButton.clicked.connect(self.cheaserSelected)
        self.rsaTypeButton = QRadioButton("RSA Şifreleme")
        self.rsaTypeButton.clicked.connect(self.RSASelected)
        self.setEncryptTypeLayout.addWidget(self.setEncryptTypeLabel, 0, 0)
        self.setEncryptTypeLayout.addWidget(self.cheaserTypeButton, 0, 1)
        self.setEncryptTypeLayout.addWidget(self.rsaTypeButton, 0, 2)
        self.setEncryptType.setLayout(self.setEncryptTypeLayout)

        self.numSliderWidget = QWidget()
        self.numSliderLayout = QGridLayout(self.numSliderWidget)
        self.numSliderTitle = QLabel("Sezar şifreleme yönteminde kullanılacak gizli rakam:")
        self.numSlider = QSlider(Qt.Horizontal)
        self.numSlider.setMinimum(1)
        self.numSlider.setMaximum(31)
        self.numSlider.setValue(1)
        self.number = 1
        self.numSlider.setTickPosition(QSlider.TicksBothSides)
        self.numSlider.setTickInterval(1)
        self.numSliderIndicator = QLabel("1 harf")
        self.numSlider.valueChanged.connect(self.valueChanged)
        self.numSliderLayout.addWidget(self.numSliderTitle, 0, 0)
        self.numSliderLayout.addWidget(self.numSlider, 1, 0)
        self.numSliderLayout.addWidget(self.numSliderIndicator, 1, 1)

        self.emptyText = QLabel("")
        self.emptyText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tab3.layout.addWidget(self.setEncryptType, 0, 0)
        self.tab3.layout.addWidget(self.numSliderWidget, 1, 0)
        self.tab3.layout.addWidget(self.emptyText, 2, 0)

        self.tab3.setLayout(self.tab3.layout)

        #? Dördüncü sekmeyi oluştur - Admin Paneli
        
        self.tab4.layout = QVBoxLayout(self)

        self.adminTitle = QLabel("Yönetici Paneli")
        self.adminTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.adminTitleFont = QFont("Droid Sans", 24, QFont.Bold)
        self.adminTitle.setAlignment(Qt.AlignCenter)
        self.adminTitle.setFont(self.adminTitleFont)

        self.spacer = QLabel("\n\n\n\n\n\n\n\n\n\nYakında yeni komutlar gelecek.")
        self.spacerFont = QFont("Droid Sans", 10, QFont.StyleItalic)
        self.spacer.setFont(self.spacerFont)
        self.spacer.setAlignment(Qt.AlignCenter)

        self.tab4.layout.addWidget(self.adminTitle)
        self.tab4.layout.addWidget(self.spacer)

        self.tab4.setLayout(self.tab4.layout)

        #? Dördüncü sekmeyi oluştur - Program Hakkında
        self.tab5.layout = QVBoxLayout(self)
        self.info = QLabel("""Şifreli Mesajlaşma Uygulaması v1.0\nGeliştiriciler:\n- Berk Akkaya\n- Ozan Alptekin""")
        self.info.setFont(QFont("Droid Sans", 15, QFont.Bold))
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tab5.layout.addWidget(self.info)
        self.tab5.setLayout(self.tab5.layout)

        #? Hazırlanan sekmeler arayüze eklenir
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        #? Yeni mesaj geldiğinde gelen sinyal changeHistory fonksiyonuna bağlanır
        self.monitor.updateText.connect(self.changeHistory)

    def pickcolor(self):
        """
        ? Rastgele bir HEX rengi üretmeyi sağlar.
        """
        r = lambda: random.randint(0, 255)
        return "#{:02x}{:02x}{:02x}".format(r(), r(), r()).upper()

    def usernameChanged(self):
        """
        ? Kullanıcı adı kutusu değiştiğinde anlık olarak giriş ekranındaki başlığı değiştiren fonksiyondur
        """
        if self.nameBox.text():
            self.loginTitle.setText("Hoş geldiniz, {}!".format(self.nameBox.text()))
        else:
            self.loginTitle.setText("Hoş geldiniz!")

    def changeHistory(self, data):
        """
        ? Gösterilmeye hazırlanan yeni mesaj bu fonksiyonla mesaj geçmişine eklenir ve kullanıcıya gösterilir.
        ? Ayrıca bu fonksiyon kullanıcıya yeni mesajı bildirmek için bir bidirim de gönderir.
        """

        if data["messageHistory"][:13] == "!clearHistory": #? Gelen mesajın mesaj temizleme komutu olup olmadığına bak.
            self.messageHistory = "<font color=\"#F12345\">Mesaj geçmişi temizlendi.</font><br><br>"
            self.chatBox.setHtml(self.messageHistory)
            self.chatBox.moveCursor(QTextCursor.End)
            print("Mesaj geçmişi temizlendi.")
        else:
            print("Geçmiş değiştiriliyor...")
            if self.isLogined and self.isReady:
                self.messageHistory += data["messageHistory"]
                self.chatBox.setHtml(self.messageHistory)
                self.chatBox.moveCursor(QTextCursor.End)
                notification.notify(title="{0} yeni mesaj gönderdi.".format(data["username"]), message="Uygulamaya gitmek için bildirime tıklayın.", app_name="Şifreli Mesajlaşma Uygulaması", app_icon="./speech-bubble.png", timeout=10)
                print("İşlem tamam!")
            else:
                print("Oturum açılmamış... TAMAM")
    
    def login(self):
        """
        ? Kullanıcının sunucuya bağlanmasını ve mesaj odasına giriş yapmasını sağlayan fonksiyondur.
        ? Ayrıca kullanıcının rengi bu kısımda rastgele seçilir.
        """
        self.color = self.pickcolor()
        self.username = self.nameBox.text()
        self.server = self.serverBox.text()
        if self.username == "" or self.server == "":
            self.connectionStatus.showMessage("Durum: Kullanıcı adı ve sunucu adresi boş bırakılamaz.")
        else:
            self.connectionStatus.showMessage("Durum: Bağlanılıyor...")
            try:
                websocket.connect(self.server)
                print("Renk:", self.color)
                websocket.emit("newUser", {"username": self.username, "color": self.color})
                self.isLogined = True
                self.messageBox.setEnabled(True)
                self.sendButton.setEnabled(True)
                self.nameBox.setEnabled(False)
                self.serverBox.setEnabled(False)
                self.loginButton.setEnabled(False)
                self.isReady = True
                self.connectionStatus.showMessage("Durum: Bağlantı kuruldu ve odaya giriş yapıldı. Şifreleme ayarlarınızı yapınız.")
                self.loginTitle.setText("{0}\nBağlandığınız sunucu adresi:\n{1}".format(self.loginTitle.text(), self.server))
            except:
                self.connectionStatus.showMessage("Durum: Sunucuya bağlanılamadı.")

    def sendMessage(self):
        """
        ? Kullanıcının yazdığı mesajın gönderilmesini sağlayan fonksiyondur.
        """
        data = {
            "username": self.username,
            "message": self.messageBox.text(),
            "encryptType": self.encryptType,
            "color": self.color
        }
        self.messageBox.setText("")

        splittedMessage = data["message"].split(" ")

        if splittedMessage[0] in self.commands:
            """
            ? Buraya kullanıcıların kullanabileceği komutlar eklenebilir.
            ? İstenirse doğru kullanımla birlikte modül kullanımı da yapılabilir.
            """

            if splittedMessage[0] == "!renkdeğiştir":
                """
                ? Kullanıcının rengini değiştirir.
                ? Boş bırakılması durumunda rastgele bir renk seçilir ve kullanıcının rengi o renk ile değiştirilir.
                ? Yanlış kullanımlarda kullanıcıyı uyaran bir yapı da mevcuttur.
                """

                splittedMessage.pop(0)

                if len(splittedMessage) == 0:
                    oldColor = self.color
                    self.color = self.pickcolor()
                    data["message"] = "Kendi rengimi <font color=\"{0}\">{0}</font> renginden <font color=\"{1}\">{1}</font> rengine değiştirdim.".format(oldColor, self.color)
                    data["color"] = self.color
                    del oldColor
                else:
                    if len(splittedMessage[0]) != 7 or splittedMessage[0][0] != "#":
                        self.messageBox.setText("UYARI: Geçersiz renk.")
                        return
                    else:
                        oldColor = self.color
                        self.color = splittedMessage[0]
                        data["message"] = "Kendi rengimi <font color=\"{0}\">{0}</font> renginden <font color=\"{1}\">{1}</font> rengine değiştirdim.".format(oldColor, self.color)
                        data["color"] = self.color
                        del oldColor

        elif splittedMessage[0] in self.adminCommands:
            """
            ? İstenirse buraya yönetici komutları eklenebilir.
            ? Şu anlık gerek duyulmadığı için boş bırakıldı.
            ? Kullanımı yukarıdaki kullanıcı komut sistemi ile aynıdır.
            """
            pass
        
        """
        ? Mesajımız buraqda şifrelenmektedir.
        ? Şu anlık Sezar Şifreleme ve RSA şifreleme yöntemleri kullanılabilir.
        ? İsteğe bağlı başka bir şifreleme yöntemi de bu kod hiyerarşisine bağlı kalınarak eklenebilir.
        
        ! ÖNEMLİ NOT: RSA yöntemindeki d anahtarının açık bir şekilde verilmesi kesinlikle güvenli değildir.
        ! Sadece öğrenme ortamında modülün nasıl çalıştığının rahat görülebilmesi için böyle bir kullanım yapılmıştır.
        ! d anahtarını bir yetkilendirme yoluyla şifreli olarak vermeniz tavsiye edilir.
        """
        if self.encryptType == "cheaser":
            data["message"] = encrypt(data["message"], self.number)
            data["number"] = self.number
        else:
            message, n, e, d = rsa.Sifrele(data["message"])
            data["message"] = message
            data["n"] = n
            data["e"] = e
            data["d"] = d
            print("""
            Şifreli Metin: {0}
            n: {1}
            e: {2}
            d: {3}
            """.format(message, n, e, d))
        """
        ? Sunucumuza mesaj bu şekilde gönderilir.
        """
        websocket.emit("newMessage", data)

    def valueChanged(self):
        """
        ? Şifreleme bölümündeki rakam ayarlayıcının değiştirilmesi durumunda belirteçteki rakamı değiştirir.
        """
        self.number = self.numSlider.value()
        self.numSliderIndicator.setText(str(self.numSlider.value()) + " harf")
    
    def cheaserSelected(self):
        """
        ? Şifreleme bölümünde Sezar Şifreleme metodunun seçilmesi durumunda gerekli düzenlemeler bu fonksiyonda yapılır.
        """
        self.encryptType = "cheaser"
        self.numSlider.setEnabled(True)
        self.number = self.numSlider.value()
    
    def RSASelected(self):
        """
        ? Şifreleme bölümünde RSA Şifreleme metodunun seçilmesi durumunda gerekli düzenlemeler bu fonksiyonda yapılır.
        """
        self.encryptType = "rsa"
        self.numSlider.setEnabled(False)

class Monitor(QObject):
    """
    ? Sunucudan yeni bir mesaj geldiğinde bunu kullanıcıya gösteilmesi için hazırlayan bir sınıf yapısı.
    """

    """
    ? PyQT altyapısında bir olayın tetiklenmesi ve gerekli aksiyonların alınması için sinyaller kullanılır.
    ? Biz burada kendimize özel mesaj geçmişinin değiştirilmesinde yardımcı olacak bir sinyal yaratıyoruz.
    
    * Not: Parantezin içindeki dict ibaresi bizim sinyal içinde göndereceğimiz verinin sözlük veri tipinde olacağını belirtir.
    """
    updateText = pyqtSignal(dict)
    
    def handle(self, data):
        """
        ? Mesaj geldiğinde ilk aşama olarak mesajın şifresi çözülür ve veriden kullanıcı adı verisi alınır.
        ? Alınan bu veriler sinyalle arayüze gönderilmek üzere update_list fonksiyonuna sokulur.
        """
        print("İstek geldi.")
        print("İşlem başlıyor...")
        
        decryptedText = rsa.SifreCoz(data["messageHistory"], data["n"], data["e"], data["d"])
        username = data["username"]

        self.update_list(decryptedText, username)

    def update_list(self, history, username):
        """
        ? PyQT altyapısında sinyalin tetiklenebilmesi için bir tetikleyici Thread yani İşlem oluşturmamız gerekir.

        ? Thread'imize bize gelen mesaj ve kullanıcı adını ve sinyal tetikleme fonksiyonunu belirtiriz.
        """
        print("update_list")
        t_monitor = Thread(self.updateHistory, parent=self, messageHistory=history, username=username)
        t_monitor.daemon = True
        t_monitor.setObjectName("monitor")
        t_monitor.start()
    
    def updateHistory(self, data):
        """
        ? Bu fonksiyon sinyalin içine gerekli verileri koyar ve sinyali tetikler.
        """
        print("updateHistory")
        self.updateText.emit(data)

class Thread(QThread):
    """
    ? Sinyalin tetiklenmesini sağlayan tetikleyici sınıftır.
    """
    def __init__(self, fn, parent=None, *args, **kwargs):
        """
        ? Sınıfımızı bu fonksiyon ile sinyali tetiklemeye hazırlarız.
        """
        print("Thread_init")
        super(Thread, self).__init__(parent)
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
    
    def run(self):
        """
        ? Sinyalimizin tetiklendiği kısımdır.
        ? Sinyalimize gerekli veriler yerleştirilir ve tetikleyici fonksiyon çalıştırılır.
        """
        print("Thread_run")
        self._fn({
            "messageHistory": self._kwargs["messageHistory"],
            "username": self._kwargs["username"]
            })

#? Uygulama yapılandırılır.
app = QApplication(sys.argv)

#? Yeni mesaj sırasında gerekli eylemi uygulayacak olan sınıf yapılandırılır.
monitor = Monitor()

#? Arayüz yapılandırılır.
ex = App(monitor=monitor)

@websocket.on("messageHistoryChanged")
def watch(data):
    """
    ? Sunucudan yeni bir mesaj geldiğinde gerekli işlemleri başlatacak fonksiyonu çağırır.
    """
    monitor.handle(data=data)

#? Uygulama çalıştırılır.
sys.exit(app.exec_())