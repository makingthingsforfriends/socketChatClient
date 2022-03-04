import select
import socket
import sys
import signal
import argparse
import ssl
from collections import defaultdict

from utils import *

SERVER_HOST = 'localhost'


class ChatServer(object):
    """ An example chat server using select """

    def __init__(self, port, backlog=5):
        self.key = 0
        self.client = None
        self.clients = 0
        self.clientmap = {}
        self.priv_chatRooms = {}
        self.active_group_chats = {}
        self.group_chat_hosts = {}
        self.outputs = []  # list output sockets

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem")
        self.context.load_verify_locations('cert.pem')
        self.context.set_ciphers('AES128-SHA')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.listen(backlog)
        self.server = self.context.wrap_socket(self.server, server_side=True)

        # Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

        print(f'Server listening to port: {port} ...')

    def sighandler(self, signum, frame):
        """ Clean up client outputs"""
        print('Shutting down server...')

        # Close existing client sockets
        for output in self.outputs:
            output.close()

        self.server.close()

    def get_client_name(self, client):
        """ Return the name of the client """
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def run(self):
        # inputs = [self.server, sys.stdin]
        inputs = [self.server]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(
                    inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                self.sock = sock
                sys.stdout.flush()
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print(
                        f'Chat server: got connection {client.fileno()} from {address}')
                    # Read the login name
                    cname = receive(client).split('NAME: ')[1]

                    # Compute client name and send back
                    self.clients += 1
                    send(client, f'CLIENT: {str(address[0])}')
                    inputs.append(client)

                    self.clientmap[client] = (address, cname)
                    # Send joining information to other clients
                    msg = f'\n(Connected: New client ({self.clients}) from {self.get_client_name(client)})'
                    for output in self.outputs:
                        send(output, msg)
                    self.outputs.append(client)

                else:
                    # handle all other sockets
                    try:
                        data = receive(sock)
                        if data:
                            if data == 'C-LIST':
                                self.currentOutput = sock
                                clientList = self.listOfConnectedClients()
                                send(sock, [1, clientList])
                                for output in self.outputs:
                                    if output != self.server and output != sock:
                                        self.currentOutput = output
                                        send(output, [1, self.listOfConnectedClients()])
                            if data == 'CR_LIST':
                                send(sock, [12, self.group_chat_hosts])
                            elif data == 'CREATE_GC':
                                self.active_group_chats[self.key] = [sock]
                                self.group_chat_hosts[self.key] = self.get_client_name(sock)
                                send(sock, [5, self.key])
                                self.key += 1
                                for output in self.outputs:
                                    if output != self.server:
                                        send(output, [11, self.group_chat_hosts])
                            elif data.split('#')[0] == 'GC_MEMBERS':
                                send(sock, [6, self.get_groupChat_members(sock, data.split('#')[1])])
                            elif data.split('#')[0] == 'NOT_CONNECTED_CLIENTS':
                                send(sock, [7, self.get_clients_not_in_groupchat(int(data.split('#')[1]))])
                            elif data.split("#")[0] == 'CONTACT_CLIENT':
                                send(self.get_client_with_name(data.split("#")[1]), [2, self.get_client_name(sock),
                                                                                     data.split('#')[1]])
                            elif data.split("#")[0] == 'OK':
                                # receiver client has accepted the chat invitation, add to priv chat rooms
                                self.priv_chatRooms[sock] = self.get_client_with_name(data.split("#")[1])
                                self.priv_chatRooms[data.split("#")[1]] = sock
                                send(self.get_client_with_name(data.split("#")[1]), [3, self.get_client_name(sock)])
                            elif data.split('#')[0] == 'MESSAGE':
                                arr = data.split('#')
                                send(self.get_client_with_name(arr[2]), [4, arr[1], arr[3]])
                            elif data.split('#')[0] == 'INVITE_THIS_CLIENT':
                                arr = data.split('#')
                                send(self.get_client_with_name(arr[1]), [8, arr[2], arr[3]])
                            elif data.split('#')[0] == 'WILL_JOIN':
                                arr = data.split('#')
                                # adds new client to the group chat list in the gc dict (keyed by room no)
                                if sock not in self.active_group_chats[int(arr[1])]:
                                    self.active_group_chats[int(arr[1])].append(sock)
                                activeGCMembers = []
                                for eachClient in self.active_group_chats.get(int(arr[1])):
                                    activeGCMembers.append(self.get_client_name(eachClient))

                                for eachClient in self.active_group_chats[int(arr[1])]:
                                    send(eachClient, [9, arr[1], activeGCMembers])
                            elif data.split('#')[0] == 'MESSAGE_MULTIPLE':
                                memberList = list(data.split('#')[2].split('!'))

                                for member in memberList:
                                    send(self.get_client_with_name(member.split('@')[0]), [10, self.get_client_name(sock),
                                                                             data.split('#')[3]])
                            else:
                                # Send as new client's message...
                                msg = f'\n#[{self.get_client_name(sock)}]>> {data}'

                                # Send data to all except ourself
                                for output in self.outputs:
                                    if output != sock:
                                        send(output, msg)
                        else:
                            print(f'Chat server: {sock.fileno()} hung up')
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)

                            # Sending client leaving information to others
                            msg = f'\n(Now hung up: Client from {self.get_client_name(sock)})'

                            for output in self.outputs:
                                send(output, msg)
                    except socket.error as e:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)

                    # test if socket is still connected
                    try:
                        send(sock, 'test')
                    except socket.error as e:
                        msg = f'\n(Now hung up: Client from {self.get_client_name(sock)})'
                        print(msg)
                        if sock in self.clientmap.keys():
                            self.clientmap.pop(sock)
                            for output in self.outputs:
                                if output != self.server and output != sock:
                                    self.currentOutput = output
                                    send(output, [1, self.listOfConnectedClients()])
                        if sock in self.priv_chatRooms.keys():
                            self.priv_chatRooms.pop(sock)
        self.server.close()

    def listOfConnectedClients(self):
        s = ""
        for anyClient in self.clientmap:
            if anyClient != self.currentOutput:
                s += self.get_client_name(anyClient)
                s += "#"
        msg = f'{s}'
        return msg

    def get_client_with_name(self, cname):
        for val in self.clientmap.values():
            if val[1] == cname:
                return list(self.clientmap.keys())[list(self.clientmap.values()).index(val)]

    def get_groupChat_members(self, sock, roomNo):
        gc_members_list = self.active_group_chats[int(roomNo)]
        client_name_list = []

        for client in gc_members_list:
            client_name_list.append(self.get_client_name(client))

        return client_name_list

    def get_clients_not_in_groupchat(self, roomNo):
        gc_members_list = self.active_group_chats[roomNo]
        print("This is gc members list")
        print(gc_members_list)
        actual_members = []
        for member in gc_members_list:
            actual_members.append(self.get_client_name(member))
        all_members_list = []
        for anyClient in self.clientmap:
            all_members_list.append(self.get_client_name(anyClient))
        return list(set(all_members_list) - set(actual_members))


if __name__ == "__main__":
    port = 9988
    server = ChatServer(port)
    server.run()
