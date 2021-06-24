from PyQt5.QtWidgets import*
from beam_mr_qt import*
from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator,QDoubleValidator

import numpy as np
import pandas as pd
import sys

class BeamMr(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MrBeam()
        self.ui.setupUi(self)

        df_donati = pd.read_excel("donati_alanlari.xlsx",header=0)
        df_donati = df_donati.set_index("cap")

        df_beton = pd.read_excel("BetonSiniflari.xlsx")
        df_beton = df_beton.set_index("BetonSinifi")

        df_celik = pd.read_excel("CelikSiniflari.xlsx")
        df_celik = df_celik.set_index("CelikSinifi")

        self.setWindowTitle("Tek Donatılı,Denge Altı Donatılmış Dikdörtgen Kesitli Kirişin Taşıma Gücü")

        self.ui.label_8.setText("Donatı Alanı: ")
        self.ui.label_9.setText("Donatı Oranı: ")
        self.ui.label_10.setText("HESAPLANIYOR...")
        self.ui.label_11.setText("Basınç Bloğu Derinliği(a): ")
        self.ui.label_12.setText("Tarafsız Eksen Derinliği(c): ")
        self.ui.label_13.setText("Moment Taşıma Gücü(Mr): ")
        self.ui.label_14.setText("HESAPLANIYOR...")

        self.ui.comboBox.addItem("1",1)
        self.ui.comboBox.addItem("2",2)
        self.ui.comboBox.addItem("3",3)
        self.ui.comboBox.addItem("4",4)
        self.ui.comboBox.addItem("5",5)
        self.ui.comboBox.addItem("6",6)
        self.ui.comboBox.addItem("7",7)
        self.ui.comboBox.addItem("8",8)
        self.ui.comboBox.addItem("9",9)
        self.ui.comboBox.addItem("10",10)

        self.ui.comboBox_3.addItem("14",14)
        self.ui.comboBox_3.addItem("16",16)
        self.ui.comboBox_3.addItem("18",18)
        self.ui.comboBox_3.addItem("20",20)
        self.ui.comboBox_3.addItem("22",22)
        self.ui.comboBox_3.addItem("24",24)
        self.ui.comboBox_3.addItem("26",26)
        self.ui.comboBox_3.addItem("28",28)
        self.ui.comboBox_3.addItem("30",30)

        self.ui.comboBox_1.addItem("C25/30",df_beton.loc["C25/30"])
        self.ui.comboBox_1.addItem("C30/37",df_beton.loc["C30/37"])
        self.ui.comboBox_1.addItem("C35/45",df_beton.loc["C35/45"])
        self.ui.comboBox_1.addItem("C40/50",df_beton.loc["C40/50"])
        self.ui.comboBox_1.addItem("C45/55",df_beton.loc["C45/55"])
        self.ui.comboBox_1.addItem("C50/60",df_beton.loc["C50/60"])

        self.ui.comboBox_2.addItem("B420C",df_celik.loc["B420C"])
        self.ui.comboBox_2.addItem("B500C",df_celik.loc["B500C"])

        self.ui.lineEdit_1.setValidator(QIntValidator(0,10000,self))
        self.ui.lineEdit_2.setValidator(QIntValidator(0,10000,self))
        self.ui.lineEdit_3.setValidator(QIntValidator(0,10000,self))
        self.ui.lineEdit_4.setValidator(QDoubleValidator(0,10000,2,self))
        
        self.ui.pushButton.clicked.connect(self.kontrol)
        self.ui.pushButton_clear.clicked.connect(self.clear)      


    def kontrol(self):
        
        liste1 = self.ui.comboBox_1.currentData()
        liste2 = self.ui.comboBox_2.currentData()

        donatı_sayisi = self.ui.comboBox.currentData()
        donati_capi = self.ui.comboBox_3.currentData()
        
        da = round((int(donatı_sayisi) * (int(donati_capi) ** 2) * 3.1415926535 / 4),0)

        self.ui.label_5.setText(str(da) +" "+ "mm2")

        if self.ui.lineEdit_1.text() == "":
            h = 500
            self.ui.label_20.setText("Tüm Verileri Giriniz...")
        elif int(self.ui.lineEdit_1.text()) < 300:
            h = 300
            self.ui.label_20.setText("Kiriş Yüksekliği 300 mm'den Az Olamaz")
        else:
            h = self.ui.lineEdit_1.text()
        
        if self.ui.lineEdit_2.text() == "":
            bw = 250
            self.ui.label_20.setText("Tüm Verileri Giriniz...")
        elif int(self.ui.lineEdit_2.text()) < 250:
            bw = 250
            self.ui.label_20.setText("Kiriş Genişliği 250 mm'den Az Olamaz")
        else:
            bw = self.ui.lineEdit_2.text()
        
        if self.ui.lineEdit_3.text() == "":
            d = 25
            self.ui.label_20.setText("Tüm Verileri Giriniz...")
        elif int(self.ui.lineEdit_3.text()) < 25: 
            d = 25 
            self.ui.label_20.setText("Pas Payı 25 mm'den Az Olamaz")
        else:
            d = self.ui.lineEdit_3.text()
        
        do = round((da / (int(bw) * (int(h) - int(d)))),5)

        if self.ui.label_20.text() == "":
            self.ui.label_15.setText(str(do))
        else:
            self.ui.label_15.setText("********************")

        if (do <= 0.85 * float(liste1["roB"])) and (do <= 0.02) and do >= (0.8 * float(liste1["Fctd"]) / float(liste2["Fyk"])):
            self.ui.label_10.setText("***Denge Altı Donatılmış***")
            self.islem_a()
        
        else:
            self.ui.label_10.setText("Denge Üstü Donatılmış.Yönetmeliklere Aykırı Donatı Seçimi")
            self.ui.label_16.setText("-----")
            self.ui.label_17.setText("-----")
            self.ui.label_18.setText("-----")
            self.ui.label_14.setText("-----")


    def islem_a(self):
        
        donatı_sayisi = self.ui.comboBox.currentData()
        donati_capi = self.ui.comboBox_3.currentData()
        
        da = round((int(donatı_sayisi) * (int(donati_capi) ** 2) * 3.1415926535 / 4),0)

        liste1 = self.ui.comboBox_1.currentData()
        liste2 = self.ui.comboBox_2.currentData()
        
        h = self.ui.lineEdit_1.text()
        bw = self.ui.lineEdit_2.text()
        d = self.ui.lineEdit_3.text()

        a = round((da / float(liste1["K3"]) / int(bw)) * (float(liste2["Fyd"]) / float(liste1["Fcd"])),2)

        self.ui.label_16.setText(str(a) + " " + "mm")

        c = round(a / float(liste1["K1"]),2)

        self.ui.label_17.setText(str(c) + " " + "mm") 

        hh = int(h) - int(d)

        fyd = float(liste2["Fyd"])
        
        mr = round(da * fyd * (hh - a / 2) * (10 ** -6),2)
        
        self.ui.label_18.setText(str(mr) + " " + "kN.m")
       
        if self.ui.lineEdit_4.text() == "":
            md = 100
            self.ui.label_20.setText("Tüm Verileri Giriniz...")
        else:
            md = self.ui.lineEdit_4.text()

        md = float(md)

        if md <= mr:
            self.ui.label_14.setText("Kiriş Verilen Yükleri Güvenle Taşıyabilir")

        else: 
            self.ui.label_14.setText("Kiriş Verilen Yükü Taşıyamaz")
    
    def clear(self):

        self.ui.lineEdit_1.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.label_5.clear()
        self.ui.label_15.clear()
        self.ui.label_16.clear()
        self.ui.label_17.clear()
        self.ui.label_18.clear()

                

        
        



