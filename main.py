from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtWebEngineWidgets as qtweb

from sys import argv


class searchBar(qtw.QLineEdit):

    def __init__(self):
        super().__init__()
        self.editing = False
    
    def focusOutEvent(self, event):
        self.editing = False
        super().focusOutEvent(event)
    
    def mousePressEvent(self, event):
        if self.editing or self.selectionLength == 0:
            super().mousePressEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        self.editing = True
        super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        if not self.hasSelectedText() and not self.editing:
            self.selectAll()
        elif self.selectionLength() == len(self.text()) and not self.editing:
            self.editing = True
            super().mousePressEvent(event)
        else:
            super().mouseReleaseEvent(event)


class Window(qtw.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.browser = qtweb.QWebEngineView()
        self.browser.setUrl(qtc.QUrl("https://google.co.uk"))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        # Navbar
        navbar = qtw.QToolBar()
        navbar.setMovable(False)
        self.addToolBar(navbar)
        # Back button
        backButton = qtw.QAction("Back", self)
        backButton.triggered.connect(self.browser.back)
        backButton.setIcon(qtg.QIcon("icons/left_arrow.svg")) # Icon by Raj Dev on https://freeicons.io
        navbar.addAction(backButton)
        # Next button
        nextButton = qtw.QAction("Next", self)
        nextButton.triggered.connect(self.browser.forward)
        nextButton.setIcon(qtg.QIcon("icons/right_arrow.svg")) # Icon by Raj Dev on https://freeicons.io     
        navbar.addAction(nextButton)
        # Refresh button
        refreshButton = qtw.QAction("Refresh", self)
        refreshButton.triggered.connect(self.browser.reload) # Icon by Muhammad Haq on https://freeicons.io
        refreshButton.setIcon(qtg.QIcon("icons/refresh.svg"))
        navbar.addAction(refreshButton)
        # Search bar
        self.searchBar = searchBar()
        self.searchBar.setTextMargins(10, 0, 0, 0)
        self.searchBar.setPlaceholderText("Type in a url to search")
        self.searchBar.returnPressed.connect(self.loadUrl)
        navbar.addWidget(self.searchBar)
        self.browser.urlChanged.connect(self.changeUrl)
    
    def loadUrl(self):
        url = self.searchBar.text()
        if "." in url:
            if len(url) > 8:
                if url[:8] != "https://":
                    url = "https://" + url
            else:
                url = "https://" + url
        else:
            url = f"https://www.google.com/search?q={'+'.join(url.split(' '))}"
        self.browser.setUrl(qtc.QUrl(url))
    
    def changeUrl(self, url):
        self.searchBar.setText(url.toString())
        self.searchBar.home(False)


if __name__ == '__main__':
    app = qtw.QApplication(argv)
    app.setApplicationName("Horse Net")
    app.setWindowIcon(qtg.QIcon("icons/horseNetIcon.png")) # https://www.vecteezy.com/free-vector/horse-logo Horse Logo Vectors by Vecteezy
    qtg.QFontDatabase.addApplicationFont("fonts/roboto-light.ttf")
    with open("style.qss", "r") as style:
        styleSheet = style.read()
    app.setStyleSheet(styleSheet)
    window = Window()
    window.show()
    app.exec()
