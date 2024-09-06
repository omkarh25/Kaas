from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class VoiceRecordingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Voice Recording")
        layout.addWidget(title_label)

        record_button = QPushButton("Start Recording")
        layout.addWidget(record_button)

        self.setLayout(layout)

# Add logging statements
import logging
logging.info("VoiceRecordingTab module loaded successfully")