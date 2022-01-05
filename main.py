import time
import threading
import math
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter, QDragEnterEvent, QDropEvent, QMouseEvent, QKeyEvent, QWheelEvent
from window import Ui_MainWindow
from add_point_dlg import Ui_Dialog
from polar_figures import MyLine, MyEllipse


class Polar(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        self.close_ = False
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/main_icon.png'))
        self.add_functions()
        self.pen = QtGui.QPen(QtCore.Qt.green)
        self.pen.setWidth(2)
        self.brush = QtGui.QBrush(QtCore.Qt.black)

        self.draw_oxoy()
        self.check_pos_thread = threading.Thread(target=self.check_mouse_pos)
        self.check_pos_thread.start()


    def add_functions(self):
        self.pushButton_clear.clicked.connect(lambda: self.clear())
        self.pushButton_check.clicked.connect(lambda: self.check())

    def clear(self):
        self.graphicsView.grScene.clear()
        self.graphicsView.grScene.points = []
        self.graphicsView.grScene.lines = []
        self.draw_oxoy()

    def check_mouse_pos(self):
        while not self.close_:
            x = round((self.graphicsView.grScene.mouse_x / 2) - 100, 2)
            y = round(-((self.graphicsView.grScene.mouse_y / 2) - 100), 2)
            self.label_m_x.setText(str(x))
            self.label_m_y.setText(str(y))
            time.sleep(0.01)

    def draw_oxoy(self):
        ox = QtCore.QLineF(QtCore.QPointF(0, 200), QtCore.QPointF(400, 200))
        self.graphicsView.grScene.addLine(ox, self.pen)
        oy = QtCore.QLineF(QtCore.QPointF(200, 0), QtCore.QPointF(200, 400))
        self.graphicsView.grScene.addLine(oy, self.pen)
        l = QtCore.QLineF(QtCore.QPointF(0, 195), QtCore.QPointF(0, 205))
        self.graphicsView.grScene.addLine(l, self.pen)
        l = QtCore.QLineF(QtCore.QPointF(100, 195), QtCore.QPointF(100, 205))
        self.graphicsView.grScene.addLine(l, self.pen)
        l = QtCore.QLineF(QtCore.QPointF(300, 195), QtCore.QPointF(300, 205))
        self.graphicsView.grScene.addLine(l, self.pen)
        l = QtCore.QLineF(QtCore.QPointF(400, 195), QtCore.QPointF(400, 205))
        self.graphicsView.grScene.addLine(l, self.pen)
        l = QtCore.QLineF(QtCore.QPointF(195, 0), QtCore.QPointF(205, 0))
        self.graphicsView.grScene.addLine(l, self.pen)
        l = QtCore.QLineF(QtCore.QPointF(195, 100), QtCore.QPointF(205, 100))
        self.graphicsView.grScene.addLine(l, self.pen)
        l = QtCore.QLineF(QtCore.QPointF(195, 300), QtCore.QPointF(205, 300))
        self.graphicsView.grScene.addLine(l, self.pen)
        l = QtCore.QLineF(QtCore.QPointF(195, 400), QtCore.QPointF(205, 400))
        self.graphicsView.grScene.addLine(l, self.pen)
        t = self.graphicsView.grScene.addText('-100')
        t.moveBy(-15, 170)
        t = self.graphicsView.grScene.addText('-50')
        t.moveBy(85, 170)
        t = self.graphicsView.grScene.addText('-100')
        t.moveBy(210, 387)
        t = self.graphicsView.grScene.addText('-50')
        t.moveBy(210, 290)
        t = self.graphicsView.grScene.addText('100')
        t.moveBy(385, 170)
        t = self.graphicsView.grScene.addText('50')
        t.moveBy(290, 170)
        t = self.graphicsView.grScene.addText('100')
        t.moveBy(210, -12)
        t = self.graphicsView.grScene.addText('50')
        t.moveBy(210, 90)
        t = self.graphicsView.grScene.addText('0')
        t.moveBy(200, 180)

        #Create greed
        # pen = QtGui.QPen(QtCore.Qt.lightGray)
        #
        # pen.setCosmetic(True)
        # for x in range(0, 410, 10):
        #     line = self.graphicsView.grScene.addLine(x, 0, x, 600, pen)
        #     line.setZValue(-10)
        # for y in range(0, 410, 10):
        #     line = self.graphicsView.grScene.addLine(0, y, 600, y, pen)
        #     line.setZValue(-10)



        # pen = QtGui.QPen(QtCore.Qt.black)
        # brush = QtGui.QBrush(QtCore.Qt.black)
        # item = MyEllipse(100, 100, 10, 10)
        # item.setAcceptHoverEvents(True)
        # item.setPen(pen)
        # item.setBrush(brush)
        # print(item.x(), item.y())
        # self.grScene.addItem(item)

    def check(self):
        data = {}
        for angle in range(360):
            angle_line = [0, 0], [100 * math.cos((angle * math.pi)/180), 100 * math.sin((angle * math.pi)/180)]
            for line in self.graphicsView.grScene.lines:
                ret = self.intersect([[line.normal_x1, line.normal_y1], [line.normal_x2, line.normal_y2]], angle_line, angle)
                try:
                    old_data = data[str(angle)]
                    if old_data == 'None':
                        old_data = None
                    print('old data: ', old_data)
                except KeyError:
                    old_data = None

                # print(f'ret: {ret}')
                if ret is not None and old_data is not None:
                        print(angle,old_data)
                        new_data = {f'{angle}': f'{old_data} {math.sqrt(math.pow(ret[0],2) + math.pow(ret[1],2))}'}
                        # new_data = {f'{angle}': f'{ret}'}
                elif old_data is None:
                    if ret is not None:
                        new_data = {f'{angle}': f'{math.sqrt(math.pow(ret[0],2) + math.pow(ret[1],2))}'}
                    else:
                        new_data = {f'{angle}': f'{ret}'}
                data.update(new_data)
                if ret is not None and self.checkBox_visualize.isChecked():
                    pen = QtGui.QPen(QtCore.Qt.black)
                    line_item = MyLine(200, 200, 200+ret[0]*2, 200-ret[1]*2, angle=str(angle))
                    line_item.setAcceptHoverEvents(True)
                    line_item.setPen(pen)
                    self.graphicsView.grScene.addItem(line_item)
                # new_data = {f'{angle}': f'{ret}     AngleLine:{angle_line[1]}     Line:{[[line.normal_x1, line.normal_y1], [line.normal_x2, line.normal_y2]]}'}

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(data)

    def intersect(self, line1, line2, angle):
        x1_1, y1_1 = line1[0][0], line1[0][1]
        x1_2, y1_2 = line1[1][0], line1[1][1]
        x2_1, y2_1 = line2[0][0], line2[0][1]
        x2_2, y2_2 = line2[1][0], line2[1][1]

        def point(x, y, angle):
            if min(x1_1, x1_2) <= x <= max(x1_1, x1_2) and min(y1_1, y1_2) <= y <= max(y1_1, y1_2) and\
               min(x2_1, x2_2) <= x <= max(x2_1, x2_2) and min(y2_1, y2_2) <= y <= max(y2_1, y2_2):
                # if angle == 90:
                #     print('90', x, y)
                # elif angle == 270:
                #     print('270', x, y)
                return [x, y]
            else:
                # print(f'Точки пересечения отрезков нет. {angle}')
                return None

        A1 = y1_1 - y1_2
        B1 = x1_2 - x1_1
        C1 = x1_1 * y1_2 - x1_2 * y1_1
        A2 = y2_1 - y2_2
        B2 = x2_2 - x2_1
        C2 = x2_1 * y2_2 - x2_2 * y2_1

        if B1 * A2 - B2 * A1 and A1:
            y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
            x = (-C1 - B1 * y) / A1
            ret = point(x, y, angle)
            return ret
        elif B1 * A2 - B2 * A1 and A2:
            y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
            x = (-C2 - B2 * y) / A2
            ret = point(x, y, angle)
            return ret
        else:
            print('Точки пересечения отрезков нет, отрезки ||.')
            return None

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_ = True
        super(Polar, self).closeEvent(a0)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Polar()
    w.show()
    sys.exit(app.exec_())
