import subprocess
import ctypes
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox

class DNSChanger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DNS Changer")
        self.setFixedSize(400, 150)

        label = QLabel(self)
        label.setText("Click the button to change your DNS servers to 178.22.122.100 and 185.51.200.2.")
        label.setGeometry(50, 20, 300, 30)

        button = QPushButton(self)
        button.setText("Change DNS")
        button.setGeometry(100, 60, 200, 30)
        button.clicked.connect(self.set_dns)

        close_button = QPushButton(self)
        close_button.setText("Close")
        close_button.setGeometry(150, 100, 100, 30)
        close_button.clicked.connect(self.close)

    def set_dns(self):
        try:
            # Check if the script is running as an administrator
            if not ctypes.windll.shell32.IsUserAnAdmin():
                QMessageBox.critical(self, "Error", "Please run this script as an administrator.")
                return

            # Set the DNS servers
            command = 'netsh interface ip set dns "Ethernet" static 178.22.122.100 primary'
            subprocess.call(command, shell=True)
            command = 'netsh interface ip add dns "Ethernet" 185.51.200.2 index=2'
            subprocess.call(command, shell=True)

            QMessageBox.information(self, "Success", "DNS servers have been changed to 178.22.122.100 and 185.51.200.2.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def close(self):
        try:
            # Reset the DNS servers to their defaults
            command = 'netsh interface ip set dns "Ethernet" dhcp'
            subprocess.call(command, shell=True)

            QMessageBox.information(self, "Success", "DNS servers have been reset to their defaults.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DNSChanger()
    window.show()
    sys.exit(app.exec_())
