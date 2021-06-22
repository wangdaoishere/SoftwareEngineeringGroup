import sys
import math
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QComboBox,QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel

class Interface_method:
    def sin(self,value):
        return math.sin(value)
    def arcsin(self,value):
        return math.asin(value)
    def tan(self,value):
        return math.tan(value)

    def arctan(self,value):
        return math.atan(value) 
    def get_func_name(self):
        return sorted(self.valueFunctions.keys())   
    def get_func_result(self,name,value):
        return self.valueFunctions[name](value)
    def __init__(self):
        self.valueFunctions = {
                        'sin': self.sin, 
                        'arcsin': self.arcsin,
                        'tan': self.tan,
                        'arctan': self.arctan,    
                    }


class Example(QWidget):
  
    def __init__(self):
        super().__init__()
        self.method=Interface_method()
        self.initUI()
    def initUI(self):
        # adaptive screen resolution
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        #self.setGeometry(300, 300,  int(self.width*0.2), int(self.width*0.2*0.3))
        self.setFixedSize(int(self.width*0.2), int(self.width*0.2*0.3))
        
        self.center()
        self.setWindowTitle('Calculator')
               
        #print(self.height)
        #print(self.width)
            
        self.btn_Calc = QPushButton('Calc', self)
        self.btn_Calc.clicked.connect(self.btn_Calc_on_click)
        
        self.cb_method = QComboBox(self)
        self.cb_method.addItems(self.method.get_func_name())
        
        self.btn_format = QPushButton('deg', self) 
        self.btn_format.clicked.connect(self.btn_format_on_click)
        
        self.qle_input = QLineEdit(self)
        
        self.qle_output = QLineEdit(self)
        
        self.qlb_result = QLabel('result',self)
        
        self.hbox_input = QHBoxLayout()
        self.hbox_output = QHBoxLayout()
        self.vbox = QVBoxLayout()
        
        self.hbox_input.addWidget(self.cb_method,1)
        self.hbox_input.addWidget(self.qle_input,4)
        self.hbox_input.addWidget(self.btn_format,1)
        
        self.hbox_output.addWidget(self.qlb_result,1,Qt.AlignCenter)
        self.hbox_output.addWidget(self.qle_output,4)
        self.hbox_output.addStretch(1)
        
        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_output)
        self.vbox.addWidget(self.btn_Calc)
        #vbox.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)
        self.show()
        
    # set window location at the center of screen    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def btn_format_on_click(self):
        sender = self.sender()
        text = sender.text()
        sender.setText("rad" if text == "deg" else "deg")
    
    def btn_Calc_on_click(self):
        str_input = self.qle_input.text().strip();
        if(str_input == '') :
            return
        self.qle_output.setText(str(self.method.get_func_result(self.cb_method.currentText(),float(eval(str_input)))))
        
if __name__ == '__main__':

      app = QApplication(sys.argv)
      ex = Example()
      sys.exit(app.exec_())      
