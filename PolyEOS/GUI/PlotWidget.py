# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 20:27:11 2018

@author: wangf
"""
import sys

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg 
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar  
    PYQT = 4
except:
    from PyQt5.QtWidgets import (QApplication,QWidget,QVBoxLayout, QHBoxLayout,\
                                 QSplitter, QLabel,QGridLayout, QPushButton,QComboBox )  
    from PyQt5.QtGui import (QFont)
    from PyQt5.QtCore import (Qt)
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg 
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar  
    PYQT = 5

from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.text import Text    
import matplotlib.ticker as ticker
import numpy as np


class CustomToolbar(NavigationToolbar):
    '''
    customize toolbar 
    '''
    def __init__(self,canvas_,parent_):
        self.toolitems = (
            ('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
            ('Back', 'consectetuer adipiscing elit', 'back', 'back'),
            ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
            ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
            ('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
            )
        NavigationToolbar.__init__(self,canvas_,parent_)
        
        
class FigureCanvas(FigureCanvasQTAgg):
    '''
    This class is a widget contaitn plots which gives user a interactive way
    to make plot.
    '''
    def __init__(self,parent=None):
        self.figure = Figure(dpi=150)
        self.ax = self.figure.add_subplot(111) 
        super(FigureCanvas,self).__init__(self.figure)
        #self.Draw()
        self.SetXlabel()
        self.SetYlabel()
        self.Pickable()
        self.figure.canvas.mpl_connect('pick_event', self.onpick2)
        
    
    def Pickable(self):
        """
        Define object needed to be pick.
        """
        for label in self.ax.get_xticklabels():  # make the xtick labels pickable
            label.set_picker(True)
        for label in self.ax.get_yticklabels():  # make the xtick labels pickable
            label.set_picker(True)            
        
    def Draw(self,xdata=[1,2,3],ydata=[[1,2,3],[2,3,4]],ax=None,alpha=1,color='#aa55ff',linewidth=1, linestyle='-'):
        '''
        Draw data on given axis, all Args are parameters used in matplotlib 
        Axes class
        
        Args:
            data: float array, data to plot 
            ax: mtplotlib axes class
            alpha: float, 0 transparent through 1.0 opaque, default=1
            color: a hex RGB or RGBA string
            linewidth: float, line width in points, default=1
            linestyle: tuple, set the linestyle of the line, default=solid
            
        Return:
            No return
        '''
        if ax is None:
            ax = self.ax
        for num,data in enumerate(ydata):
            ax.plot(data, alpha=alpha, color=color, linewidth=linewidth+num/2,\
                    linestyle=linestyle, picker=True)

    def DrawFill(self,xdata=[1,2,3],ydata=[[1,2,3],[2,3,4]],ydatastd=[[1,1,1],[1,1,1]],ax=None,alpha=1,color='#aa55ff',linewidth=1, linestyle='-'):
        '''
        Draw data on given axis, all Args are parameters used in matplotlib 
        Axes class
        
        Args:
            data: float array, data to plot 
            ax: mtplotlib axes class
            alpha: float, 0 transparent through 1.0 opaque, default=1
            color: a hex RGB or RGBA string
            linewidth: float, line width in points, default=1
            linestyle: tuple, set the linestyle of the line, default=solid
            
        Return:
            No return
        '''

        xdata = np.array(xdata)
        ydata = np.array(ydata)
        if ax is None:
            ax = self.ax
        ax.cla()
        for num in range(len(ydata)):
            ax.plot(xdata,ydata[num], alpha=1, color=color, linewidth=linewidth+num/2,\
                    linestyle=linestyle, picker=True)
            ax.fill_between(xdata,ydata[num]-ydatastd[num],ydata[num]+ydatastd[num],facecolor='blue', interpolate=True)
        
        
    def SetXlabel(self, text='', ax=None, fontsize=12, verticalalignment='top',\
                  horizontalalignment='center'):
        '''
        Set X label on a given axia, all Args are parametres used in matplotlib
        Axes class
        
        Args:
            text: string, text content on xlable
            ax: mtplotlib axes class
            fontsize: float, size of the text
            verticalalignment: string, vertial alignment, must be 'top', 'bottom'
                                'center' or 'baseline', default is top
            horizontalalignment: string, horizontala alignment, must be 'center'
                                , 'right', 'left', default is center

        Return:
            No return        
        '''
        if ax is None:
            ax = self.ax        
        ax.set_xlabel(text, fontsize=fontsize, verticalalignment=verticalalignment, \
                      horizontalalignment=horizontalalignment, picker=True)

        

        
        


    def SetYlabel(self, text='', ax=None, fontsize=12, verticalalignment='bottom',\
                  horizontalalignment='center',rotation=90):
        '''
        Set Y label on a given axia, all Args are parametres used in matplotlib
        Axes class
        
        Args:
            text: string, text content on xlable
            ax: mtplotlib axes class
            fontsize: float, size of the text
            verticalalignment: string, vertial alignment, must be 'top', 'bottom'
                                'center' or 'baseline', default is top
            horizontalalignment: string, horizontala alignment, must be 'center'
                                , 'right', 'left', default is center
            rotation: float, rotate angle in degree                

        Return:
            No return        
        '''
        if ax is None:
            ax = self.ax
        ax.set_ylabel(text, fontsize=fontsize, verticalalignment=verticalalignment, \
                      horizontalalignment=horizontalalignment, picker=True )    
        

    def onpick2(self,event):
        print (event.artist)
        print (type(event.artist))
        if isinstance(event.artist, Line2D):
            print ('Ture')
        if isinstance(event.artist, Text):
            text = event.artist
            print('onpick1 text:', text.get_text())
            text.set_text('wf')
# =============================================================================
#         if isinstance(event.artist, Tick):
#             print ('Ture1')
# =============================================================================
        

class FigureCanvasSplitter(QSplitter):
    '''
    Splitter contain FigureCanvas
    '''
    
    def __init__(self,parent=None):
        super(FigureCanvasSplitter, self).__init__(Qt.Vertical,parent)  
        self.title='figure'
        self.canvas = FigureCanvas(parent=parent)
        self.ntb = CustomToolbar(self.canvas, self)    
        self.addWidget(self.canvas)        
        self.addWidget(self.ntb)     
        self.com = QComboBox()
        self.com.addItems(['Depth (km)','Pressure (GPa)','Temperature (K)'])
        self.com1 = QComboBox()
        self.com1.addItems(['Vp (km/s)','Vs (km/s)','Density (Kg/m3)'])
        layout = QSplitter()
        layout.addWidget(self.com)
        layout.addWidget(self.com1)
        self.addWidget(layout)
        
    def New(self):
        self.canvas.ax.cla()
        #self.canvas.ax.draw()


if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    #from Mineral_Physics.Solidsolution import c2c ,CF,Cpx,Gt,Aki,Wus,O,Opx,Pl,Ppv,Pv,Ring,Sp,Wad
    #qapp = QApplication(sys.argv)
    GUI =FigureCanvasSplitter()
    GUI.canvas.DrawFill()
    GUI.show()
    app.exec_()