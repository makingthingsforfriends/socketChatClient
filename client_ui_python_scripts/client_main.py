# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 800)
        self.connected_clients_list = QtWidgets.QListWidget(Form)
        self.connected_clients_list.setGeometry(QtCore.QRect(10, 30, 251, 192))
        self.connected_clients_list.setObjectName("connected_clients_list")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label.setObjectName("label")
        self.oneToOneChatButton = QtWidgets.QPushButton(Form)
        self.oneToOneChatButton.setGeometry(QtCore.QRect(280, 30, 71, 31))
        self.oneToOneChatButton.setObjectName("oneToOneChatButton")
        self.chat_rooms_list = QtWidgets.QListWidget(Form)
        self.chat_rooms_list.setGeometry(QtCore.QRect(10, 250, 251, 151))
        self.chat_rooms_list.setObjectName("chat_rooms_list")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 230, 121, 16))
        self.label_2.setObjectName("label_2")
        self.CreateGCButton = QtWidgets.QPushButton(Form)
        self.CreateGCButton.setGeometry(QtCore.QRect(280, 250, 71, 31))
        self.CreateGCButton.setObjectName("CreateGCButton")
        self.JoinButton = QtWidgets.QPushButton(Form)
        self.JoinButton.setGeometry(QtCore.QRect(280, 290, 71, 31))
        self.JoinButton.setObjectName("JoinButton")
        self.CloseButton = QtWidgets.QPushButton(Form)
        self.CloseButton.setGeometry(QtCore.QRect(280, 400, 71, 31))
        self.CloseButton.setObjectName("CloseButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Connected Clients"))
        self.oneToOneChatButton.setText(_translate("Form", "1:1 Chat"))
        self.label_2.setText(_translate("Form", "Chat rooms (Group chat)"))
        self.CreateGCButton.setText(_translate("Form", "Create"))
        self.JoinButton.setText(_translate("Form", "Join"))
        self.CloseButton.setText(_translate("Form", "Close"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
