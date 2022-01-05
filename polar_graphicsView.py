from PyQt5.QtWidgets import QGraphicsView, QApplication, QGraphicsSceneMouseEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, Qt, QEvent, QPointF, QRectF
from PyQt5.QtGui import QPainter, QDragEnterEvent, QDropEvent, QMouseEvent, QKeyEvent, QWheelEvent
from PyQt5 import QtGui
from main import MyLine, MyEllipse
from polar_scene import graphicsScene


class MouseFlag(Qt.MouseEventFlags):
    def __init__(self):
        super(MouseFlag, self).__init__(self)
        self.mid_key = True


class MouseEvent(QMouseEvent):
    def __init__(self, *__args):
        self.mid_key = True
        super(MouseEvent, self).__init__(*__args)

    def source(self) -> QtCore.Qt.MouseEventSource:
        # super(MouseEvent, self).source()
        return QtCore.Qt.MouseEventSource(2)


class QDMGraphicsView(QGraphicsView):
    def __init__(self, parent: 'QWidget'=None):
        super(QDMGraphicsView, self).__init__(parent)
        self.centralwidget = parent
        self.grScene = graphicsScene(self.centralwidget)
        self.setScene(self.grScene)
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [10, 15]

    def mousePressEvent(self, event:  QMouseEvent):
        super(QDMGraphicsView, self).mousePressEvent(event)
        sp = event.localPos().toPoint()
        item = self.itemAt(
            sp
        )
        # print(item)
        if event.button() == QtCore.Qt.LeftButton and not isinstance(item, MyEllipse) and event.source() != 2:
           self.left_button_press(event)
        # elif event.button() == QtCore.Qt.LeftButton and isinstance(item, MyEllipse):
        #     pen = QtGui.QPen(QtCore.Qt.black)
        #     if len(self.grScene.points) > 0:
        #         line_item = MyLine(self.grScene.points[-1].x_ + 4, self.grScene.points[-1].y_ + 4, item.x_ + 4,
        #                            item.y_ + 4)
        #         line_item.setAcceptHoverEvents(True)
        #         line_item.setPen(pen)
        #         self.grScene.addItem(line_item)
        #         self.grScene.lines.append(line_item)
        #         self.grScene.points[-1].add_finish_line(line_item)
        #         item.add_start_line(line_item)
        if event.button() == QtCore.Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        else:
            # print('else')
            super(QDMGraphicsView, self).mousePressEvent(event)
            
    def mouseReleaseEvent(self, event: QMouseEvent):

        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        else:
            # print('else')
            super(QDMGraphicsView, self).mouseReleaseEvent(event)

    def left_button_press(self, event:  QMouseEvent):
        # self.grScene.mousePressEvent(event)
        position = event.localPos().toPoint()
        position = self.mapToScene(position)
        # print(position)
        # print("pressed here: " + str(position.x()) + ", " + str(position.y()))
        pen = QtGui.QPen(QtCore.Qt.black)
        brush = QtGui.QBrush(QtCore.Qt.black)
        item = MyEllipse(position.x(), position.y(), 4, 4)
        print(position.x(), position.y(), '\n', item.x_, item.y_)
        item.setAcceptHoverEvents(True)
        item.setPen(pen)
        item.setBrush(brush)
        self.grScene.addItem(item)
        # if len(self.grScene.points) > 0:
        #     line_item = MyLine(self.grScene.points[-1].center_x, self.grScene.points[-1].center_y, item.center_x, item.center_y)
        #     line_item.setAcceptHoverEvents(True)
        #     line_item.setPen(pen)
        #     self.grScene.addItem(line_item)
        #     self.grScene.lines.append(line_item)
        #     self.grScene.points[-1].add_finish_line(line_item)
        #     item.add_start_line(line_item)
        self.grScene.points.append(item)

    # def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

    def middleMouseButtonPress(self, event:  QMouseEvent):
        releaseEvent = MouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        # print(self.grScene.points)
        # self.grScene.mouseReleaseEvent(releaseEvent)
        self.mouseReleaseEvent(releaseEvent)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = MouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        # print('fake: ', fakeEvent.source())
        self.mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event: QMouseEvent):
        """When Middle mouse button was released"""
        fakeEvent = MouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        self.mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    # def left_button_press(self, event:  QMouseEvent):
    #     position = QtCore.QPointF(event.scenePos())
    #     # print("pressed here: " + str(position.x()) + ", " + str(position.y()))
    #     pen = QtGui.QPen(QtCore.Qt.black)
    #     brush = QtGui.QBrush(QtCore.Qt.black)
    #     item = MyEllipse(position.x(), position.y(), 4, 4)
    #     item.setAcceptHoverEvents(True)
    #     item.setPen(pen)
    #     item.setBrush(brush)
    #     self.addItem(item)
    #     if len(self.points) > 0:
    #         line_item = MyLine(self.points[-1].x_ + 4, self.points[-1].y_ + 4, item.x_ + 4, item.y_ + 4)
    #         line_item.setAcceptHoverEvents(True)
    #         line_item.setPen(pen)
    #         self.addItem(line_item)
    #         self.lines.append(line_item)
    #         self.points[-1].add_finish_line(line_item)
    #         item.add_start_line(line_item)
    #     self.points.append(item)
    #
    # def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     super(QDMGraphicsView, self).mouseMoveEvent(event)
    #     position = QtCore.QPointF(event.scenePos())
    #     self.mouse_x = position.x()
    #     self.mouse_y = position.y()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:

        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:

            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep
        print('zoomFactor: ', zoomFactor)
        print('zoom: ', self.zoom)
        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
