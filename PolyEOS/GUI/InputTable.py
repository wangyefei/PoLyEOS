# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 17:29:45 2018

@author: wangf
"""

import numpy as np
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    PYQT = 4
except:
    from PyQt5.QtWidgets import  QWidget,QVBoxLayout,QTabWidget,QTableWidgetItem
    from PyQt5.QtCore import Qt

try:
    from CustomWidget.Table import TableWidgetCustom
except:
    from .CustomWidget.Table import TableWidgetCustom   
    
class InputTable(TableWidgetCustom):
    """
    This class use for input Depth, Pressure and Temperature and reflect output
    Vp,Vs and Density
    """    
    def __init__(self,parent=None,test=False):
        super(InputTable, self).__init__(parent)
        self.createTable(row=20,col=6)
        self.setHorizontalHeaderLabels(['D (Km)','P (GPa)','T (K)','Vp (km/s)','Vs (km/s','Rho (kg/m³)'])
        for col in range(3,6):
            for row in range(20):
                item = QTableWidgetItem(' ')
                item.setFlags(Qt.ItemIsEnabled)
                self.setItem(row,col, item)
        self.setGeometry(100,100,400,800)
        if test:
            self.setItem(0,0,QTableWidgetItem('110'))
            self.setItem(0,1,QTableWidgetItem('2.0'))
            self.setItem(0,2,QTableWidgetItem('1600'))

            self.setItem(1,0,QTableWidgetItem('410'))
            self.setItem(1,1,QTableWidgetItem('11.0'))
            self.setItem(1,2,QTableWidgetItem('1700'))
            
            self.setItem(2,0,QTableWidgetItem('660'))
            self.setItem(2,1,QTableWidgetItem('17.0'))
            self.setItem(2,2,QTableWidgetItem('1800'))
            
    def New(self):
        rowcount = self.rowCount()
        for row in range(rowcount):
             for col in range(6):
                 self.setItem(row,col,QTableWidgetItem(' '))
        
        
        
    def GetData(self):
        rowcount = self.rowCount()
        self.Depth=np.zeros(rowcount)  -1
        self.Pressure=np.zeros(rowcount) -1
        self.Temperature=np.zeros(rowcount) -1
        for row in range(rowcount):
            if not isinstance((self.item(row,0)),type(None)): 
                if  self.item(row, 0).text() !=  ' ':
                    self.Depth[row] = float(self.item(row, 0).text())
            else:
                pass
            if not isinstance((self.item(row,1)),type(None)): 
                if  self.item(row, 0).text() !=  ' ':
                    self.Temperature[row] = float(self.item(row, 1).text())   
            else:
                pass 
               
            if not isinstance((self.item(row,2)),type(None)): 
                if  self.item(row, 0).text() !=  ' ':
                    self.Pressure[row] = float(self.item(row, 2).text())
            else:
                pass 
        D = [];P=[];T=[]
        for i in range(rowcount):
            if self.Depth[i] != -1 and self.Pressure[i] != -1 and self.Temperature[i] != -1:
                D.append(self.Depth[i])
                P.append(self.Pressure[i])
                T.append(self.Temperature[i])
                
        return np.array(D),np.array(P),np.array(T)          
        
if __name__ == "__main__":
    import sys
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
    except:
        from PyQt5.QtWidgets import QApplication
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    GUI = InputTable(test=True)
    GUI.show()
    app.exec_()