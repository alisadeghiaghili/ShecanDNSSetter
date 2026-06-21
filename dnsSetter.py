# -*- coding: utf-8 -*-
"""
DNS Changer Application
@author: Ali Sadeghi
"""

import sys
import ctypes
import wmi
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QMessageBox
)


DNS_PROVIDERS = {
    'Shecan': ('178.22.122.100', '185.51.200.2'),
    '403':    ('10.202.10.202',  '10.202.10.102'),
}


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def get_active_adapters():
    """Return all IP-enabled adapters that are Wireless or Ethernet."""
    c = wmi.WMI()
    return [
        a for a in c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        if a.Description and (
            "Wireless" in a.Description or "Ethernet" in a.Description
        )
    ]


def read_current_dns() -> list[str]:
    """Read DNS servers from the first matching active adapter."""
    for adapter in get_active_adapters():
        servers = adapter.DNSServerSearchOrder
        if servers:
            return [s for s in servers if s]
    return []


class DNSChangerApp(QWidget):
    def __init__(self):
        super().__init__()
        # DNS قبل از هر تغییری ذخیره می‌شه
        self._original_dns: list[str] | None = None
        self._custom_active = False
        self._initUI()

    # ------------------------------------------------------------------ UI --

    def _initUI(self):
        self.setWindowTitle("DNS Changer")
        self.setFixedSize(340, 180)

        self.status_label      = QLabel('یک provider انتخاب کنید.')
        self.current_dns_label = QLabel()

        self.provider_combo = QComboBox()
        self.provider_combo.addItem('انتخاب provider')
        self.provider_combo.addItems(DNS_PROVIDERS.keys())
        self.provider_combo.currentTextChanged.connect(self._on_provider_changed)

        self.toggle_btn = QPushButton('Activate')
        self.toggle_btn.setEnabled(False)
        self.toggle_btn.clicked.connect(self._toggle_dns)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.current_dns_label)
        layout.addWidget(self.provider_combo)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.toggle_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)
        self._refresh_dns_label()

    # ----------------------------------------------------------- Slots ------

    def _on_provider_changed(self, text: str):
        """اگه DNS فعاله و provider عوض شد، اول reset کن."""
        if text == 'انتخاب provider':
            self.toggle_btn.setEnabled(False)
            return

        self.toggle_btn.setEnabled(True)

        if self._custom_active:
            self._do_reset()
            self.toggle_btn.setText('Activate')
            self.status_label.setText('Provider تغییر کرد — دوباره Activate کنید.')

    def _toggle_dns(self):
        if self._custom_active:
            self._do_reset()
            self.toggle_btn.setText('Activate')
            self.status_label.setText('DNS به حالت اولیه برگشت.')
        else:
            self._do_activate()

        self._refresh_dns_label()

    # -------------------------------------------------- Core logic ----------

    def _do_activate(self):
        provider = self.provider_combo.currentText()
        if provider not in DNS_PROVIDERS:
            return

        primary, secondary = DNS_PROVIDERS[provider]

        try:
            # ذخیره DNS فعلی قبل از تغییر
            self._original_dns = read_current_dns() or None

            adapters = get_active_adapters()
            if not adapters:
                self._warn("هیچ adapter فعالی پیدا نشد.")
                return

            failed = False
            for adapter in adapters:
                result = adapter.SetDNSServerSearchOrder([primary, secondary])
                # WMI یه tuple برمی‌گردونه؛ عنصر اول return code هست
                ret_code = result[0] if isinstance(result, (list, tuple)) else result
                if ret_code != 0:
                    failed = True

            if failed:
                self._warn(
                    "تغییر DNS با خطا مواجه شد.\n"
                    "مطمئن شوید برنامه با دسترسی Administrator اجرا شده."
                )
                self._original_dns = None
                return

            self._custom_active = True
            self.toggle_btn.setText('Deactivate')
            self.status_label.setText(f"DNS روی {provider} تنظیم شد.")

        except Exception as e:
            self._warn(f"خطا در تنظیم DNS:\n{e}")

    def _do_reset(self):
        try:
            adapters = get_active_adapters()
            for adapter in adapters:
                # پاس دادن None یا لیست خالی → DHCP automatic
                adapter.SetDNSServerSearchOrder(self._original_dns or [])
        except Exception as e:
            self._warn(f"خطا در بازگردانی DNS:\n{e}")
        finally:
            self._custom_active = False
            self._original_dns = None

    # --------------------------------------------------------- Helpers ------

    def _refresh_dns_label(self):
        servers = read_current_dns()
        if not servers:
            text = 'Current DNS: Automatic (DHCP)'
        else:
            text = 'Current DNS: ' + ', '.join(servers)
        self.current_dns_label.setText(text)

    @staticmethod
    def _warn(msg: str):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle("هشدار")
        box.setText(msg)
        box.exec_()


# ----------------------------------------------------------------------- main

if __name__ == '__main__':
    if not is_admin():
        # خود برنامه رو با UAC elevation دوباره اجرا می‌کنه
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)

    app = QApplication(sys.argv)
    window = DNSChangerApp()
    window.show()
    sys.exit(app.exec_())
