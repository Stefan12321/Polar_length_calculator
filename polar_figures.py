import math
import time

from PyQt5 import QtCore, QtGui, QtWidgets

DEBUG = False


class MyLine(QtWidgets.QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, angle=''):
        super(MyLine, self).__init__(x1, y1, x2, y2)
        self.angle = angle
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.normal_x1 = (x1 / 2) - 100
        self.normal_y1 = -((y1 / 2) - 100)
        self.normal_x2 = (x2 / 2) - 100
        self.normal_y2 = -((y2 / 2) - 100)
        self.setZValue(-10)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super(MyLine, self).hoverEnterEvent(event)
        pen = QtGui.QPen(QtCore.Qt.green)
        self.setPen(pen)
        self.setToolTip(f'X1: {self.normal_x1}\nY1: {self.normal_y1}\nX2: {self.normal_x2}\nY2: {self.normal_y2}\n'
                        f'Len: {math.sqrt(math.pow(self.normal_x2 - self.normal_x1,2) + math.pow(self.normal_y2 - self.normal_y1,2))}' +
                       ('' if self.angle == '' else f'\nAngle: {self.angle}'))

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super(MyLine, self).hoverLeaveEvent(event)
        pen = QtGui.QPen(QtCore.Qt.black)
        self.setPen(pen)

    def setLine(self, *__args) -> None:
        super(MyLine, self).setLine(*__args)
        print('Add line ', __args)
        self.x1 = __args[0]
        self.y1 = __args[1]
        self.x2 = __args[2]
        self.y2 = __args[3]
        self.normal_x1 = (self.x1 / 2) - 100
        self.normal_y1 = -((self.y1 / 2) - 100)
        self.normal_x2 = (self.x2 / 2) - 100
        self.normal_y2 = -((self.y2 / 2) - 100)


class MyEllipse(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x, y, w, h):
        self.center_x = x
        self.center_y = y
        self.width = w
        self.height = h
        x -= (self.width/2)
        y -= (self.height/2)
        super(MyEllipse, self).__init__(0, 0, w, h)
        self.x_ = x
        self.y_ = y
        self.setPos(self.x_, self.y_)
        print('orig_position', self.scenePos())
        # print(self.x_, self.y_, self.pos().x())
        self.setAcceptHoverEvents(True)
        self.start_line = []
        self.finish_line = []
        self.start = 0
        self.end = 1

    def add_start_line(self, line):
        self.start_line.append(line)

    def add_finish_line(self, line):
        self.finish_line.append(line)

    def chose_item(self):
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        self.setPen(pen)
        self.setBrush(brush)

    def unchose_item(self):
        pen = QtGui.QPen(QtCore.Qt.black)
        brush = QtGui.QBrush(QtCore.Qt.black)
        self.setPen(pen)
        self.setBrush(brush)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super(MyEllipse, self).hoverEnterEvent(event)
        pen = QtGui.QPen(QtCore.Qt.green)
        self.setPen(pen)
        # print(self.pos().x(), self.pos().y())
        if not DEBUG:
            self.setToolTip(f'X: {(self.center_x / 2) - 100}\nY: {-((self.center_y / 2) - 100)}')
        else:
            self.setToolTip(f'X: {(self.center_x / 2) - 100}\nY: {-((self.center_y / 2) - 100)}\n{self.x_} {self.y_}\n'
                            f'Start lines: {self.start_line}\n Finish lines: {self.finish_line}')
        # print('enter')
        # print(self.start_line, self.finish_line)

    # mouse click event
    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            super(MyEllipse, self).mousePressEvent(event)  # Костыль
        # self.start = time.time()

    def mouseMoveEvent(self, event):
        super(MyEllipse, self).mouseMoveEvent(event)
        print('button:', event.button())
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()
        # print(f'orig_cursor_position: {orig_cursor_position}\nupdated_cursor_position: {updated_cursor_position}')

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()

        self.setPos(updated_cursor_x, updated_cursor_y)
        self.x_ = self.scenePos().x()
        self.y_ = self.scenePos().y()
        self.center_x = self.scenePos().x() + (self.width / 2)
        self.center_y = self.scenePos().y() + (self.height / 2)
        # print(f'center_x: {self.center_x}\ncenter_y: {self.center_y}\nPos: {self.scenePos()}')
        # print(f'finish_line: {self.finish_line}\nstart_line: {self.start_line}')
        if len(self.start_line) > 0:
            for line in self.start_line:
                line.x1 = self.center_x
                line.y1 = self.center_y
                line.setLine(line.x1, line.y1, line.x2, line.y2)

        if len(self.finish_line) > 0:
            for line in self.finish_line:
                line.x2 = self.center_x
                line.y2 = self.center_y
                line.setLine(line.x1, line.y1, line.x2, line.y2)

    def mouseReleaseEvent(self, event):
        # super(MyEllipse, self).mouseReleaseEvent(event)
        self.end = time.time()
        # print(self.end,'\n', self.start)
        if self.end - self.start < 0.3:
            print('aaaaass')
        # print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))
        # self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super(MyEllipse, self).hoverLeaveEvent(event)
        pen = QtGui.QPen(QtCore.Qt.black)
        self.setPen(pen)

    def setPos_(self, x: float, y: float) -> None:
        self.center_x = x
        self.center_y = y
        x -= (self.width / 2)
        y -= (self.height / 2)
        self.x_ = x
        self.y_ = y
        if len(self.start_line) > 0:
            for line in self.start_line:
                line.x1 = self.center_x
                line.y1 = self.center_y
                line.setLine(line.x1, line.y1, line.x2, line.y2)

        if len(self.finish_line) > 0:
            for line in self.finish_line:
                line.x2 = self.center_x
                line.y2 = self.center_y
                line.setLine(line.x1, line.y1, line.x2, line.y2)
        self.setPos(x, y)

    def setPos(self, *__args) -> None:
        super(MyEllipse, self).setPos(*__args)
        # print('POS: ',__args)

    # def connect_line(self):
    #     line_item = MyLine(self.center_x, self.center_y, )
    #     line_item.setAcceptHoverEvents(True)
    #     line_item.setPen(pen)
    #     self.grScene.addItem(line_item)
    #     self.grScene.lines.append(line_item)
    #     self.grScene.points[-1].add_finish_line(line_item)
    #     item.add_start_line(line_item)



    # def contextMenuEvent(self, event):
    #     menu = QtWidgets.QMenu()
    #     removeAction = menu.addAction("Remove")
    #     markAction = menu.addAction("Mark")
    #     selectedAction = menu.exec(event.screenPos())