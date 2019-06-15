"""
Mesajlaşma uygulaması
Hazırlayanlar: Berk Akkaya ve Ozan Alptekin

=================== YAPILACAKLAR LİSTESİ =========================
Şu anlık bir şey yok.
"""

import socketio
import sys
from time import sleep
from src.cheaserDecrypt import decrypt
from src.cheaserEncrypt import encrypt
import src.rsa as rsa
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from plyer import notification
import random

websocket = socketio.Client()

class App(QMainWindow):
    def __init__(self, monitor):
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

        self.show()

class Widgets(QWidget):

    def __init__(self, parent, monitor, statusBar):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.monitor = monitor

        self.connectionStatus = statusBar

        self.isLogined = False
        self.isReady = False

        #Renkleri tanımla
        #self.colors = {
        #    "red": "#ff0000",
        #    "blue": "#00a1ff",
        #    "orange": "#ff5000",
        #    "purple": "#6e00ff",
        #    "green": "#3bff00"
        #}

        self.colorkeys = ["red", "blue", "orange", "purple", "green"]
        
        #Sekme ekranını hazırla
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(450, 700)
        
        #Sekmeleri programa tanımla
        self.tabs.addTab(self.tab1, "Giriş Yap")
        self.tabs.addTab(self.tab2, "Sohbet")
        self.tabs.addTab(self.tab3, "Şifreleme Ayarları")
        self.tabs.addTab(self.tab4, "Program Hakkında")
        
        #Birinci Sekmeyi oluştur. - Giriş Yap
        self.tab1.layout = QVBoxLayout(self)

        self.inputContainer = QWidget()
        self.inputContainerLayout = QGridLayout()
        self.tab1.layout.setSpacing(1)
        
        self.loginTitle = QLabel("Hoş geldiniz!")
        self.loginTitle.setObjectName("LoginTitle")
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

        #İkinci sekmeyi oluştur - Sohbet
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

        #Üçüncü sekmeyi oluştur - Şifreleme Ayarları
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

        #Dördüncü sekmeyi oluştur - Program Hakkında
        self.tab4.layout = QVBoxLayout(self)
        self.info = QLabel("""
        Sezar ve RSA Şifreleyici v1.0
        Geliştiriciler:
        - Berk Akkaya
        - Ozan Alptekin
        """)

        self.tab4.layout.addWidget(self.info)
        self.tab4.setLayout(self.tab4.layout)

        #Widget'e yeni sekmeler ekle
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.monitor.updateText.connect(self.changeHistory)

    def usernameChanged(self):
        if self.nameBox.text():
            self.loginTitle.setText("Hoş geldiniz, {}!".format(self.nameBox.text()))
        else:
            self.loginTitle.setText("Hoş geldiniz!")

    def changeHistory(self, data):
        print("Geçmiş değiştiriliyor...")
        if self.isLogined and self.isReady:
            self.chatBox.setText(data)
            print("İşlem tamam!")
        else:
            print("Oturum açılmamış... TAMAM")
        self.chatBox.moveCursor(QTextCursor.End)
        notification.notify(title="Yeni mesajınız var.", message="<b>Uygulamaya bakmayı unutmayın.</b>", app_name="Şifreli Mesajlaşma Uygulaması", timeout=10)
    
    def login(self):
        self.username = self.nameBox.text()
        self.server = self.serverBox.text()
        if self.username == "" or self.server == "":
            self.connectionStatus.showMessage("Durum: Kullanıcı adı ve sunucu adresi boş bırakılamaz.")
        else:
            self.connectionStatus.showMessage("Durum: Bağlanılıyor...")
            try:
                websocket.connect(self.server)
                websocket.emit("newUser", {"username": self.username})
                self.isLogined = True
                #self.color = self.colors[random.choice(self.colorkeys)]
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
        data = {
            "username": self.username,
            "message": self.messageBox.text()
            #"encryptType": self.encryptType
            #"color": self.color
        }
        self.messageBox.setText("")

        #if self.encryptType == "cheaser":
        #    data["message"] = encrypt(self.messageBox.toPlainText(), self.number)
        #    data["number"] = self.number
        #else:
        #    message, n, e, d = rsa.Sifrele(self.messageBox.toPlainText())
        #    data["message"] = message
        #    data["n"] = n
        #    data["e"] = e
        #    data["d"] = d
        #
        websocket.emit("newMessage", data)

    def valueChanged(self):
        self.number = self.numSlider.value()
        self.numSliderIndicator.setText(str(self.numSlider.value()) + " harf")
    
    def cheaserSelected(self):
        self.encryptType = "cheaser"
        self.numSlider.setEnabled(True)
        self.number = self.numSlider.value()
    
    def RSASelected(self):
        self.encryptType = "rsa"
        self.numSlider.setEnabled(False)

class Monitor(QObject):

    updateText = pyqtSignal(str)
    
    def handle(self, data):
        print("İstek geldi.")
        print("İşlem başlıyor...")
        strHistory = ""
        isFirst = True
        for i in data["messageHistory"]:
            if isFirst:
                strHistory += i
                isFirst = False
            else:
                strHistory += "\n{}".format(i)
        self.update_list(strHistory)

    def update_list(self, history):
        print("update_list")
        t_monitor = Thread(self.updateHistory, parent=self, messageHistory=history)
        t_monitor.daemon = True
        t_monitor.setObjectName("monitor")
        t_monitor.start()
    
    def updateHistory(self, history):
        print("updateHistory")
        self.updateText.emit(history)

class Thread(QThread):
    def __init__(self, fn, parent=None, *args, **kwargs):
        print("Thread_init")
        super(Thread, self).__init__(parent)
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
    
    def run(self):
        print("Thread_run")
        self._fn(self._kwargs["messageHistory"])

app = QApplication(sys.argv)

with open("./css/stylesheet.css", "r+") as css:
    app.setStyleSheet(css.read())
    css.close()

monitor = Monitor()

ex = App(monitor=monitor)

@websocket.on("messageHistoryChanged")
def watch(data):
    monitor.handle(data = data)

sys.exit(app.exec_())