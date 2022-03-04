import ssl
import sys
import random
import threading
from collections import defaultdict

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from utils import *
from client_ui_python_scripts import client_main, client_groupchat, client_chat, client_setup, \
    client_invitation_to_priv_chat, client_invite_member_to_gc, client_invitation_to_group_chat


def show_error(error_type, message):
    errorDialog = QtWidgets.QMessageBox()
    errorDialog.setText(message)
    errorDialog.setWindowTitle(error_type)
    errorDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
    errorDialog.exec_()


stop_thread = False


class Client(object):

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.nickname = ""
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.messages = []
        self.current_roomNo = 0
        self.mainWindow = QtWidgets.QMainWindow()

        # setting up client setup widget
        self.setupWidget = QtWidgets.QWidget(self.mainWindow)
        self.setupUI = client_setup.Ui_Welcome()
        self.setupUI.setupUi(self.setupWidget)
        self.setupUI.buttonBox.accepted.connect(self.btn_ok_clicked)
        self.setupUI.buttonBox.rejected.connect(self.btn_cancel_clicked)

        # setting up client home ui
        self.homeWidget = QtWidgets.QWidget(self.mainWindow)
        self.homeWidget.setHidden(True)
        self.clientHomeUI = client_main.Ui_Form()
        self.clientHomeUI.setupUi(self.homeWidget)
        self.clientHomeUI.CloseButton.clicked.connect(self.btn_cancel_clicked)

        # setting up invitation message
        self.invitationDialog = QtWidgets.QDialog(self.mainWindow)
        self.invitationDialog.setHidden(True)
        self.invitationDialogUI = client_invitation_to_priv_chat.Ui_Dialog()
        self.invitationDialogUI.setupUi(self.invitationDialog)

        # setting up private chat widget and hide it
        self.privateChatWidget = QtWidgets.QWidget(self.mainWindow)
        self.privateChatWidget.setHidden(True)
        self.privateChatUI = client_chat.Ui_client_chat()
        self.privateChatUI.setupUi(self.privateChatWidget)

        # setting up group chat widget and hide it
        self.groupChatWidget = QtWidgets.QWidget(self.mainWindow)
        self.groupChatWidget.setHidden(True)
        self.groupChatUI = client_groupchat.Ui_Form()
        self.groupChatUI.setupUi(self.groupChatWidget)

        self.inviteToGCWidget = QtWidgets.QWidget(self.mainWindow)
        self.inviteToGCWidget.setHidden(True)
        self.inviteToGCUI = client_invite_member_to_gc.Ui_Form()
        self.inviteToGCUI.setupUi(self.inviteToGCWidget)

        self.inviteToGCInvitationDialog = QtWidgets.QDialog(self.mainWindow)
        self.inviteToGCInvitationDialog.setHidden(True)
        self.inviteToGCDialogUI = client_invitation_to_group_chat.Ui_Dialog()
        self.inviteToGCDialogUI.setupUi(self.inviteToGCInvitationDialog)

        self.mainWindow.setGeometry(QtCore.QRect(1080, 400, 400, 300))
        self.mainWindow.show()

    def btn_cancel_clicked(self):
        self.connected = False
        sys.exit(0)

    def btn_ok_clicked(self):
        host = self.setupUI.IPAddress_LineEdit.text()
        port = self.setupUI.Port_LineEdit.text()
        self.nickname = self.setupUI.Nickname_LineEdit.text()

        if len(host) == 0:
            host = "localhost"
        if len(port) == 0:
            port = 9988
        else:
            try:
                port = int(port)
            except Exception as e:
                error = "Invalid port number \n'{}'".format(str(e))
                print("[INFO]", error)
                show_error("Port Number Error", error)

        if len(self.nickname) < 1:
            nickname = socket.gethostname()

        # Unique random identifier for server
        self.nickname = self.nickname + "_" + str(random.randint(1, 10000))

        if self.connecting(host, port, self.nickname):
            self.setupWidget.setHidden(True)
            self.connected = True
            self.worker.moveToThread(self.recv_thread)
            self.recv_thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.recv_thread.quit)
            self.worker.signalForUpdatedConnectedClientsList.connect(self.getConnectedClients)
            self.worker.invitationSignal.connect(self.respond_to_invitation)
            self.worker.sender_start_priv_chat.connect(self.sender_start_priv_chat)
            self.worker.show_message.connect(self.show_message)
            self.worker.pass_groupchat_room_number.connect(self.setRoomNumberLabelOnGroupChat)
            self.worker.set_GC_Members_List.connect(self.set_GC_Members_List)
            self.worker.set_not_in_GC_members_list.connect(self.set_not_connected_clients_invite_list)
            self.worker.show_invitation_to_GC.connect(self.show_invitation_to_GC)
            self.worker.join_gc_successful.connect(self.load_gc)
            self.worker.update_chatrooms_list.connect(self.update_chatrooms_list)
            self.worker.send_message_to_all_gc_members.connect(self.update_groupchat_messages)
            self.worker.get_active_chatrooms.connect(self.set_active_chatrooms)
            self.recv_thread.start()
            self.start_home()

            # self.recv_thread.messageSignal.connect(self.show_message)

    def connecting(self, host, port, nickname):
        try:
            self.client_socket = self.context.wrap_socket(self.client_socket, server_hostname=host)
            self.client_socket.connect((host, port))
            print(f'Now connected to chat server@ address {host} on port {port}')

            send(self.client_socket, 'NAME: ' + nickname)
            data = receive(self.client_socket)

            print("[INFO] Connected to server")
            self.recv_thread = QThread()
            self.worker = Worker(self.client_socket)

            return True
        except Exception as e:
            error = "Unable to connect to server \n'{}'".format(str(e))
            print("[INFO]")
            show_error("Connection Error", error)
            self.setupUI.IPAddress_LineEdit.clear()
            self.setupUI.Port_LineEdit.clear()

            return False

    def start_home(self):
        send(self.client_socket, 'C-LIST')
        send(self.client_socket, 'CR_LIST')
        self.privateChatWidget.setHidden(True)
        self.privateChatWidget.close()
        self.groupChatWidget.setHidden(True)
        self.groupChatWidget.close()
        self.homeWidget.setHidden(False)
        self.clientHomeUI.oneToOneChatButton.setDefault(True)
        self.clientHomeUI.oneToOneChatButton.clicked.connect(lambda: self.oneToOneChat())
        self.clientHomeUI.CreateGCButton.clicked.connect(lambda: self.createGroupChat())
        self.clientHomeUI.JoinButton.clicked.connect(lambda: self.pre_join_GC())

    def getConnectedClients(self, data):
        self.clientHomeUI.connected_clients_list.clear()
        arr = data[0].split('#')
        for d in arr:
            if d == '':
                break
            self.clientHomeUI.connected_clients_list.addItem(d.split('@')[0])

    def oneToOneChat(self):
        # send invitation to other person
        clientToContact = self.clientHomeUI.connected_clients_list.currentItem().text()
        send(self.client_socket, 'CONTACT_CLIENT#' + clientToContact)

    def respond_to_invitation(self, sender, receiver):
        self.invitationDialogUI.senderLabel.setText(sender)
        self.invitationDialogUI.AcceptInvitationButton.clicked.connect(lambda: self.start_priv_chat(sender, receiver))
        self.invitationDialogUI.RejectInvitationButton.clicked.connect(lambda: self.reject_priv_chat(sender, receiver))
        self.invitationDialog.setHidden(False)

    def start_priv_chat(self, sender, receiver):
        send(self.client_socket, 'OK#' + sender)
        self.invitationDialog.setHidden(True)
        self.homeWidget.setHidden(True)
        self.mainWindow.setWindowTitle("Chatting with: " + sender)
        self.privateChatWidget.deleteLater()
        self.privateChatWidget = QtWidgets.QWidget(self.mainWindow)
        self.privateChatUI = client_chat.Ui_client_chat()
        self.privateChatUI.setupUi(self.privateChatWidget)
        self.privateChatUI.messageDisplayBrowser.clear()
        self.privateChatUI.lineEdit.clear()
        self.privateChatUI.label_2.setText(sender)
        self.privateChatUI.sendButton.clicked.connect(lambda: self.sendMessage(receiver, sender))
        self.privateChatUI.closeChatButton.clicked.connect(lambda: self.start_home())
        self.privateChatWidget.setHidden(False)

    def sender_start_priv_chat(self, receiver):
        self.mainWindow.setWindowTitle("Chatting with: " + receiver)
        self.homeWidget.setHidden(True)
        self.privateChatWidget.deleteLater()
        self.privateChatWidget = QtWidgets.QWidget(self.mainWindow)
        self.privateChatUI = client_chat.Ui_client_chat()
        self.privateChatUI.setupUi(self.privateChatWidget)
        self.privateChatUI.messageDisplayBrowser.clear()
        self.privateChatUI.label_2.setText(receiver)
        self.privateChatUI.sendButton.clicked.connect(lambda: self.sendMessage(self.nickname, receiver))
        self.privateChatUI.closeChatButton.clicked.connect(lambda: self.start_home())
        self.privateChatWidget.setHidden(False)

    def reject_priv_chat(self, sender, receiver):
        self.invitationDialog.setHidden(True)
        send(self.client_socket, 'REJECT#' + sender)

    def sendMessage(self, sender, receiver):
        message = self.privateChatUI.lineEdit.text()
        self.privateChatUI.messageDisplayBrowser.append(sender + '> ' + message)
        self.privateChatUI.lineEdit.clear()
        msg = 'MESSAGE#' + sender + '#' + receiver + '#' + message
        send(self.client_socket, msg)

    def show_message(self, sender, message):
        self.privateChatUI.messageDisplayBrowser.append(sender + '> ' + message)

    def createGroupChat(self):
        send(self.client_socket, 'CREATE_GC')

    def setRoomNumberLabelOnGroupChat(self, roomNo):
        self.current_roomNo = roomNo
        self.groupChatWidget.deleteLater()
        self.groupChatWidget = QtWidgets.QWidget(self.mainWindow)
        self.groupChatUI = client_groupchat.Ui_Form()
        self.groupChatUI.setupUi(self.groupChatWidget)
        self.groupChatUI.label_4.setText(str(roomNo))
        self.setupGroupChatFunctionalities()

    def setupGroupChatFunctionalities(self):
        self.homeWidget.setHidden(True)
        self.groupChatWidget.setHidden(False)
        self.groupChatUI.hostLabel.setText(self.nickname)
        print("to send to server: " + str(self.current_roomNo))
        send(self.client_socket, 'GC_MEMBERS#' + str(self.current_roomNo))
        self.groupChatUI.inviteButton.clicked.connect(lambda: self.groupChatInvite(self.current_roomNo))

    def set_GC_Members_List(self, memberList):
        print(memberList)
        self.groupChatUI.membersInRoom.clear()
        for member in memberList:
            self.groupChatUI.membersInRoom.append(member.split('@')[0])

    def groupChatInvite(self, current_roomNo):
        send(self.client_socket, 'NOT_CONNECTED_CLIENTS#' + str(current_roomNo))
        self.inviteToGCUI.inviteButton.clicked.connect(lambda: self.invite_to_GC(self.nickname, current_roomNo))
        self.inviteToGCUI.CancelButton.clicked.connect(lambda: self.go_back_to_groupchat())
        self.groupChatWidget.setHidden(True)
        self.inviteToGCWidget.setHidden(False)

    def set_not_connected_clients_invite_list(self, not_in_gc):
        self.inviteToGCUI.connectedClientsNotInGCList.clear()
        for member in not_in_gc:
            self.inviteToGCUI.connectedClientsNotInGCList.addItem(member.split('@')[0])

    def invite_to_GC(self, nickname, current_roomNo):
        clientToContact = self.inviteToGCUI.connectedClientsNotInGCList.currentItem().text()
        send(self.client_socket, 'INVITE_THIS_CLIENT#' + clientToContact + '#' + nickname + '#' + str(current_roomNo))

    def show_invitation_to_GC(self, sender, roomNo):
        self.inviteToGCInvitationDialog.setHidden(False)
        self.inviteToGCDialogUI.senderLabel.setText(sender)
        self.inviteToGCDialogUI.roomNoLabel.setText(str(roomNo))
        self.inviteToGCDialogUI.AcceptButton.clicked.connect(lambda: self.join_GC(sender, roomNo))
        self.inviteToGCDialogUI.RejectButton.clicked.connect(lambda: self.close_invitation())

    def close_invitation(self):
        self.inviteToGCInvitationDialog.close()

    def join_GC(self, sender, roomNo):
        send(self.client_socket, 'WILL_JOIN#' + str(roomNo))

    def go_back_to_groupchat(self):
        self.inviteToGCWidget.setHidden(True)
        self.groupChatWidget.setHidden(False)

    def load_gc(self, roomNo, activeMembers):
        self.inviteToGCWidget.setHidden(True)
        self.homeWidget.setHidden(True)
        self.groupChatWidget.deleteLater()
        self.groupChatWidget = QtWidgets.QWidget(self.mainWindow)
        self.groupChatUI = client_groupchat.Ui_Form()
        self.groupChatUI.setupUi(self.groupChatWidget)
        self.setRoomNumberLabelOnGroupChat(roomNo)
        self.groupChatUI.sendButton.clicked.connect(lambda: self.sendToMultipleClients(self.nickname, activeMembers))
        self.groupChatUI.closeButton.clicked.connect(lambda: self.start_home())
        self.groupChatWidget.setHidden(False)

    def sendToMultipleClients(self, sender, activeMembers):
        message = self.groupChatUI.sendMessageLineEdit.text()
        self.groupChatUI.sendMessageLineEdit.clear()
        memberString = '!'.join(activeMembers)
        msg = 'MESSAGE_MULTIPLE#' + sender + '#' + memberString + '#' + message
        send(self.client_socket, msg)

    def update_chatrooms_list(self, activeChatrooms):
        self.clientHomeUI.chat_rooms_list.clear()
        for gc_room_number in activeChatrooms.keys():
            chatRoomString = "Room " + str(gc_room_number) + " by " + activeChatrooms.get(gc_room_number)[0]
            self.clientHomeUI.chat_rooms_list.addItem(chatRoomString)

    def update_groupchat_messages(self, sender, message):
        self.groupChatUI.MessageBrowser.append(sender + "> " + message)

    def pre_join_GC(self):
        text = self.clientHomeUI.chat_rooms_list.currentItem().text()
        roomNo = int(text.split(' ')[1])
        self.join_GC(self.nickname, roomNo)

    def set_active_chatrooms(self, groupchats):
        self.clientHomeUI.chat_rooms_list.clear()
        for room in groupchats.keys():
            chatRoomString = "Room " + str(room) + " by " + groupchats.get(room)[0]
            self.clientHomeUI.chat_rooms_list.addItem(chatRoomString)


