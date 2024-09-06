import sys
import logging
from PyQt6.QtWidgets import QApplication
from KaasQt.main_window import MainWindow
from KaasQt.utils import measure_loading_time, setup_logging

class KaasApp:
    """
    Main application class for Kaas.
    """

    def __init__(self):
        """
        Initialize the Kaas application.
        """
        self.app = QApplication(sys.argv)
        self.main_window = None
        setup_logging()

    @measure_loading_time
    def run(self):
        """
        Run the Kaas application.
        """
        try:
            self.main_window = MainWindow()
            self.main_window.show()
            return self.app.exec()
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            return 1

if __name__ == "__main__":
    kaas_app = KaasApp()
    sys.exit(kaas_app.run())