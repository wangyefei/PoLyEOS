# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 13:10:42 2018

@author: wangf
"""
try:
    from PyQt5.QtWidgets import  QWidget,QVBoxLayout,QTabWidget,QTableWidgetItem
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    
try:
    from CustomWidget.Table import TableWidgetCustom
except:
    from .CustomWidget.Table import TableWidgetCustom   

class TabTable(QWidget):
    """
    This is the base widget for tab table
    """
    def __init__(self, parent=None,**kwargs):   
        super(TabTable, self).__init__(parent)
        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300,200) 
 
        # Add tabs
        for i in kwargs:
            self.tabs.addTab(kwargs[i],i)

 
 
        # Add tabs to widget        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
 
    
    def New(self):
        self.tabs.currentWidget().New()
"""
    params = {
            'V_0': ufloat(8.826,0.1),
            'K_0': ufloat(129, 1),
            'G_0': ufloat(129, 1),
            'S_0':ufloat(198.0,10),
            'molar_mass':100,
            'n':3,
            'a_0':ufloat(0.3698*1e-5,1e-6),
            "dKdP": ufloat(4.21796,0.1),
            "dGdP": ufloat(1.21796,0.1),
            "dKdT0T": ufloat(1.1,0.1),
            "d2KdP2": ufloat(0.0127, 0.001),
            'Debye00': ufloat(809.1703,10),
            'grueneisen00': ufloat(0.99282,0.1),
            'q00': ufloat(2.10672,0.1),
            'G00': ufloat(81599990000.0,1599990000),
            "G'00": ufloat(1.46257,0.1),
            'eta_s_0': ufloat(2.29972,0.1),
            }
"""

class HPInput(TableWidgetCustom):
    """
    This class is used to store user input for HP EPS
    """
    def __init__(self,parent=None):
        super(HPInput, self).__init__(parent)
        self.name = 'HP'
        self.setWindowTitle("HP EOS")
        paramslist = ['Name','Formula','V_0 (cm³/mol)','Rho (kg/m³)','K_0 (GPa)',"K'","K''",\
                      'G_0 (GPa)',"G'",'a_0 (1/K)','S_0 J/(K*mol)']     
        params = ['fo','Mg2SiO4','4.366e-05(1e-6)','3210(1)','127(1)','4.1(0.1)','0.0127(0.001)',\
                  '81.(5)','1.21(0.1)','0.36981e-5(1e-6)','198.0(10)']
        self.row = len(paramslist)
        self.createTable(row=len(paramslist),col=2)
        self.paramsSet(paramslist = paramslist)
        self.paramsData(params = params)
        self.setHorizontalHeaderLabels(['name','value'])
        
    def New(self):
        for row in range((self.row)):
            self.setItem(row,1, QTableWidgetItem("0(0)"))

class SLBInput(TableWidgetCustom):
    """
    This class is used to store user input for HP EPS
    """
    def __init__(self,parent=None):
        super(SLBInput, self).__init__(parent)
        self.name = 'SLB'
        self.setWindowTitle("HP EOS")
        paramslist = ['Name','Formula','V_0 (cm³/mol)','K_0 (GPa)',"K'","K''",\
                      'G_0 (GPa)',"G'",'Debye_0 (K)','grueneisen_0','q_0','eta_s_0']
        params = ['fo','Mg2SiO4','4.366e-05(1e-6)','127(1)','4.1(0.1)','0.0127(0.001)',\
                  '81.(5)','1.21(0.1)','809.(10)','0.99282(0.1)','2.1(0.1)','2.2(0.1)']  
        self.row = len(paramslist)
        self.createTable(row=len(paramslist),col=2)
        self.paramsSet(paramslist=paramslist)
        self.paramsData(params = params)
        self.setHorizontalHeaderLabels(['name','value'])


    def New(self):
        for row in range((self.row)):
            self.setItem(row,1, QTableWidgetItem("0(0)"))    

if __name__ == "__main__":
    import sys
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
    except:
        from PyQt5.QtWidgets import QApplication
    a = HPInput()
    b = SLBInput()
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    GUI = TabTable(HP_EOS = a,SLB_EOS=b)
    #GUI = HPInput()
    GUI.show()
    app.exec_()
        