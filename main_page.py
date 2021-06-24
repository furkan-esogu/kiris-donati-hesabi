from PyQt5.QtWidgets import*
from main_page_qt import Ui_MainWindow
from beam_mr import BeamMr
from beam_rf import BeamRf
import os


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.beam_mr = BeamMr()
        self.beam_rf = BeamRf()

        self.ui.pushButton_1.clicked.connect(self.open_beammr)
        self.ui.pushButton_2.clicked.connect(self.open_beamrf)
        self.ui.pushButton_5.clicked.connect(self.exit)
        self.ui.pushButton_3.clicked.connect(self.benioku)
        self.ui.pushButton_4.clicked.connect(self.yapim)

    def open_beammr(self):

        self.beam_mr.show()
    
    def open_beamrf(self):

        self.beam_rf.show()
    
    def exit(self):

        qApp.quit()

    def benioku(self):

        os.startfile('benioku.pdf')
    
    def yapim(self):

        os.startfile("yapim.pdf")



