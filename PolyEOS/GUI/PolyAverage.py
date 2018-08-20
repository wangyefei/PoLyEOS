import sys
import numpy as np
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    PYQT = 4
except:
    from PyQt5.QtWidgets import QWidget,QApplication,QCheckBox,QSplitter,QLabel,QComboBox,\
                                QTableWidget,QTableWidgetItem,QHBoxLayout,QVBoxLayout,QPushButton,\
                                QTextEdit,QMessageBox,QHeaderView
    from PyQt5.QtGui import QKeySequence
    from PyQt5.QtCore import Qt
    PYQT = 5
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
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)

    def keyPressEvent(self, event):
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
            print (row,col,row1,row!=row1)
            if row != row1:
                text += '\n'            
            item = self.item(row, col)
            if item:
                text += item.text()
            text += ' '
            row1 = row
        QApplication.clipboard().setText(text);

    def Paste(self):
        QApplication.clipboard().text()
        pass

class CijTable(TableWidgetCustom):
    """
    store Cij data
    """
    def __init__(self):
        super(CijTable,self).__init__()
        self.resize(400, 50)
        self.setRowCount(6)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(['Ci1', 'Ci2', 'Ci3', 'Ci4', 'Ci5','Ci6'])
        self.setVerticalHeaderLabels(['C1j', 'C2j', 'C3j', 'C4j', 'C5j','C6j'])
        self.SetData()
        header = self.horizontalHeader()    
        if PYQT == 5:
            for i in range(6):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.setGeometry(300, 300, 600, 600)
         
    def SetData(self):
        self.setItem(0,0, QTableWidgetItem("298(13.)"))
        self.setItem(0,1, QTableWidgetItem("115(6)"))
        self.setItem(0,2, QTableWidgetItem("115(6)"))
        self.setItem(0,3, QTableWidgetItem("0(0)"))
        self.setItem(0,4, QTableWidgetItem("0(0)"))
        self.setItem(0,5, QTableWidgetItem("0(0)"))
        self.setItem(1,0, QTableWidgetItem("115(6)"))
        self.setItem(1,1, QTableWidgetItem("298(13.)"))
        self.setItem(1,2, QTableWidgetItem("115(6)"))
        self.setItem(1,3, QTableWidgetItem("0(0)"))
        self.setItem(1,4, QTableWidgetItem("0(0)"))
        self.setItem(1,5, QTableWidgetItem("0(0)"))
        self.setItem(2,0, QTableWidgetItem("115(6)"))
        self.setItem(2,1, QTableWidgetItem("115(6)"))
        self.setItem(2,2, QTableWidgetItem("298(13.)"))
        self.setItem(2,3, QTableWidgetItem("0(0)"))
        self.setItem(2,4, QTableWidgetItem("0(0)"))
        self.setItem(2,5, QTableWidgetItem("0(0)"))        
        self.setItem(3,0, QTableWidgetItem("0(0)"))
        self.setItem(3,1, QTableWidgetItem("0(0)"))
        self.setItem(3,2, QTableWidgetItem("0(0)"))
        self.setItem(3,3, QTableWidgetItem("112(6)"))
        self.setItem(3,4, QTableWidgetItem("0(0)"))
        self.setItem(3,5, QTableWidgetItem("0(0)"))
        self.setItem(4,0, QTableWidgetItem("0(0)"))
        self.setItem(4,1, QTableWidgetItem("0(0)"))
        self.setItem(4,2, QTableWidgetItem("0(0)"))
        self.setItem(4,3, QTableWidgetItem("0(0)"))
        self.setItem(4,4, QTableWidgetItem("112(6)"))
        self.setItem(4,5, QTableWidgetItem("0(0)"))
        self.setItem(5,0, QTableWidgetItem("0(0)"))
        self.setItem(5,1, QTableWidgetItem("0(0)"))
        self.setItem(5,2, QTableWidgetItem("0(0)"))
        self.setItem(5,3, QTableWidgetItem("0(0)"))
        self.setItem(5,4, QTableWidgetItem("0(0)"))
        self.setItem(5,5, QTableWidgetItem("112(6)"))  
    
    def GetData(self):
        c = [[],[],[],[],[],[]]
        for row in range(6):
            for col in range(6):
                try:
                    c[row].append(String_to_float(self.item(row,col).text()))
                except:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Check number in row:" + str(row+1)+"column:" + str(col+1))
                    msg.setWindowTitle("MessageBox")
                    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    if msg.exec_()== QMessageBox.Yes:
                        return True
                    else:
                        return False  
        self.c = unumpy.matrix(c)
        
        
