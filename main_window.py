"""
Main application window.
The UI layer knows nothing about WMI, providers, or OS calls.
It only speaks to DNSService.
"""

from __future__ import annotations
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QMessageBox,
)

from ..core import DNSService, ServiceError, State
from ..core.providers import providers_by_category


class MainWindow(QWidget):

    def __init__(self, service: DNSService) -> None:
        super().__init__()
        self._service = service
        self._build_ui()
        self._refresh()

    # ------------------------------------------------------------------ build

    def _build_ui(self) -> None:
        self.setWindowTitle("DNS Changer")
        self.setFixedSize(420, 220)

        self._status_lbl  = QLabel("یک provider انتخاب کنید.")
        self._dns_lbl     = QLabel()
        self._desc_lbl    = QLabel("")
        self._desc_lbl.setStyleSheet("color: gray; font-size: 10px;")

        self._combo = QComboBox()
        self._combo.addItem("── انتخاب provider ──")
        # گروه‌بندی بر اساس category
        for category, providers in providers_by_category().items():
            if not providers:
                continue
            # جداکننده گروه (غیر قابل انتخاب)
            self._combo.insertSeparator(self._combo.count())
            # عنوان گروه به عنوان آیتم غیرفعال
            self._combo.addItem(f"▸ {category.value}")
            idx = self._combo.count() - 1
            self._combo.model().item(idx).setEnabled(False)
            for p in providers:
                self._combo.addItem(f"  {p.name}", userData=p.name)

        self._combo.currentIndexChanged.connect(self._on_index_changed)

        self._btn = QPushButton("Activate")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._on_toggle)

        layout = QVBoxLayout()
        layout.addWidget(self._status_lbl)
        layout.addWidget(self._dns_lbl)
        layout.addWidget(self._desc_lbl)
        layout.addWidget(self._combo)

        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(self._btn)
        layout.addLayout(row)

        self.setLayout(layout)

    # ------------------------------------------------------------- helpers

    def _selected_provider_key(self) -> str | None:
        """Return the provider key stored as userData, or None."""
        return self._combo.currentData()

    # ------------------------------------------------------------- slots

    def _on_index_changed(self) -> None:
        key = self._selected_provider_key()
        if key is None:
            self._btn.setEnabled(False)
            self._desc_lbl.setText("")
            return

        provider = self._service.available_providers().get(key)
        self._desc_lbl.setText(provider.description if provider else "")
        self._btn.setEnabled(True)

        if self._service.is_active:
            self._run(lambda: self._service.deactivate())
            self._status_lbl.setText("Provider تغییر کرد — دوباره Activate کنید.")
            self._btn.setText("Activate")

    def _on_toggle(self) -> None:
        key = self._selected_provider_key()
        if key is None:
            return

        if self._service.is_active:
            self._run(lambda: self._service.deactivate())
        else:
            self._run(lambda: self._service.activate(key))

        self._refresh()

    # ------------------------------------------------------------ helpers

    def _run(self, fn) -> bool:
        """Execute a service call, show error dialog on ServiceError."""
        try:
            fn()
            return True
        except ServiceError as e:
            self._show_warning(str(e))
            return False

    def _refresh(self) -> None:
        """Sync all labels with current service state."""
        servers = self._service.current_dns()
        self._dns_lbl.setText(
            "Current DNS: " + (", ".join(servers) if servers else "Automatic (DHCP)")
        )

        if self._service.state is State.ACTIVE:
            self._status_lbl.setText(
                f"DNS روی {self._service.active_provider} فعال است."
            )
            self._btn.setText("Deactivate")
        else:
            if self._combo.currentText() != "انتخاب provider":
                self._status_lbl.setText("DNS در حالت پیش‌فرض است.")

    @staticmethod
    def _show_warning(msg: str) -> None:
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle("هشدار")
        box.setText(msg)
        box.exec_()
