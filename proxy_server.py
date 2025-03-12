#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
import socket
import threading

class ProxyServer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.server_socket = None
        self.is_running = False

    def initUI(self):
        self.setWindowTitle('SOCKS5 Proxy Server')
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.port_label = QLabel('Port:', self)
        self.port_input = QLineEdit(self)
        self.port_input.setText('1688')

        self.start_button = QPushButton('Start Server', self)
        self.start_button.clicked.connect(self.start_server)

        self.stop_button = QPushButton('Stop Server', self)
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def log_message(self, message):
        self.text_edit.append(message)

    def start_server(self):
        port = int(self.port_input.text())
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        self.is_running = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.log_message(f'Server started on port {port}')

        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        while self.is_running:
            client_socket, addr = self.server_socket.accept()
            self.log_message(f'Connection from {addr}')
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            # Handle SOCKS5 protocol here
            pass
        finally:
            client_socket.close()

    def stop_server(self):
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.log_message('Server stopped')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    proxy_server = ProxyServer()
    proxy_server.show()
    sys.exit(app.exec_())