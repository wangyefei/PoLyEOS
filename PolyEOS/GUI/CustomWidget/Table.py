# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 14:54:54 2018

@author: wangf
"""

import sys
from io import StringIO
import numpy as np
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    PYQT = 4
except:
    from PyQt5.QtWidgets import (QTableWidget,QTableWidgetItem,QApplication,QVBoxLayout,\
                                    QMessageBox )
    from PyQt5.QtGui import QAbstractOpenGLFunctions,QKeySequence
    from PyQt5.QtCore import Qt
from uncertainties import ufloat, unumpy, test_uncertainties


def String_to_float(string):
    try:
        aa =  string.split('(')
        a,b = float(aa[0]),float(aa[1][:-1])
    except:
        aa =  string.split('(')
        a,b = float(aa[0]),0
    return ufloat(a,b)


class TableWidgetCustom(QTableWidget):
    """
    This is class based on QTableWidget, the aim of this class is to add custom 
    function. Here is a list that this custom widget can do
    1) Copy text from multiple cells by CTRL + C
    """
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)    
        #self.createTable()
        
    """
    Overwrite Key Press Event
    """
    def keyPressEvent(self, event):
        """
        Replace kye press event
        """
        if event.matches(QKeySequence.Copy):
            self.copy()
        elif event.matches(QKeySequence.Paste):
            self.paste()
        else:
            QTableWidget.keyPressEvent(self, event)
      

    def copy(self):
        indexes = self.selectedItems()
        if len(indexes) < 1:
            # No row selected
            return
        text = ''
        row1 = indexes[0].row()
        for idx in indexes:
            row = idx.row()
            col = idx.column()
            if row != row1:
                text += '\n'            
            item = self.item(row, col)
            if item:
                text += item.text()
            text += ' '
            row1 = row
        QApplication.clipboard().setText(text);
        
    def paste(self):
        #print ('wf')
        text = QApplication.clipboard().text()
        #self.text = text.split('\t')
        c = np.loadtxt(StringIO(text),delimiter='\t')
        row = len(c)
        col = len(c[0])
        #print (row,col)
        indexes = self.selectedItems()
        #print (indexes[0].row(),indexes[-1].row())
        aa = indexes[-1].row() - indexes[0].row() + 1
        #print (aa,indexes[-1].column(),indexes[0].column())
        bb = indexes[-1].column() - indexes[0].column() + 1
       # print (aa,bb)
        if  bb != col:
            print ('bad')
        else:
            for i in range(len(indexes)):
                self.setItem(indexes[i].row,indexes[i].column, QTableWidgetItem(c[i]))
        pass       
            
    def createTable(self,row=10,col=3,test=False):
        """
        file in some number for test
        """
        self.setRowCount(row)
        self.setColumnCount(col)
        if test:
            self.setItem(0,0, QTableWidgetItem("1"))
            self.setItem(0,1, QTableWidgetItem("2"))
            self.setItem(1,0, QTableWidgetItem("2"))
            self.setItem(1,1, QTableWidgetItem("3"))
            self.setItem(2,0, QTableWidgetItem("4"))
            self.setItem(2,1, QTableWidgetItem("5"))
            self.setItem(3,0, QTableWidgetItem("6"))
            self.setItem(3,1, QTableWidgetItem("7"))


    """
    Custom input data
    """        
    def paramsSet(self,paramslist = None):
        self.paramslist = paramslist
        for num,name in enumerate(self.paramslist):
            item = QTableWidgetItem(name)
            item.setFlags(Qt.ItemIsEnabled)
            self.setItem(num,0, item)
            
    def paramsData(self,params = None):
        self.params = params
        for num,name in enumerate(self.params):
            item = QTableWidgetItem(name)
            #item.setFlags(Qt.ItemIsEnabled)
            self.setItem(num,1, item)
    
    def GetParams(self):
        self.params={}
        if isinstance((self.item(0,1)),type(None)):
                print ('Please input ' +self.item(0, 0).text() +': ')
        
        try:
            self.params.update({self.item(0, 0).text(): self.item(0, 1).text()})
        except:
            print ('Check input at' +self.item(0, 0).text() +': ' )
            
        try:
            self.params.update({self.item(1, 0).text(): self.item(1, 1).text()})
        except:
            print ('Check input at' +self.item(1, 0).text() +': ' )  
              
        for row in range(2,self.rowCount()):
            if isinstance((self.item(row,1)),type(None)):
                print ('Please input ' +self.item(row, 0).text() +': ')
                break
            try:
                self.params.update({self.item(row, 0).text(): self.String_to_float(self.item(row, 1).text())})
            except:
                print ('Check input at' +self.item(row, 0).text() +': ' )

        
    def String_to_float(self,string):
        try:
            aa =  string.split('(')
            a,b = float(aa[0]),float(aa[1][:-1])
        except:
            aa =  string.split('(')
            a,b = float(aa[0]),0
        return ufloat(a,b)                

                
        
        
        

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    #from Mineral_Physics.Solidsolution import c2c ,CF,Cpx,Gt,Aki,Wus,O,Opx,Pl,Ppv,Pv,Ring,Sp,Wad
    #qapp = QApplication(sys.argv)
    GUI = TableWidgetCustom()
    #GUI.createTable()
    GUI.show()
    app.exec_()