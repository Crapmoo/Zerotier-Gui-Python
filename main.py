import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QWidget, QMessageBox
import subprocess

class ZerotierGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zerotier Network Manager by Crapmoo")
        self.setGeometry(0, 0, 800, 600)
        self.setWindowIcon(QIcon('icon.ico'))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setStyleSheet("background-color: #333333; color: #ffffff;")

        self.text_box = QTextEdit()  
        text = list_network()
        self.text_box.setPlainText(text)

        self.text_box.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
        layout.addWidget(self.text_box)

        self.network_id_label = QLabel("Network ID:")
        self.network_id_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(self.network_id_label)

        self.network_id_entry = QLineEdit()
        layout.addWidget(self.network_id_entry)

        join_button = QPushButton("Join Network")
        join_button.clicked.connect(self.join_network_and_reload)
        layout.addWidget(join_button)

        leave_button = QPushButton("Leave Network")
        leave_button.clicked.connect(self.leave_network_and_reload)
        layout.addWidget(leave_button)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        central_widget.setLayout(layout)

    def join_network_and_reload(self):
        network_id = self.network_id_entry.text()
        result = subprocess.run(['zerotier-cli', 'join', network_id], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            QMessageBox.information(self, "Success", f"Joined network with ID: {network_id}")
            self.reload_text()  
        else:
            QMessageBox.critical(self, "Error", "Failed to join the network. Check the network ID.")

    def leave_network_and_reload(self):
        network_id = self.network_id_entry.text()
        result = subprocess.run(['zerotier-cli', 'leave', network_id], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            QMessageBox.information(self, "Success", f"Left network with ID: {network_id}")
            self.reload_text()  
        else:
            QMessageBox.critical(self, "Error", "Failed to leave the network. Check the network ID.")

    def reload_text(self):
        
        text = list_network()
        self.text_box.setPlainText(text)

def list_network():
    result = subprocess.run(['zerotier-cli', 'listnetworks'], capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        return f"{result.stdout}Restart the program if you don't find Network Lists."
    else:
        return f"Error: {result.stderr}"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ZerotierGUI()
    window.show()
    sys.exit(app.exec_())
    # code by crapmoo