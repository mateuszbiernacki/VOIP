# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Client\gui\qt_des\call_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.end_button = QtWidgets.QPushButton(Dialog)
        self.end_button.setGeometry(QtCore.QRect(160, 240, 75, 23))
        self.end_button.setObjectName("end_button")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 100, 61, 21))
        self.label.setObjectName("label")
        self.login_label = QtWidgets.QLabel(Dialog)
        self.login_label.setGeometry(QtCore.QRect(130, 100, 121, 21))
        self.login_label.setObjectName("login_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.end_button.setText(_translate("Dialog", "End"))
        self.label.setText(_translate("Dialog", "Call with"))
        self.login_label.setText(_translate("Dialog", "LOGIN"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())