import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsView, QGraphicsSceneMouseEvent
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QRect, QLine
from polar_figures import MyLine, MyEllipse
from polar_dialogs import AddPointDialog


class graphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self,centralwidget, parent=None):
        super(graphicsScene, self).__init__(parent)
        self.centralwidget = centralwidget
        self.points = []
        self.lines = []
        self.mouse_x = 0
        self.mouse_y = 0
        self.gridSize = 20
        self.gridSquares = 5
        self.start_point = []
        self.end_point = []
        self.initAssets()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super(graphicsScene, self).mouseMoveEvent(event)
        position = QtCore.QPointF(event.scenePos())
        self.mouse_x = position.x()
        self.mouse_y = position.y()

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")
        self._color_state = QColor("#ccc")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidthF(0.25)

        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidthF(0.5)

    def clear(self) -> None:
        super().clear()
        self.points = []

    def contextMenuEvent(self, event):
        sp = event.scenePos().toPoint()
        item = self.itemAt(
            sp,
            QtGui.QTransform())
        print(item)
        if isinstance(item, MyEllipse):
            menu = QtWidgets.QMenu()
            removeAction = menu.addAction("Remove")
            removeAction.triggered.connect(lambda: self._remove_action(item))
            connectAction = menu.addAction("Connect")
            connectAction.triggered.connect(lambda: self._connect_action(item))
            moveAction = menu.addAction("Move")
            moveAction.triggered.connect(lambda: self._move_action(item))
            selectedAction = menu.exec(event.screenPos())

        elif isinstance(item, MyLine):
            menu = QtWidgets.QMenu()
            removeAction = menu.addAction("Remove")
            removeAction.triggered.connect(lambda: self._remove_line_action(item))
            selectedAction = menu.exec(event.screenPos())

        elif item is None:
            menu = QtWidgets.QMenu()
            addPoint = menu.addAction("Add point")
            addPoint.triggered.connect(lambda: self.add_point_action())
            # markAction = menu.addAction("Mark")
            selectedAction = menu.exec(event.screenPos())

        else:
            pass

    def _remove_line_action(self, item):
        self.lines.remove(item)
        self.removeItem(item)
        for item_ in self.items():
            if isinstance(item_, MyEllipse):
                try:
                    item_.finish_line.remove(item)
                except:
                    try:
                        item_.start_line.remove(item)
                    except:
                        pass

    def _remove_action(self, item):
        self.points.remove(item)
        self.removeItem(item)
        # print("Item", item.x_, item.y_)
        for line in self.lines:
            if line.x1 == item.center_x or line.x2 == item.center_x:
                self.removeItem(line)
            if line.y1 == item.center_y or line.y2 == item.center_y:
                self.removeItem(line)
        for item_ in self.items():
            if isinstance(item_, MyEllipse):
                for line in item.finish_line:
                    if line.x1 == item.center_x or line.x2 == item.center_x:
                        # print(item_.finish_line,'\n', line)
                        item_.start_line.remove(line)
                    elif line.y1 == item.center_y or line.y2 == item.center_y:
                        item_.start_line.remove(line)
                for line in item.start_line:
                    if line.x1 == item.center_x or line.x2 == item.center_x:
                        item_.finish_line.remove(line)
                    elif line.y1 == item.center_y or line.y2 == item.center_y:
                        item_.finish_line.remove(line)
            # print(line.x1, line.x2, line.y1, line.y2)

    def _connect_action(self, item):
        pen = QtGui.QPen(QtCore.Qt.black)
        if len(self.start_point) == 0:
            self.start_point = [item.center_x, item.center_y, item]
            item.chose_item()
            print('start_point: ', self.start_point)
        elif len(self.end_point) == 0 and len(self.start_point) != 0:
            self.end_point = [item.center_x, item.center_y, item]
            print('end_point: ', self.end_point)
            self.line_item = MyLine(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1])
            self.line_item .setAcceptHoverEvents(True)
            self.line_item .setPen(pen)
            self.addItem(self.line_item)
            self.lines.append(self.line_item)
            self.end_point[2].add_finish_line(self.line_item)
            self.start_point[2].add_start_line(self.line_item)
            # item.add_start_line(self.line_item )
            self.start_point[2].unchose_item()
            self.start_point = []
            self.end_point = []


        # if item.start_line is None or item.finish_line is None and len(self.points) > 0 and self.points[-1] is not item:
        #     print(item)
        #     line_item = MyLine(self.points[-1].center_x, self.points[-1].center_y, item.center_x, item.center_y)
        #     line_item.setAcceptHoverEvents(True)
        #     line_item.setPen(pen)
        #     self.addItem(line_item)
        #     self.lines.append(line_item)
        #     self.points[-1].add_finish_line(line_item)
        #     item.add_start_line(line_item)

        # elif item.start_line is None or item.finish_line is None and len(self.points) > 0 and self.points[-1] is item:
        #     print('item')
        #     line_item = MyLine(item.center_x, item.center_y, self.points[0].center_x, self.points[0].center_y)
        #     line_item.setAcceptHoverEvents(True)
        #     line_item.setPen(pen)
        #     self.addItem(line_item)
        #     self.lines.append(line_item)
        #     item.add_finish_line(line_item)
        #     self.points[0].add_start_line(line_item)
        #
        # else:
        #     QtWidgets.QMessageBox.warning(self.centralwidget, "Ошибка",
        #                                   "К этой точке уже подключены две точки",
        #                                   QtWidgets.QMessageBox.Ok)
    def _move_action(self, item):
        dlg = AddPointDialog()
        dlg.setWindowTitle('Move point')
        dlg.show()
        dlg.exec()
        if dlg.point[0] != None:
            item.setPos_(dlg.point[0], dlg.point[1])

    def add_point_action(self):
        # dlg = AddPointWidget()
        dlg = AddPointDialog()
        dlg.show()
        dlg.exec()
        if dlg.point[0] != None:
            pen = QtGui.QPen(QtCore.Qt.black)
            brush = QtGui.QBrush(QtCore.Qt.black)
            item = MyEllipse(dlg.point[0], dlg.point[1], 4, 4)
            item.setAcceptHoverEvents(True)
            item.setPen(pen)
            item.setBrush(brush)
            self.addItem(item)
            # if len(self.points) > 0:
            #     line_item = MyLine(self.points[-1].center_x, self.points[-1].center_y, item.center_x, item.center_y)
            #     line_item.setAcceptHoverEvents(True)
            #     line_item.setPen(pen)
            #     self.addItem(line_item)
            #     self.lines.append(line_item)
            #     self.points[-1].add_finish_line(line_item)
            #     item.add_start_line(line_item)
            self.points.append(item)

    def drawBackground(self, painter:QPainter, rect:QRect):
        """Draw background scene grid"""
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if (x % (self.gridSize*self.gridSquares) != 0):
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if (y % (self.gridSize*self.gridSquares) != 0): lines_light.append(QLine(left, y, right, y))
            else: lines_dark.append(QLine(left, y, right, y))


        # draw the lines
        painter.setPen(self._pen_light)
        try: painter.drawLines(*lines_light)                    # supporting PyQt5
        except TypeError: painter.drawLines(lines_light)        # supporting PySide2

        painter.setPen(self._pen_dark)
        try: painter.drawLines(*lines_dark)                     # supporting PyQt5
        except TypeError: painter.drawLines(lines_dark)         # supporting PySide2