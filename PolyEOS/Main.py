# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 17:35:43 2018

@author: wangf
"""
import sys
try:
    from PyQt5.QtWidgets import (QApplication)
    PYQT = 5
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    PYQT = 4

from MainWindows import MainWindow

print ('wf')
GUI = MainWindow(test=True)
GUI.show()
#app.exec_()
    
    
# =============================================================================
# if __name__ == "__main__":
#     if not QApplication.instance():
#         app = QApplication(sys.argv)
#     else:
#         app = QApplication.instance() 
#     #from Mineral_Physics.Solidsolution import c2c ,CF,Cpx,Gt,Aki,Wus,O,Opx,Pl,Ppv,Pv,Ring,Sp,Wad
#     #qapp = QApplication(sys.argv)
#     GUI = MainWindow(test=True)
#     GUI.show()
#     app.exec_()
#    # HP_Vp_Vs(11,1700,GUI.params)    
# =============================================================================
