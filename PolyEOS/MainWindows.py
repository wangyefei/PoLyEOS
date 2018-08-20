# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 12:53:24 2018

@author: wangf
"""
import sys
import os
import numpy as np
try:
    from PyQt5.QtWidgets import (QMainWindow, QApplication,QAction,QFileDialog,\
                                 QMdiArea,QTextEdit,QMdiSubWindow,QDockWidget,\
                                 QTableWidgetItem)
    from PyQt5.QtGui import (QIcon,QKeySequence)
    from PyQt5.QtCore import Qt,QSize
    PYQT = 5
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    PYQT = 4

from GUI.DockWidget import TabTable,HPInput,SLBInput
from GUI.InputTable import InputTable
from GUI.PlotWidget import FigureCanvasSplitter
from GUI.PolyAverage import CijTable,GUI_polyaverage
from EOS.HP2011 import HP_Vp_Vs
from EOS.SLB import Stix_Vp_Vs
from EOS.tools import dictionarize_formula,formula_mass,atomic_masses
#from uncertainties import ufloat, unumpy, test_uncertainties

class MainWindow(QMainWindow):
    
    def __init__(self,test=False):
        super(MainWindow, self).__init__()
        self.ManuBar()
        self.ToolBar()
        self.MDI()
        self.Dock()
        self.StatusBar()
        self.resize(1800,900)
        try:
            self.setWindowIcon(QIcon('mor.png'))
        except:
            print ('wf')
        if test:
            self.CreatDataSheet()
            self.CreatFigure()
        

    """
    This part is about the menubar settings
    """   

    def CreateAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            getattr(action, signal).connect(slot)
#            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
     
    def ManuBar(self):
        self.ManuBarFile()
        #self.ManuBarEdit()
        #self.DataBarEdit()
        self.ManuBarView()
        
        
    ### Manu Bar File
    def ManuBarFile(self):
        self.fileNewAction = self.CreateAction(text="&New...", slot=self.fileNew,
                                          shortcut=QKeySequence.New,
                                          icon=os.path.join(os.getcwd(), 'GUI','image', 'new-file.png'),
                                          tip ="Create an new file")
        self.fileRunAction = self.CreateAction(text="&Run...", slot=self.fileRun,
                                          #shortcut=QKeySequence.New,
                                          icon=os.path.join(os.getcwd(), 'GUI','image', 'Run.png'),
                                          tip ="Run the file")        
        self.fileMenu = self.menuBar().addMenu("&File")       
        self.fileMenu.addAction(self.fileNewAction)
        self.fileMenu.addAction(self.fileRunAction)    
        
    def fileNew(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if PYQT == 5:
            fileName = fileName[0]
        else:
            pass
        if fileName:
            file1 = open(fileName,'r')
            file1.close()

    def GetParams(self):
        self.dockwidget.tabs.currentWidget().GetParams()
        self.params = self.dockwidget.tabs.currentWidget().params
        n = sum(dictionarize_formula(self.params['Formula']).values())
        molar_mass = formula_mass(dictionarize_formula(self.params['Formula']),atomic_masses)
        self.params.update({'n': n})
        self.params.update({'molar_mass': molar_mass})
        

    def GetDPT(self):
        self.Depth,self.Temperature,self.Pressure  = self.inputtable.GetData()
        num = len(self.Depth)
        self.Vp  = np.zeros(num);self.Vpstd = np.zeros(num);
        self.Vs  = np.zeros(num);self.Vsstd = np.zeros(num);
        self.Rho = np.zeros(num);self.Rhostd = np.zeros(num);
   
    def Plot(self):
        xx = self.figure.com.currentIndex()
        yy = self.figure.com1.currentIndex()   
        if xx == 0:
            xdata = self.Depth
            xlabel = 'Depth (km)'
        if xx == 1:
            xdata = self.Pressure
            xlabel = 'Pressure (GPa)'
        if xx ==2:
            xdata = self.Temperature
            xlabel = "Temperature (K)"
 
        
        if yy == 0:
            ydata = self.Vp
            ydatastd = self.Vpstd
            ylabel = 'Vp (Km/s)'
        if yy == 1:
            ydata = self.Vs
            ydatastd = self.Vsstd  
            ylabel = 'Vs (Km/s)'
        if yy == 2:
            ydata = self.Rho
            ydatastd = self.Rhostd   
            ylabel = 'Rho (Kg/m3)'

        self.figure.canvas.DrawFill(xdata,ydata=[ydata],ydatastd=[ydatastd],ax=None,alpha=1,color='#aa55ff',linewidth=1, linestyle='-')

        
        self.figure.canvas.SetXlabel(xlabel)
        self.figure.canvas.SetYlabel(ylabel)
        self.figure.canvas.draw()
        
        
    def fileRun(self):
        if self.dockwidget.tabs.currentWidget().name == 'HP':
            self.GetDPT()
            self.GetParams()
            num = len(self.Depth)
            for i in range(num):
                if self.Depth[i] != -1 and self.Pressure[i] != -1 and self.Temperature[i] != -1:
                    Vp,Vs,Rho,K,G  = HP_Vp_Vs(self.Pressure[i],self.Temperature[i],self.params,Tr=298)
                    self.inputtable.setItem(i,3, QTableWidgetItem(str(Vp)) )
                    self.inputtable.setItem(i,4, QTableWidgetItem(str(Vs)) )
                    self.inputtable.setItem(i,5, QTableWidgetItem(str(Rho)) )
                    self.Vp[i] =  Vp.all().n; self.Vpstd[i] = Vp.all().std_dev
                    self.Vs[i] =  Vs.all().n; self.Vsstd[i] = Vs.all().std_dev
                    self.Rho[i] = Rho.n;self.Rhostd[i] = Rho.std_dev
       
        elif self.dockwidget.tabs.currentWidget().name == 'SLB':
            self.GetDPT()
            self.GetParams()
            num = len(self.Depth)            
            self.params['G_0 (GPa)'] *= 1e9
            self.params['K_0 (GPa)'] *= 1e9
            for i in range(num):
                if self.Depth[i] != -1 and self.Pressure[i] != -1 and self.Temperature[i] != -1:
                    Vp,Vs,Rho,K,G  = Stix_Vp_Vs(self.Pressure[i]*1e9,self.Temperature[i],self.params,Tr=298)
                    self.inputtable.setItem(i,3, QTableWidgetItem(str(Vp)) )
                    self.inputtable.setItem(i,4, QTableWidgetItem(str(Vs)) )
                    self.inputtable.setItem(i,5, QTableWidgetItem(str(Rho)) )
                    self.Vp[i] =  Vp.n; self.Vpstd[i] = Vp.std_dev
                    self.Vs[i] =  Vs.n; self.Vsstd[i] = Vs.std_dev
                    self.Rho[i] = Rho.n;self.Rhostd[i] = Rho.std_dev
                    #print ('wf')
        else:
            pass
        #print ('dond')
        self.Plot()
        self.update()
                    
    
    ### Manu Bar Edit        
    def ManuBarEdit(self):
        self.editMenu = self.menuBar().addMenu("&Edit")    
        
    ### Dat bar Edit
    def DataBarEdit(self):
        addDataSheet = self.CreateAction(text="&New data", slot=self.CreatDataSheet,
                                          tip ="Create an new data sheet")
        addDataPlot = self.CreateAction(text="&New plot", slot=self.CreatFigure,
                                          tip ="Create an new plot")        
        self.dataMenu = self.menuBar().addMenu("&Data")
        self.dataMenu.addAction(addDataSheet)
        self.dataMenu.addAction(addDataPlot)
        
    def CreatDataSheet(self):
        self.inputtable = InputTable(test=True)
        self.inputtable.setMinimumHeight(self.height())
        self.inputtable.setMinimumWidth(0.24*self.width())
        self.mdi.addSubWindow(self.inputtable)
        self.inputtable.show()


 
    def CreatFigure(self):
        self.figure = FigureCanvasSplitter()
        self.mdi.addSubWindow(self.figure)
        self.figure.setBaseSize(QSize(350,500))
        self.figure.show()

        

        
    ### Manu Bar View   
    def ManuBarView(self):
        togglefileTool = self.CreateAction(text="Toggle Toolbar", slot=self.handleToggleTool,
                                           tip='hide toolbar',checkable=True)
        toggleStatus = self.CreateAction(text="Toggle Statusbar", slot=self.handleToggleStatus,
                                           tip='hide statusbar',checkable=True)
        dock1  = self.CreateAction(text="Toggle EOS data sheet", slot=self.EOSData,
                                           tip='EOS data sheet show',checkable=True)
        dock2  = self.CreateAction(text="Toggle Cij data sheet", slot=self.CijData,
                                           tip='Cij data sheet show',checkable=True)        
        self.viewMenu = self.menuBar().addMenu("&View") 
        self.viewMenu.addAction(togglefileTool)
        self.viewMenu.addAction(toggleStatus) 
        self.viewMenu.addAction(dock1) 
        self.viewMenu.addAction(dock2) 

    def handleToggleTool(self):
        if self.fileToolbar.isHidden():
            self.fileToolbar.show()
        else:
            self.fileToolbar.hide()
 
 
    def handleToggleStatus(self):
        if self.status.isHidden():
            self.status.show()
        else:
            self.status.hide()

    def CijData(self):
        if self.dock1.isHidden():
            self.dock1.setVisible(True)
            #self.dock1.move(0,0)
        else:
            self.dock1.hide()        
        
    def EOSData(self):
        if self.dock.isHidden():
            self.dock.setVisible(True)
            #self.dock.move(0,0)
        else:
            self.dock.hide()

    
    """
    This part is about the toolbar
    """
    def AddActions(self, target, actions):
        for  action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)        
    
    def ToolBar(self):
        self.ToolBarFile()
                
    def ToolBarFile(self):
        self.fileToolbar = self.addToolBar("File")
        self.fileToolbar.setObjectName("FileToolBar")
        self.AddActions(self.fileToolbar, [self.fileNewAction])
        self.AddActions(self.fileToolbar, [self.fileRunAction])
    
    def ToolBarEdit(self):    
        self.editToolbar = self.AddToolBar("Edit")
        self.editToolbar.setObjectName("EditToolBar")
        self.addActions(self.editToolbar, [self.fileNewAction])

    """
    This part is main area
    """
    def MDI(self):
      self.mdi = QMdiArea()
      self.setCentralWidget(self.mdi)  
      

    '''
    This part is about the Dock Widget
    '''
    def Dock(self):
        self.dock1 = QDockWidget("Poly average",self)
        self.dock = QDockWidget("EOS",self)
        a = HPInput()
        b = SLBInput()
        c = GUI_polyaverage()
        self.dockwidget = TabTable(parent=self,HP_EOS = a,SLB_EOS=b)
        self.dock.setWidget(self.dockwidget)
        self.dock1.setWidget(c)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock1)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock)
        self.dock1.setMinimumSize(QSize(350,400))
        self.dock.setMinimumSize(QSize(350,400))        
        
        #self.dockwidget.Layout(self.structure)
    
    
    '''
    This part is status bar
    '''   
    def StatusBar(self):
        self.status = self.statusBar()
        self.status.showMessage('Message in statusbar.')
        
        
    '''
    This is for testing
    '''
    
if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    #from Mineral_Physics.Solidsolution import c2c ,CF,Cpx,Gt,Aki,Wus,O,Opx,Pl,Ppv,Pv,Ring,Sp,Wad
    #qapp = QApplication(sys.argv)
    GUI = MainWindow(test=True)
    GUI.show()
    app.exec_()
   # HP_Vp_Vs(11,1700,GUI.params)