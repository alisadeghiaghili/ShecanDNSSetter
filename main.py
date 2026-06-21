"""
Entry point.
Responsibilities:
  1. Ensure admin privileges (Windows UAC).
  2. Instantiate DNSService (core).
  3. Pass service into MainWindow (UI).
  4. Run the Qt event loop.
"""

import sys
from PyQt5.QtWidgets import QApplication

from utils.privileges import ensure_admin
from core import DNSService
from ui  import MainWindow


def main() -> None:
    ensure_admin()

    app     = QApplication(sys.argv)
    service = DNSService()
    window  = MainWindow(service)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
