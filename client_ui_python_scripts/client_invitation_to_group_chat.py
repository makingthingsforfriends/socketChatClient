# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_invitation_to_group_chat.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(210, 125)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.label.setObjectName("label")
        self.senderLabel = QtWidgets.QLabel(Dialog)
        self.senderLabel.setGeometry(QtCore.QRect(60, 20, 47, 13))
        self.senderLabel.setObjectName("senderLabel")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 121, 16))
        self.label_3.setObjectName("label_3")
        self.roomNoLabel = QtWidgets.QLabel(Dialog)
        self.roomNoLabel.setGeometry(QtCore.QRect(150, 50, 47, 13))
        self.roomNoLabel.setObjectName("roomNoLabel")
        self.AcceptButton = QtWidgets.QPushButton(Dialog)
        self.AcceptButton.setGeometry(QtCore.QRect(110, 80, 75, 23))
        self.AcceptButton.setObjectName("AcceptButton")
        self.RejectButton = QtWidgets.QPushButton(Dialog)
        self.RejectButton.setGeometry(QtCore.QRect(20, 80, 75, 23))
        self.RejectButton.setObjectName("RejectButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Client:"))
        self.senderLabel.setText(_translate("Dialog", "[Client]"))
        self.label_3.setText(_translate("Dialog", "Invites you to join room:"))
        self.roomNoLabel.setText(_translate("Dialog", "[roomNo]"))
        self.AcceptButton.setText(_translate("Dialog", "Accept"))
        self.RejectButton.setText(_translate("Dialog", "Reject"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