class Worker(QObject):
    finished = QtCore.pyqtSignal()
    signalForUpdatedConnectedClientsList = QtCore.pyqtSignal(list)
    messageSignal = QtCore.pyqtSignal(str)
    invitationSignal = QtCore.pyqtSignal(str, str)
    sender_start_priv_chat = QtCore.pyqtSignal(str)
    show_message = QtCore.pyqtSignal(str, str)
    pass_groupchat_room_number = QtCore.pyqtSignal(int)
    set_GC_Members_List = QtCore.pyqtSignal(list)
    set_not_in_GC_members_list = QtCore.pyqtSignal(list)
    show_invitation_to_GC = QtCore.pyqtSignal(str, int)
    join_gc_successful = QtCore.pyqtSignal(int, list)
    update_chatrooms_list = QtCore.pyqtSignal(dict)
    send_message_to_all_gc_members = QtCore.pyqtSignal(str, str)
    get_active_chatrooms = QtCore.pyqtSignal(dict)

    def __init__(self, client_socket):
        super(Worker, self).__init__()
        self.client_socket = client_socket
        self.connected = True

    def run(self):
        while self.connected:
            self.receive_data()
        self.finished.emit(2)

    def receive_data(self):
        data = receive(self.client_socket)
        if data:
            if type(data) is list:
                # get list of connected clients
                if data[0] == 1:
                    data.pop(0)
                    message = data
                    self.signalForUpdatedConnectedClientsList.emit(message)
                # send invite for private chat, #data[1] contains the client the invitation is from,
                # data[2] contains the client the invitation is to
                if data[0] == 2:
                    sender = data[1].split('@')[0]
                    receiver = data[2]
                    self.invitationSignal.emit(sender, receiver)
                # if the client accepts the invitation to private chat
                # sender client should receive conf from server
                if data[0] == 3:
                    receiver = data[1].split('@')[0]
                    self.sender_start_priv_chat.emit(receiver)
                if data[0] == 4:
                    # data[1] is the person who sent it to them
                    # data[2] is message
                    sender = data[1].split('@')[0]
                    self.show_message.emit(sender, data[2])
                if data[0] == 5:
                    print(data[1])
                    self.pass_groupchat_room_number.emit(data[1])
                if data[0] == 6:
                    self.set_GC_Members_List.emit(data[1])
                if data[0] == 7:
                    self.set_not_in_GC_members_list.emit(data[1])
                if data[0] == 8:
                    self.show_invitation_to_GC.emit(data[1], int(data[2]))
                if data[0] == 9:
                    print("does it?")
                    self.join_gc_successful.emit(int(data[1]), data[2])
                if data[0] == 10:
                    self.send_message_to_all_gc_members.emit(data[1], data[2])
                if data[0] == 11:
                    self.update_chatrooms_list.emit(data[1])
                if data[0] == 12:
                    self.get_active_chatrooms.emit(data[1])
            elif type(data) is str:
                pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    c = Client()
    sys.exit(app.exec())