class Selection(QWidget):
    """
    This class use for select point group and crystal systems.
    """
    def __init__(self):
        super(Selection, self).__init__()  
        label1 = QLabel("1. Please select a crystal systems")
        self.selectxtalsystems = QComboBox()
        self.selectxtalsystems.addItems(['Cubic'])
        label2 = QLabel("2. Please select a point group")
        self.selectPG = QComboBox()
        self.selectPG.addItems(['select'])        
        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.selectxtalsystems )
        layout.addWidget(label2)
        layout.addWidget(self.selectPG )
        self.setLayout(layout)
        
        



class GUI_polyaverage(QWidget):
    
    def __init__(self,parent=None):
        super(GUI_polyaverage, self).__init__(parent)    
        self.initUI()
        
    def initUI(self): 
        layout_fig = QSplitter(Qt.Vertical)
# =============================================================================
#         self.select = Selection()
#         self.layout_fig.addWidget(self.select)
# =============================================================================
        self.table = CijTable()
        layout_fig.addWidget(self.table)
        button = QPushButton()
        button.setText('Calculate')
        button.clicked.connect(self.calculate)
        layout_fig.addWidget(button)
        self.text = QTextEdit()
        layout_fig.addWidget(self.text)        
        layout = QVBoxLayout()
        layout.addWidget(layout_fig)

        self.setLayout(layout)
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Elastic properties')
   
    def calculate(self):
        self.table.GetData()
        print ('getdata')
        c = self.table.c
        try:
            s = c.I
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Singular matrix")
            msg.setWindowTitle("MessageBox")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg.exec_()== QMessageBox.Yes:
                return True
            else:
                return False  
        print ('inverse')
        s = np.array(s)
        c = np.array(c)
        self.c = c
        self.s = s
        #print ('wf1')
        self.Br = 1./ ((s[0][0] + s[1][1] + s[2][2]) + 2.*(s[0][1] + s[1][2] + s[2][0]))
        self.Gr = 15./ (4*(s[0][0] + s[1][1] + s[2][2]) - 4.*(s[0][1] + s[1][2] + s[2][0]) + 3.*(s[3][3] + s[4][4] + s[5][5]))
        self.Bv = (1./9.) * (c[0][0] + c[1][1] + c[2][2]) + (2./9.) * (c[0][1] + c[0][2] + c[1][2]) 
        self.Gv = (1./15.) * (c[0][0] + c[1][1] + c[2][2] - c[0][1] -c[2][0] -c[1][2]) + (1./5.) * (c[3][3] + c[4][4] + c[5][5])  
        self.Bh = 0.5* (self.Br + self.Bv)
        self.Gh = 0.5* (self.Gr + self.Gv)
        self.E = 9*self.Bh*self.Gh/(3*self.Bh+self.Gh)
        self.A = 5 * (self.Gv/self.Gr) + (self.Bv/self.Br) - 6
        self.I = (3*self.Bh - 2*self.Gh) /(6*self.Bv + 2*self.Gv)
        
        string1 = "Bulk modulus (Voigt):         " + str(self.Bv) + '\n'
        string2 = "Shear modulus (Voigt):        " + str(self.Gv) + '\n'
        string3 = "Bulk modulus (Reuss):         " + str(self.Br) + '\n'
        string4 = "Shear modulus (Reuss):        " + str(self.Gr) + '\n'
        string5 = "Bulk modulus (VHR):           " + str(self.Bh) + '\n'
        string6 = "Shear modulus (VHR):          " + str(self.Gh) + '\n'   
        string7 = "Universal elastic anisotropy: " + str(self.A) + '\n'   
        string8 = "Isotropic Poisson ratio:      " + str(self.I) + '\n'   
        string = string1 + string2 + string3 + string4 + string5 + string6 + string8 #+ string8
        
        f = self.text.font()
        f.setPointSize(10) # sets the size to 27
        self.text.setFont(f)

        self.text.setText(string)
        self.update()


if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    Gui = GUI_polyaverage()
    Gui.show()
    app.exec_()
