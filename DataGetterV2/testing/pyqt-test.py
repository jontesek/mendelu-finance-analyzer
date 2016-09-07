import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 


class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()

url = 'http://finance.yahoo.com/quote/AMD?p=AMD'
#This does the magic.Loads everything
r = Render(url)
#result is a QString.
result = r.frame.toHtml()

formatted_result = str(result.toAscii())

with open("../test_data/yahoo_data.html", "w") as text_file:
    text_file.write(formatted_result)
