# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(474, 345)
        MainWindow.setStyleSheet("background-color: white\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: white")
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 20, 271, 151))
        font = QtGui.QFont()
        font.setFamily("hAndy")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("background: transparent\n"
"")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 100, 351, 71))
        font = QtGui.QFont()
        font.setFamily("hAndy")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background: transparent;\n"
"")
        self.label_2.setObjectName("label_2")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(130, 220, 231, 101))
        font = QtGui.QFont()
        font.setFamily("hAndy")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.start.setFont(font)
        self.start.setStyleSheet("border-radius: 50px;\n"
"background-color: white;\n"
"border: 5px solid #0091fa;")
        self.start.setObjectName("start")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 161, 16))
        font = QtGui.QFont()
        font.setFamily("hAndy")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 180, 101, 161))
        font = QtGui.QFont()
        font.setFamily("hAndy")
        self.label_4.setFont(font)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Подбор фильма"))
        self.label.setText(_translate("MainWindow", "Готовы выбрать "))
        self.label_2.setText(_translate("MainWindow", "подходящий фильм?"))
        self.start.setText(_translate("MainWindow", "Начать"))
        self.label_3.setText(_translate("MainWindow", "Выполнил Глушин Никита"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
