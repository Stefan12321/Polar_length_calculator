import math

from PyQt5 import QtWidgets
from add_point_dlg import Ui_Dialog


class AddPointDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(AddPointDialog, self).__init__()
        self.setupUi(self)
        self.lineEdit_x.setText('0')
        self.lineEdit_y.setText('0')
        self.point = [None, None]
        self.add_function()
        self.dont_change = False

    def add_function(self):
        self.conn_func = lambda: self.sync()
        self.pushButton_ok.clicked.connect(lambda: self.ok())
        self.pushButton_cancel.clicked.connect(lambda: self.close())
        self.lineEdit_x.textChanged.connect(self.conn_func)
        self.lineEdit_y.textChanged.connect(self.conn_func)
        self.lineEdit_angle.textChanged.connect(self.conn_func)
        self.lineEdit_radius.textChanged.connect(self.conn_func)

    def sync(self):
        sender = self.sender()
        # print('sender: ', sender)
        if sender is self.lineEdit_x or sender is self.lineEdit_y:
            try:
                x = float(self.lineEdit_x.text())
                y = float(self.lineEdit_y.text())
                r, O = self.from_cartesian_to_polar(x, y)
                self.lineEdit_angle.textChanged.disconnect(self.conn_func)
                self.lineEdit_radius.textChanged.disconnect(self.conn_func)
                self.lineEdit_angle.setText(str(round(O, 2)))
                self.lineEdit_radius.setText(str(round(r, 2)))
                self.lineEdit_angle.textChanged.connect(self.conn_func)
                self.lineEdit_radius.textChanged.connect(self.conn_func)
            except:
                pass
        elif sender is self.lineEdit_angle or sender is self.lineEdit_radius:
            try:
                r = float(self.lineEdit_radius.text())
                O = float(self.lineEdit_angle.text())
                x, y = self.from_polar_to_cartesian(O, r)
                self.lineEdit_x.textChanged.disconnect(self.conn_func)
                self.lineEdit_y.textChanged.disconnect(self.conn_func)
                self.lineEdit_x.setText(str(round(x, 2)))
                self.lineEdit_y.setText(str(round(y, 2)))
                self.lineEdit_x.textChanged.connect(self.conn_func)
                self.lineEdit_y.textChanged.connect(self.conn_func)
            except:
                pass

    @staticmethod
    def from_cartesian_to_polar(x: float, y: float) -> (float, float):
        r = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        O = math.acos(x/r) * (180/math.pi)
        return r, O

    @staticmethod
    def from_polar_to_cartesian(O: float, r: float) -> (float, float):
        x = r * math.cos(O * math.pi / 180)
        y = r * math.sin(O * math.pi / 180)
        return x, y

    def ok(self):
        self.point = [(float(self.lineEdit_x.text())+100)*2, 200 - float(self.lineEdit_y.text())*2]
        print(self.point)
        self.close()

