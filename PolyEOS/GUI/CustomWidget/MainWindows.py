# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 12:53:24 2018

@author: wangf
"""
import sys
import os
try:
    from PyQt5.QtWidgets import (QMainWindow, QApplication,QAction,QFileDialog,\
                                 QMdiArea,QTextEdit,QMdiSubWindow,QDockWidget)
    from PyQt5.QtGui import (QIcon,QKeySequence)
    from PyQt5.QtCore import Qt
    PYQT = 5
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    PYQT = 4
#from PlotWidget import FigureCanvasSplitter
#from Table import Table
#from DockWidget import DockWidget


class MainWindow(QMainWindow):
    
    def __init__(self,test=False):
        super(MainWindow, self).__init__()
        self.structure=[]
        self.ManuBar()
        self.ToolBar()
        self.MDI()
        self.Dock()
        self.StatusBar()
        self.resize(1800,1000)
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
        self.ManuBarEdit()
        self.DataBarEdit()
        self.ManuBarView()
        
        
    ### Manu Bar File
    def ManuBarFile(self):
        self.fileNewAction = self.CreateAction(text="&New...", slot=self.fileNew,
                                          shortcut=QKeySequence.New,
                                          icon=os.path.join(os.getcwd(), 'image', 'new-file.png'),
                                          tip ="Create an new file")
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.fileNewAction)
        
    def fileNew(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if PYQT == 5:
            fileName = fileName[0]
        else:
            pass
        if fileName:
            file1 = open(fileName,'r')
            ReadFile()
            file1.close()
    
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
        sub = Table(parent=self)
        self.mdi.addSubWindow(sub)
        sub.show()
        self.structure.append(sub)
        self.UpdateDock()

 
    def CreatFigure(self):
        sub = FigureCanvasSplitter()
        self.mdi.addSubWindow(sub)
        sub.show()
        self.structure[0].figures.append(sub)
        self.UpdateDock()
        

        
    ### Manu Bar View   
    def ManuBarView(self):
        togglefileTool = self.CreateAction(text="Toggle Toolbar", slot=self.handleToggleTool,
                                           tip='hide toolbar',checkable=True)
        toggleStatus = self.CreateAction(text="Toggle Statusbar", slot=self.handleToggleStatus,
                                           tip='hide statusbar',checkable=True)
        
        self.viewMenu = self.menuBar().addMenu("&View") 
        self.viewMenu.addAction(togglefileTool)
        self.viewMenu.addAction(toggleStatus)        

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
        self.dock = QDockWidget("Dock",self)
        self.dockwidget = DockWidget()
        self.dock.setWidget(self.dockwidget)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock)
        self.dockwidget.Layout(self.structure)
    
    def UpdateDock(self):
        self.dockwidget.Layout(self.structure)
        #self.dockwidget.treeView.setModel(self.dockwidget.model)

        
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