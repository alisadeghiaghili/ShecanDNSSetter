# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 02:11:24 2023

@author: Ali Sadeghi
"""

# The app should be run as admin

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import wmi
import time

class DNSChangerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("DNS Changer")
        self.setGeometry(100, 100, 300, 150)

        self.primary_dns = '178.22.122.100'
        self.secondary_dns = '185.51.200.2'
        self.default_dns = ['Obtain DNS server address automatically']

        self.status_label = QLabel('Click the button to set custom DNS.')
        self.current_dns_label = QLabel('Current DNS: ')
        self.dns_button = QPushButton('Activate')
        self.dns_button.clicked.connect(self.toggle_dns)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.current_dns_label)
        layout.addWidget(self.dns_button)
        self.setLayout(layout)

        self.update_current_dns_label()

    def toggle_dns(self):
        if self.dns_button.text() == 'Activate':
            self.set_custom_dns()
            self.dns_button.setText('Deactivate')
            self.status_label.setText(f"Custom DNS set: {self.primary_dns}, {self.secondary_dns}")
        else:
            self.reset_dns()
            self.dns_button.setText('Activate')
            self.status_label.setText('Click the button to set custom DNS.')
        self.update_current_dns_label()

    def set_custom_dns(self):
        c = wmi.WMI()
        adapter_configs = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        for adapter in adapter_configs:
            if "Wireless" in adapter.Description or "Ethernet" in adapter.Description:
                adapter.SetDNSServerSearchOrder([self.primary_dns, self.secondary_dns])

    def reset_dns(self):
        c = wmi.WMI()
        adapter_configs = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        for adapter in adapter_configs:
            if "Wireless" in adapter.Description or "Ethernet" in adapter.Description:
                adapter.SetDNSServerSearchOrder([])

        # Wait for a short duration for DNS settings to take effect
        time.sleep(2)

    def get_current_dns(self):
        c = wmi.WMI()
        adapter_configs = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        for adapter in adapter_configs:
            if "Wireless" in adapter.Description or "Ethernet" in adapter.Description:
                return adapter.DNSServerSearchOrder

    def update_current_dns_label(self):
        current_dns = self.get_current_dns()
        if current_dns:
            self.current_dns_label.setText(f'Current DNS: {", ".join(current_dns)}')
        else:
            self.current_dns_label.setText('Current DNS: Obtain DNS server address automatically')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DNSChangerApp()
    window.show()
    sys.exit(app.exec_())
