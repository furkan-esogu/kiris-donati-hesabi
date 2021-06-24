from PyQt5.QtWidgets import*
from main_page import MainPage


app = QApplication([])
pencere = MainPage()
pencere.show()
app.exec_()