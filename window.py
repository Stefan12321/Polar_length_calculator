# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QDMGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_check = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_check.setObjectName("pushButton_check")
        self.verticalLayout_2.addWidget(self.pushButton_check)
        self.pushButton_clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.verticalLayout_2.addWidget(self.pushButton_clear)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_m_x = QtWidgets.QLabel(self.centralwidget)
        self.label_m_x.setMinimumSize(QtCore.QSize(50, 0))
        self.label_m_x.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_m_x.setText("")
        self.label_m_x.setObjectName("label_m_x")
        self.horizontalLayout.addWidget(self.label_m_x)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_m_y = QtWidgets.QLabel(self.centralwidget)
        self.label_m_y.setMinimumSize(QtCore.QSize(50, 0))
        self.label_m_y.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_m_y.setText("")
        self.label_m_y.setObjectName("label_m_y")
        self.horizontalLayout_2.addWidget(self.label_m_y)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.checkBox_visualize = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_visualize.setObjectName("checkBox_visualize")
        self.verticalLayout_2.addWidget(self.checkBox_visualize)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 850, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Polar"))
        self.pushButton_check.setText(_translate("MainWindow", "Check"))
        self.pushButton_clear.setText(_translate("MainWindow", "Clear"))
        self.label.setText(_translate("MainWindow", "Mouse X:"))
        self.label_2.setText(_translate("MainWindow", "Mouse Y:"))
        self.checkBox_visualize.setText(_translate("MainWindow", "Visualize"))
from polar_graphicsView import QDMGraphicsView