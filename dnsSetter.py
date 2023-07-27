# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 19:37:41 2023

@author: Ali Sadeghi
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
import wmi

class DNSChangerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.custom_dns_activated = False
        self.current_provider = None
        self.default_dns_values = None

    def initUI(self):
        self.setWindowTitle("DNS Changer")
        self.setGeometry(100, 100, 300, 200)

        self.primary_dns_shecan = '178.22.122.100'
        self.secondary_dns_shecan = '185.51.200.2'
        self.primary_dns_403 = '10.202.10.202'
        self.secondary_dns_403 = '10.202.10.102'
        self.default_dns = ['Obtain DNS server address automatically']

        self.status_label = QLabel('Click the button to set custom DNS.')
        self.current_dns_label = QLabel('Current DNS: ')
        self.dns_button = QPushButton('Activate')
        self.dns_button.setEnabled(False)  # Initially disabled
        self.dns_button.clicked.connect(self.toggle_dns)

        self.provider_combo = QComboBox()
        self.provider_combo.addItems(['Select provider', 'Shecan', '403'])
        self.provider_combo.activated[str].connect(self.provider_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.current_dns_label)
        layout.addWidget(self.provider_combo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.dns_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.update_current_dns_label()

    def toggle_dns(self):
        if not self.custom_dns_activated:
            self.set_custom_dns()
            self.dns_button.setText('Deactivate')
            self.status_label.setText(f"Custom DNS set.")
        else:
            self.reset_dns()
            self.dns_button.setText('Activate')
            self.status_label.setText('Click the button to set custom DNS.')
        self.custom_dns_activated = not self.custom_dns_activated
        self.update_current_dns_label()

    def set_custom_dns(self):
        c = wmi.WMI()
        adapter_configs = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        for adapter in adapter_configs:
            if "Wireless" in adapter.Description or "Ethernet" in adapter.Description:
                provider = self.provider_combo.currentText()
                self.current_provider = provider  # Store the current provider
                if provider == 'Shecan':
                    adapter.SetDNSServerSearchOrder([self.primary_dns_shecan, self.secondary_dns_shecan])
                elif provider == '403':
                    adapter.SetDNSServerSearchOrder([self.primary_dns_403, self.secondary_dns_403])
                # Store the default DNS values
                self.default_dns_values = adapter.DNSServerSearchOrder

    def reset_dns(self):
        if self.default_dns_values is not None:
            c = wmi.WMI()
            adapter_configs = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
            for adapter in adapter_configs:
                if "Wireless" in adapter.Description or "Ethernet" in adapter.Description:
                    adapter.SetDNSServerSearchOrder(self.default_dns_values)

    def provider_changed(self, provider_name):
        if provider_name != 'Select provider':
            self.dns_button.setEnabled(True)  # Enable the button when a provider is selected
            if self.custom_dns_activated and self.current_provider != provider_name:
                # Deactivate custom DNS if it's active and provider changed
                self.reset_dns()
                self.dns_button.setText('Activate')
                self.custom_dns_activated = False
                self.status_label.setText('Click the button to set custom DNS.')
                self.update_current_dns_label()
        else:
            self.dns_button.setEnabled(False)  # Disable the button if "Select provider" is selected

    def update_current_dns_label(self):
        c = wmi.WMI()
        adapter_configs = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        for adapter in adapter_configs:
            if "Wireless" in adapter.Description or "Ethernet" in adapter.Description:
                dns_servers = adapter.DNSServerSearchOrder
                if dns_servers == self.default_dns:
                    self.current_dns_label.setText('Current DNS: Default')
                else:
                    self.current_dns_label.setText(f'Current DNS: {", ".join(dns_servers)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DNSChangerApp()
    window.show()
    sys.exit(app.exec_())
