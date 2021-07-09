import sys
import math
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QComboBox, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QLabel
from TriFunctions import *


class Interface_method:

    def sin(self, value):
        return sin.sin(value)
        # return mySin(value)
        # return math.sin(value)

    def arcsin(self, value):
        return arcsin.asin(value)
        # return invert_angle_to_rad(asin(value))
        # return math.asin(value)

    def cos(self, value):
        return cos.cos(value)
        # return myCos(value)
        # return math.cos(value)

    def arctan(self, value):
        return arctan.atan(value)
        # return atan(value)
        # return math.atan(value)

    def get_func_name(self):
        return sorted(self.valueFunctions.keys())

    def get_func_result(self, name, value, is_deg):
        if is_deg:
            return self.valueFunctions[name](value)
        else:
            if "arc" in name:
                return utils.deg2rad(self.valueFunctions[name](value))
            else:
                return self.valueFunctions[name](utils.rad2deg(value))

    def __init__(self):
        self.valueFunctions = {
            'sin': self.sin,
            'arcsin': self.arcsin,
            'cos': self.cos,
            'arctan': self.arctan,
        }


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.method = Interface_method()
        self.initUI()

    def initUI(self):
        # adaptive screen resolution
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        # self.setGeometry(300, 300,  int(self.width*0.2), int(self.width*0.2*0.3))
        self.setFixedSize(int(self.width * 0.2), int(self.width * 0.2 * 0.3))

        self.center()
        self.setWindowTitle('Calculator')

        # print(self.height)
        # print(self.width)

        self.btn_Calc = QPushButton('Calc', self)
        self.btn_Calc.clicked.connect(self.btn_calc_on_click)

        self.cb_method = QComboBox(self)
        self.cb_method.addItems(self.method.get_func_name())
        self.cb_method.currentIndexChanged.connect(self.cb_method_changed)

        self.btn_format_input = QPushButton('deg', self)
        self.btn_format_input.clicked.connect(self.btn_format_on_click)
        self.btn_format_input.setEnabled(False)

        self.btn_format_output = QPushButton('deg', self)
        self.btn_format_output.clicked.connect(self.btn_format_on_click)

        self.qle_input = QLineEdit(self)
        self.qle_input.textEdited.connect(self.input_format_check)
        self.qle_input.returnPressed.connect(self.btn_calc_on_click)

        self.qle_output = QLineEdit(self)
        self.qle_output.setFocusPolicy(Qt.NoFocus)

        self.qlb_result = QLabel('result', self)

        self.hbox_input = QHBoxLayout()
        self.hbox_output = QHBoxLayout()
        self.vbox = QVBoxLayout()

        self.hbox_input.addWidget(self.cb_method, 1)
        self.hbox_input.addWidget(self.qle_input, 4)
        self.hbox_input.addWidget(self.btn_format_input, 1)

        self.hbox_output.addWidget(self.qlb_result, 1, Qt.AlignCenter)
        self.hbox_output.addWidget(self.qle_output, 4)
        self.hbox_output.addWidget(self.btn_format_output, 1)

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_output)
        self.vbox.addWidget(self.btn_Calc)
        # vbox.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbox)
        self.show()

    # set window location at the center of screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def input_format_check(self):
        """
        输入校验
        :return:
        """
        try:
            str_input = self.qle_input.text().strip()
            self.method.get_func_result(self.cb_method.currentText(), float(eval(str_input)),
                                        self.btn_format_input.text() == "deg" and self.btn_format_input.isEnabled() or self.btn_format_output.text() == "deg" and self.btn_format_output.isEnabled())
        except:
            self.qle_input.setStyleSheet("color: red;")
            self.qle_output.setStyleSheet("color: red;")
            self.qle_output.setText("无效输入!")
            self.btn_Calc.setEnabled(False)
        else:
            self.qle_input.setStyleSheet("color: black;")
            self.qle_output.setStyleSheet("color: black;")
            self.qle_output.setText("")
            self.btn_Calc.setEnabled(True)

    flag = 0

    def cb_method_changed(self):
        """
        选择sin、cos时输入框后单位可选为角度或弧度，输出框后单位为不可选状态。
        选择arcsin、arctan时输入框后单位为不可选状态，输出框后单位可选为角度或弧度。
        :return: None
        """
        if "arc" in self.cb_method.currentText():
            self.btn_format_input.setEnabled(False)
            self.btn_format_output.setEnabled(True)
            # self.flag = 0
        else:
            self.btn_format_input.setEnabled(True)
            self.btn_format_output.setEnabled(False)
            # self.flag = 1
        self.input_format_check()  # 选择函数改变后对输入进行校验

    def btn_format_on_click(self):
        """
        切换输入框/输出框后的单位
        :return:None
        """
        sender = self.sender()
        text = sender.text()
        sender.setText("rad" if text == "deg" else "deg")

    def btn_calc_on_click(self):
        """
        点击计算按钮执行动作
        :return: None
        """
        str_input = self.qle_input.text().strip()
        if str_input == "":
            return
        self.qle_output.setText(
            str(self.method.get_func_result(self.cb_method.currentText(), float(eval(str_input)),
                                            self.btn_format_input.text() == "deg" and self.btn_format_input.isEnabled()  # 执行的是sin/cos计算
                                            or
                                            self.btn_format_output.text() == "deg" and self.btn_format_output.isEnabled()  # 执行arcsin/arctan
                                            )
                )
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
