# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_invitation_to_priv_chat.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(207, 128)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 50, 51, 16))
        self.label.setObjectName("label")
        self.senderLabel = QtWidgets.QLabel(Dialog)
        self.senderLabel.setGeometry(QtCore.QRect(80, 50, 47, 13))
        self.senderLabel.setObjectName("senderLabel")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 141, 16))
        self.label_3.setObjectName("label_3")
        self.AcceptInvitationButton = QtWidgets.QPushButton(Dialog)
        self.AcceptInvitationButton.setGeometry(QtCore.QRect(110, 80, 75, 23))
        self.AcceptInvitationButton.setObjectName("AcceptInvitationButton")
        self.RejectInvitationButton = QtWidgets.QPushButton(Dialog)
        self.RejectInvitationButton.setGeometry(QtCore.QRect(20, 80, 75, 23))
        self.RejectInvitationButton.setObjectName("RejectInvitationButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Private chat invitation"))
        self.label.setText(_translate("Dialog", "From user:"))
        self.senderLabel.setText(_translate("Dialog", "[User]"))
        self.label_3.setText(_translate("Dialog", "Invitation to private chat!"))
        self.AcceptInvitationButton.setText(_translate("Dialog", "Accept"))
        self.RejectInvitationButton.setText(_translate("Dialog", "Reject"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())