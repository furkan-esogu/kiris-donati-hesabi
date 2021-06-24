from PyQt5.QtWidgets import*
from beam_rf_qt import*
from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator,QDoubleValidator

import numpy as np
import pandas as pd
import sys


class BeamRf(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_FrBeam()
        self.ui.setupUi(self)

        df_donati = pd.read_excel("donati_alanlari.xlsx",header=0)
        df_donati = df_donati.set_index("cap")

        df_beton = pd.read_excel("BetonSiniflari.xlsx")
        df_beton = df_beton.set_index("BetonSinifi")

        df_celik = pd.read_excel("CelikSiniflari.xlsx")
        df_celik = df_celik.set_index("CelikSinifi")

        df_cubuk = pd.read_excel("CubukSayisi.xlsx",header=0)
        df_cubuk = df_cubuk.set_index("bw")

        self.ui.label_text.setText("HESAPLANIYOR...")

        self.ui.comboBox_bs.addItem("C25/30",df_beton.loc["C25/30"])
        self.ui.comboBox_bs.addItem("C30/37",df_beton.loc["C30/37"])
        self.ui.comboBox_bs.addItem("C35/45",df_beton.loc["C35/45"])
        self.ui.comboBox_bs.addItem("C40/50",df_beton.loc["C40/50"])
        self.ui.comboBox_bs.addItem("C45/55",df_beton.loc["C45/55"])
        self.ui.comboBox_bs.addItem("C50/60",df_beton.loc["C50/60"])

        self.ui.comboBox_cs.addItem("B420C",df_celik.loc["B420C"])
        self.ui.comboBox_cs.addItem("B500C",df_celik.loc["B500C"])

        self.ui.lineEdit_h.setValidator(QIntValidator(0,10000,self))
        self.ui.lineEdit_bw.setValidator(QIntValidator(0,10000,self))
        self.ui.lineEdit_d.setValidator(QIntValidator(0,10000,self))
        self.ui.lineEdit_md.setValidator(QDoubleValidator(0,10000,2,self))

        self.ui.pushButton_hesapla.clicked.connect(self.hesap)
        self.ui.pushButton_clear.clicked.connect(self.clear)


    def hesap(self):

        beton_sinifi = self.ui.comboBox_bs.currentData()
        celik_sinifi = self.ui.comboBox_cs.currentData()
        
        if self.ui.lineEdit_h.text() == "":
            h = 500
            self.ui.label_error.setText("Tüm Verileri Giriniz...")
        elif int(self.ui.lineEdit_h.text()) < 300:
            h = 300
            self.ui.label_error.setText("Kiriş Yüksekliği 300 mm'den Az Olamaz")
        else:
            h = int(self.ui.lineEdit_h.text())
        
        if self.ui.lineEdit_bw.text() == "":
            bw = 250
            self.ui.label_error.setText("Tüm Verileri Giriniz...")
        else:
            bw = int(self.ui.lineEdit_bw.text())

        if self.ui.lineEdit_d.text() == "":
            dd = 40
            self.ui.label_error.setText("Tüm Verileri Giriniz...")
        elif int(self.ui.lineEdit_d.text()) <= 25:
            self.ui.label_error.setText("Pas Payı 25 mm'den Az Olamaz")
            dd = 25
        else:
            dd = int(self.ui.lineEdit_d.text())
        
        if self.ui.lineEdit_md.text() == "":
            md = 138.8
            self.ui.label_error.setText("Tüm Verileri Giriniz...")
        else:
            md = float(self.ui.lineEdit_md.text())

        d = h - dd
        
        fck = float(beton_sinifi["Fck"])
        fctk = float(beton_sinifi["Fctk"])
        fctd = float(beton_sinifi["Fctd"])
        fcd = float(beton_sinifi["Fcd"])
        roB = float(beton_sinifi["roB"])
        k1 = float(beton_sinifi["K1"])
        k3 = float(beton_sinifi["K3"])

        fyk = float(celik_sinifi["Fyk"])
        fyd = float(celik_sinifi["Fyd"])

        
        k = (2 * md * (10 ** 6)) / (k3 * fcd * bw * d * d)

        a = d * (1 - ((1 - k) ** 0.5))

        if self.ui.label_error.text() == "":
            self.ui.label_a_2.setText(str(round(a,2)) + " mm")
        else:
            self.ui.label_a_2.setText("********************")

        aS = k3 * fcd * a * bw / fyd
        
        if self.ui.label_error.text() == "":
            self.ui.label_as_2.setText(str(round(aS,0)) + " mm2")
        else:
            self.ui.label_as_2.setText("********************")

        df_donati = pd.read_excel("donati_alanlari.xlsx",header=0)
        df_donati = df_donati.set_index("cap")

        df_bw200 = pd.read_excel("donati_alanlari.xlsx",sheet_name="bw200",header=0)
        df_bw200 = df_bw200.set_index("cap")
    
        df_bw250 = pd.read_excel("donati_alanlari.xlsx",sheet_name="bw250",header=0)
        df_bw250 = df_bw250.set_index("cap")

        df_bw300 = pd.read_excel("donati_alanlari.xlsx",sheet_name="bw300",header=0)
        df_bw300 = df_bw300.set_index("cap")

        df_bw350 = pd.read_excel("donati_alanlari.xlsx",sheet_name="bw350",header=0)
        df_bw350 = df_bw350.set_index("cap")

        df_bw400 = pd.read_excel("donati_alanlari.xlsx",sheet_name="bw400",header=0)
        df_bw400 = df_bw400.set_index("cap")

        df_bw450 = pd.read_excel("donati_alanlari.xlsx",sheet_name="bw450",header=0)
        df_bw450 = df_bw450.set_index("cap")

        df_bw500 = pd.read_excel("donati_alanlari.xlsx",sheet_name="bw500",header=0)
        df_bw500 = df_bw500.set_index("cap")

        df_bw550 = pd.read_excel("donati_alanlari.xlsx",sheet_name="bw550",header=0)
        df_bw550 = df_bw550.set_index("cap")

        df_bw600 = pd.read_excel("donati_alanlari.xlsx",sheet_name="bw600",header=0)
        df_bw600 = df_bw600.set_index("cap")

        if bw < 250:

            self.ui.label_rf_2.setText("Kiriş Genişliği 250 mm'den Az Olamaz")
            self.ui.label_error.setText("Kiriş Genişliği 250 mm'den Az Olamaz")

            df_bw200_values = df_bw200.values
            df_bw200_tuples = np.unravel_index(np.argmin(np.abs(df_bw200_values-aS),axis=None),df_bw200_values.shape)

            cap = int(df_bw200_tuples[0])
            sayi = int(df_bw200_tuples[1])

            cubuk_sayisi = int(df_bw200.columns[int(df_bw200_tuples[1])])
            cubuk_capi = int(df_bw200.index[int(df_bw200_tuples[0])])

            donati_alani = round(df_bw200.iloc[cap,sayi])

        elif bw >= 250 and bw < 300 :
            
            if self.ui.label_error.text() == "": 

                df_bw250_values = df_bw250.values
                df_bw250_tuples = np.unravel_index(np.argmin(np.abs(df_bw250_values-aS),axis=None),df_bw250_values.shape)

                cap = int(df_bw250_tuples[0])
                sayi = int(df_bw250_tuples[1])

                cubuk_sayisi = int(df_bw250.columns[int(df_bw250_tuples[1])])
                cubuk_capi = int(df_bw250.index[int(df_bw250_tuples[0])])

                donati_alani = round(df_bw250.iloc[cap,sayi])

                self.ui.label_rf_2.setText(str(cubuk_sayisi)+ " Φ " + str(cubuk_capi) +" "+"("+ str(donati_alani) +" mm2)")

            else:
                self.ui.label_rf_2.setText("********************")

        elif bw >= 300 and bw < 350:
            
            if self.ui.label_error.text() == "":

                df_bw300_values = df_bw300.values
                df_bw300_tuples = np.unravel_index(np.argmin(np.abs(df_bw300_values-aS),axis=None),df_bw300_values.shape)

                cap = int(df_bw300_tuples[0])
                sayi = int(df_bw300_tuples[1])

                cubuk_sayisi = int(df_bw300.columns[int(df_bw300_tuples[1])])
                cubuk_capi = int(df_bw300.index[int(df_bw300_tuples[0])])

                donati_alani = round(df_bw300.iloc[cap,sayi])

                self.ui.label_rf_2.setText(str(cubuk_sayisi)+ " Φ " + str(cubuk_capi) +" "+"("+ str(donati_alani) +" mm2)")

            else:
                self.ui.label_rf_2.setText("********************")
                
        elif bw >= 350 and bw < 400:

            if self.ui.label_error.text() == "":

                df_bw350_values = df_bw350.values
                df_bw350_tuples = np.unravel_index(np.argmin(np.abs(df_bw350_values-aS),axis=None),df_bw350_values.shape)

                cap = int(df_bw350_tuples[0])
                sayi = int(df_bw350_tuples[1])

                cubuk_sayisi = int(df_bw350.columns[int(df_bw350_tuples[1])])
                cubuk_capi = int(df_bw350.index[int(df_bw350_tuples[0])])

                donati_alani = round(df_bw350.iloc[cap,sayi])

                self.ui.label_rf_2.setText(str(cubuk_sayisi)+ " Φ " + str(cubuk_capi) +" "+"("+ str(donati_alani) +" mm2)")
           
            else:
                self.ui.label_rf_2.setText("********************")

        elif bw >= 400 and bw < 450:
            
            if self.ui.label_error.text() == "":

                df_bw400_values = df_bw400.values
                df_bw400_tuples = np.unravel_index(np.argmin(np.abs(df_bw400_values-aS),axis=None),df_bw400_values.shape)

                cap = int(df_bw400_tuples[0])
                sayi = int(df_bw400_tuples[1])

                cubuk_sayisi = int(df_bw400.columns[int(df_bw400_tuples[1])])
                cubuk_capi = int(df_bw400.index[int(df_bw400_tuples[0])])

                donati_alani = round(df_bw400.iloc[cap,sayi])

                self.ui.label_rf_2.setText(str(cubuk_sayisi)+ " Φ " + str(cubuk_capi) +" "+"("+ str(donati_alani) +" mm2)")
            else:
                self.ui.label_rf_2.setText("********************")

        elif bw >= 450 and bw < 500:
            
            if self.ui.label_error.text() == "":

                df_bw450_values = df_bw450.values
                df_bw450_tuples = np.unravel_index(np.argmin(np.abs(df_bw450_values-aS),axis=None),df_bw450_values.shape)

                cap = int(df_bw450_tuples[0])
                sayi = int(df_bw450_tuples[1])

                cubuk_sayisi = int(df_bw450.columns[int(df_bw450_tuples[1])])
                cubuk_capi = int(df_bw450.index[int(df_bw450_tuples[0])])

                donati_alani = round(df_bw450.iloc[cap,sayi])

                self.ui.label_rf_2.setText(str(cubuk_sayisi)+ " Φ " + str(cubuk_capi) +" "+"("+ str(donati_alani) +" mm2)")
            else:
                self.ui.label_rf_2.setText("********************")

        elif bw >= 500 and bw < 550:
            
            if self.ui.label_error.text() == "":

                df_bw500_values = df_bw500.values
                df_bw500_tuples = np.unravel_index(np.argmin(np.abs(df_bw500_values-aS),axis=None),df_bw500_values.shape)

                cap = int(df_bw500_tuples[0])
                sayi = int(df_bw500_tuples[1])

                cubuk_sayisi = int(df_bw500.columns[int(df_bw500_tuples[1])])
                cubuk_capi = int(df_bw500.index[int(df_bw500_tuples[0])])

                donati_alani = round(df_bw500.iloc[cap,sayi])

                self.ui.label_rf_2.setText(str(cubuk_sayisi)+ " Φ " + str(cubuk_capi) +" "+"("+ str(donati_alani) +" mm2)")
            else:
                self.ui.label_rf_2.setText("********************")

        elif bw >= 550 and bw < 600:
            
            if self.ui.label_error.text() == "":

                df_bw550_values = df_bw550.values
                df_bw550_tuples = np.unravel_index(np.argmin(np.abs(df_bw550_values-aS),axis=None),df_bw550_values.shape)

                cap = int(df_bw550_tuples[0])
                sayi = int(df_bw550_tuples[1])

                cubuk_sayisi = int(df_bw550.columns[int(df_bw550_tuples[1])])
                cubuk_capi = int(df_bw550.index[int(df_bw550_tuples[0])])

                donati_alani = round(df_bw550.iloc[cap,sayi])

                self.ui.label_rf_2.setText(str(cubuk_sayisi)+ " Φ " + str(cubuk_capi) +" "+"("+ str(donati_alani) +" mm2)")
            else:
                self.ui.label_rf_2.setText("********************")
        elif bw == 600:

            if self.ui.label_error.text() == "":

                df_bw600_values = df_bw600.values
                df_bw600_tuples = np.unravel_index(np.argmin(np.abs(df_bw600_values-aS),axis=None),df_bw600_values.shape)

                cap = int(df_bw600_tuples[0])
                sayi = int(df_bw600_tuples[1])

                cubuk_sayisi = int(df_bw600.columns[int(df_bw600_tuples[1])])
                cubuk_capi = int(df_bw600.index[int(df_bw600_tuples[0])])

                donati_alani = round(df_bw600.iloc[cap,sayi])

                self.ui.label_rf_2.setText(str(cubuk_sayisi)+ " Φ " + str(cubuk_capi) +" "+"("+ str(donati_alani) +" mm2)")

        elif bw > 600:
            
            self.ui.label_rf_2.setText("Tanımsız Kiriş Genişliği")
            self.ui.label_error.setText("Tanımsız Kiriş Genişliği")
        
        if self.ui.label_error.text() == "":
            ro = round((donati_alani / (bw * d)),5)
            self.ui.label_do_2.setText(str(ro))
        else:
            self.ui.label_do_2.setText("********************")
        
        if self.ui.label_error.text() == "":
            self.ui.label_text.setText("Kiriş Değerleri Yönetmeliklere Uygundur...")
        else:
            self.ui.label_do_2.setText("********************")



    def clear(self):

        self.ui.lineEdit_h.clear()
        self.ui.lineEdit_bw.clear()
        self.ui.lineEdit_d.clear()
        self.ui.lineEdit_md.clear()
        self.ui.label_a_2.clear()
        self.ui.label_as_2.clear()
        self.ui.label_rf_2.clear()
        self.ui.label_error.clear()
        self.ui.label_rf_2.clear()
        
            
            

        



        

















