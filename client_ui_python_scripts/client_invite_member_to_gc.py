# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_invite_member_to_gc.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(160, 325)
        self.connectedClientsNotInGCList = QtWidgets.QListWidget(Form)
        self.connectedClientsNotInGCList.setGeometry(QtCore.QRect(10, 40, 141, 231))
        self.connectedClientsNotInGCList.setObjectName("connectedClientsNotInGCList")
        self.inviteButton = QtWidgets.QPushButton(Form)
        self.inviteButton.setGeometry(QtCore.QRect(10, 280, 71, 31))
        self.inviteButton.setObjectName("inviteButton")
        self.CancelButton = QtWidgets.QPushButton(Form)
        self.CancelButton.setGeometry(QtCore.QRect(80, 280, 71, 31))
        self.CancelButton.setObjectName("CancelButton")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 211, 16))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.inviteButton.setText(_translate("Form", "Invite"))
        self.CancelButton.setText(_translate("Form", "Cancel"))
        self.label_5.setText(_translate("Form", "Connected Clients:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())