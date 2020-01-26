# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_gif_form(object):
    def setupUi(self, gif_form):
        gif_form.setObjectName("gif_form")
        gif_form.resize(375, 289)
        gif_form.setStyleSheet("background-color: white;")
        self.label = QtWidgets.QLabel(gif_form)
        self.label.setGeometry(QtCore.QRect(-10, 50, 391, 241))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(gif_form)
        self.label_2.setGeometry(QtCore.QRect(30, 5, 491, 21))
        font = QtGui.QFont()
        font.setFamily("hAndy")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background: transparent")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(gif_form)
        self.label_3.setGeometry(QtCore.QRect(110, 20, 251, 31))
        font = QtGui.QFont()
        font.setFamily("hAndy")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background: transparent")
        self.label_3.setObjectName("label_3")

        self.retranslateUi(gif_form)
        QtCore.QMetaObject.connectSlotsByName(gif_form)

    def retranslateUi(self, gif_form):
        _translate = QtCore.QCoreApplication.translate
        gif_form.setWindowTitle(_translate("gif_form", "Загрузка"))
        self.label_2.setText(_translate("gif_form", "Мы ищем для Вас лучший фильм."))
        self.label_3.setText(_translate("gif_form", "Ещё секунду..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gif_form = QtWidgets.QWidget()
    ui = Ui_gif_form()
    ui.setupUi(gif_form)
    gif_form.show()
    sys.exit(app.exec_())
