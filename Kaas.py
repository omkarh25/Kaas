# import sys
# import requests
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
#     QPushButton, QStackedWidget, QComboBox, QLabel, QTextEdit, QMessageBox,
#     QFileDialog, QLineEdit, QProgressDialog
# )
# from PyQt6.QtCore import Qt, QThread, pyqtSignal
# from PyQt6.QtGui import QFont, QShortcut, QKeySequence

# class TranscriptFetchThread(QThread):
#     finished = pyqtSignal(str)  # Emit transcript text when done
#     error = pyqtSignal(str)

#     def __init__(self, file_search_dir):
#         super().__init__()
#         self.file_search_dir = file_search_dir

#     def run(self):
#         try:
#             self.fetch_transcript()
#         except Exception as e:
#             self.error.emit(str(e))

#     def fetch_transcript(self):
#         # Use the file_search_dir directly in the URL
#         url = f"http://115.245.248.122:8051/meeting/wisdom-file/{self.file_search_dir}"
#         print(f"Fetching transcript from: {url}")  # Log URL for debugging

#         response = requests.get(url)
#         if response.status_code == 200:
#             print(f"GET Response Text: {response.text}")  # Print the GET response (transcript)
#             self.finished.emit(response.text)  # Pass transcript text to the main thread
#         else:
#             print(f"GET Error: {response.status_code}, {response.text}")  # Print GET error if any
#             self.error.emit(f"Error fetching transcript: {response.status_code}, {response.text}")

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.file_search_dir = None  # Store file_search_dir here
#         self.init_ui()
#         self.create_shortcuts()

#     def init_ui(self):
#         self.setWindowTitle("Meeting Transcriber")
#         self.setGeometry(200, 100, 1000, 600)  # Adjust window size
#         self.setStyleSheet("""
#             QLabel {
#                 font-size: 14px;
#                 font-family: Arial, sans-serif;
#                 color: #444;
#             }
#             QPushButton {
#                 background-color: #1976D2;
#                 color: white;
#                 padding: 12px 24px;
#                 border-radius: 8px;
#                 font-size: 16px;
#             }
#             QPushButton:hover {
#                 background-color: #1565C0;
#             }
#             QLineEdit, QComboBox, QTextEdit {
#                 padding: 10px;
#                 border-radius: 8px;
#                 border: 1px solid #ccc;
#                 font-size: 14px;
#                 background-color: #FAFAFA;
#                 color: black;
#             }
#             QWidget {
#                 background-color: #F5F5F5;
#             }
#             QStackedWidget {
#                 background-color: #FFF;
#             }
#             QVBoxLayout {
#                 spacing: 15px;
#             }
#         """)

#         central_widget = QWidget()
#         main_layout = QHBoxLayout(central_widget)

#         # Sidebar
#         sidebar = QWidget()
#         sidebar_layout = QVBoxLayout(sidebar)
#         sidebar.setFixedWidth(250)
#         sidebar.setStyleSheet("background-color: #2C3E50; padding: 10px;")

#         meeting_transcriber_btn = QPushButton("Meeting Transcriber")
#         meeting_transcriber_btn.setStyleSheet("background-color: #3498DB; color: white;")
#         sidebar_layout.addWidget(meeting_transcriber_btn)

#         transcript_search_btn = QPushButton("Search Transcript")
#         transcript_search_btn.setStyleSheet("background-color: #3498DB; color: white;")
#         sidebar_layout.addWidget(transcript_search_btn)

#         sidebar_layout.addStretch()

#         self.content_stack = QStackedWidget()
#         self.content_stack.addWidget(self.create_meeting_transcriber())
#         self.content_stack.addWidget(self.create_transcript_search())

#         meeting_transcriber_btn.clicked.connect(self.show_meeting_transcriber)
#         transcript_search_btn.clicked.connect(self.show_transcript_search)

#         main_layout.addWidget(sidebar)
#         main_layout.addWidget(self.content_stack, 1)

#         self.setCentralWidget(central_widget)

#     def create_meeting_transcriber(self):
#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         layout.setContentsMargins(30, 20, 30, 20)  # Add margins

#         title = QLabel("Meeting Transcriber")
#         title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
#         title.setStyleSheet("color: #333; margin-bottom: 20px;")
#         layout.addWidget(title)

#         layout.addWidget(QLabel("Language:"))
#         self.language_input = QLineEdit()
#         self.language_input.setPlaceholderText("Enter language code (e.g., 'en')")
#         layout.addWidget(self.language_input)

#         layout.addWidget(QLabel("Meeting Subject:"))
#         self.meeting_subject_input = QLineEdit()
#         self.meeting_subject_input.setPlaceholderText("Enter meeting subject")
#         layout.addWidget(self.meeting_subject_input)

#         layout.addWidget(QLabel("Department:"))
#         self.department_input = QComboBox()
#         self.department_input.addItems(["trademan", "dhoom Studios", "serendipity"])
#         layout.addWidget(self.department_input)

#         layout.addWidget(QLabel("Knowledge Patterns:"))
#         self.knowledge_pattern_input = QComboBox()
#         self.knowledge_pattern_input.addItems(["idea_compass", "keynote", "recommendation", "github_issues", "summary", "All of the above"])
#         layout.addWidget(self.knowledge_pattern_input)

#         upload_btn = QPushButton("Upload Audio File")
#         upload_btn.clicked.connect(self.upload_audio_file)
#         layout.addWidget(upload_btn)

#         self.file_path_label = QLabel("No file selected")
#         layout.addWidget(self.file_path_label)

#         transcribe_btn = QPushButton("Submit Audio and Transcribe")
#         transcribe_btn.clicked.connect(self.transcribe_audio)
#         layout.addWidget(transcribe_btn)

#         self.transcription_text = QTextEdit()
#         self.transcription_text.setReadOnly(True)
#         self.transcription_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Set scroll policy
#         layout.addWidget(self.transcription_text)

#         layout.addStretch()

#         return widget

#     def create_transcript_search(self):
#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         layout.setContentsMargins(30, 20, 30, 20)

#         title = QLabel("Search Transcript")
#         title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
#         title.setStyleSheet("color: #333; margin-bottom: 20px;")
#         layout.addWidget(title)

#         layout.addWidget(QLabel("File Search Directory:"))
#         self.search_input = QLineEdit()
#         self.search_input.setPlaceholderText("Enter file_search_dir")
#         layout.addWidget(self.search_input)

#         search_btn = QPushButton("Search Transcript")
#         search_btn.clicked.connect(self.search_transcript)
#         layout.addWidget(search_btn)

#         self.search_transcription_text = QTextEdit()
#         self.search_transcription_text.setReadOnly(True)
#         self.search_transcription_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Set scroll policy
#         layout.addWidget(self.search_transcription_text)

#         layout.addStretch()

#         return widget

#     def upload_audio_file(self):
#         file_dialog = QFileDialog()
#         file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.m4a)")
#         if file_path:
#             self.file_path_label.setText(f"Selected file: {file_path}")
#             self.audio_file = file_path

#     def transcribe_audio(self):
#         if not self.audio_file:
#             QMessageBox.warning(self, "No File", "Please upload an audio file first.")
#             return

#         # Other required fields
#         language = self.language_input.text()
#         meeting_subject = self.meeting_subject_input.text()
#         department = self.department_input.currentText()
#         selected_pattern = self.knowledge_pattern_input.currentText()

#         if not language or not meeting_subject or not department:
#             QMessageBox.warning(self, "Missing Fields", "Please provide all required fields.")
#             return

#         # Just showing that audio is being transcribed
#         self.transcription_text.setPlainText("Submitting the audio for transcription...")

#         # Simulating the process
#         # Replace this part with the actual API call to your transcription service
#         # Assume the `file_search_dir` is returned by the transcription process

#         # Example file_search_dir (replace with the actual path from your API response)
#         self.file_search_dir = "+Users+traderscafe+Desktop+hakuna-matata+uploads+serendipity+2024-09-19_21-16-04"

#         # Set the transcription text and show that it's transcribed
#         self.transcription_text.setPlainText(f"Audio transcribed successfully! Transcript goes here...")

#         # Switch to the search tab and populate the file_search_dir input field
#         self.search_input.setText(self.file_search_dir)
#         self.show_transcript_search()

#     def search_transcript(self):
#         file_search_dir = self.search_input.text()
#         if not file_search_dir:
#             QMessageBox.warning(self, "Missing Input", "Please enter a file_search_dir.")
#             return

#         # Show loader
#         self.progress_dialog = QProgressDialog("Fetching transcript...", "Cancel", 0, 0, self)
#         self.progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
#         self.progress_dialog.show()

#         # Fetch the transcript using a separate thread
#         self.transcript_thread = TranscriptFetchThread(file_search_dir)
#         self.transcript_thread.finished.connect(self.on_transcript_fetched)
#         self.transcript_thread.error.connect(self.on_transcript_fetch_error)
#         self.transcript_thread.start()

#     def on_transcript_fetched(self, transcript_text):
#         self.progress_dialog.hide()  # Hide the loader
#         self.search_transcription_text.setPlainText(transcript_text)  # Display transcript

#     def on_transcript_fetch_error(self, error_msg):
#         self.progress_dialog.hide()  # Hide the loader
#         QMessageBox.critical(self, "Error", f"Failed to fetch transcript: {error_msg}")

#     def show_meeting_transcriber(self):
#         self.content_stack.setCurrentIndex(0)

#     def show_transcript_search(self):
#         # Populate the search input field with the latest file_search_dir if available
#         if self.file_search_dir:
#             self.search_input.setText(self.file_search_dir)
#         self.content_stack.setCurrentIndex(1)

#     def create_shortcuts(self):
#         QShortcut(QKeySequence("Ctrl+M"), self, activated=self.show_meeting_transcriber)
#         QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

# import sys
# import requests
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
#     QPushButton, QStackedWidget, QComboBox, QLabel, QTextEdit, QMessageBox,
#     QFileDialog, QLineEdit, QProgressDialog
# )
# from PyQt6.QtCore import Qt, QThread, pyqtSignal
# from PyQt6.QtGui import QFont, QShortcut, QKeySequence

# class TranscriptFetchThread(QThread):
#     finished = pyqtSignal(str)  # Emit transcript text when done
#     error = pyqtSignal(str)

#     def __init__(self, file_search_dir):
#         super().__init__()
#         self.file_search_dir = file_search_dir

#     def run(self):
#         try:
#             self.fetch_transcript()
#         except Exception as e:
#             self.error.emit(str(e))

#     def fetch_transcript(self):
#         # Use the file_search_dir directly in the URL
#         url = f"http://115.245.248.122:8051/meeting/wisdom-file/{self.file_search_dir}"
#         print(f"Fetching transcript from: {url}")  # Log URL for debugging

#         response = requests.get(url)
#         if response.status_code == 200:
#             print(f"GET Response Text: {response.text}")  # Print the GET response (transcript)
#             self.finished.emit(response.text)  # Pass transcript text to the main thread
#         else:
#             print(f"GET Error: {response.status_code}, {response.text}")  # Print GET error if any
#             self.error.emit(f"Error fetching transcript: {response.status_code}, {response.text}")

# class RecordingThread(QThread):
#     finished = pyqtSignal(str)  # Emit the file_search_dir when done
#     error = pyqtSignal(str)

#     def __init__(self, audio_file, language, meeting_subject, department, knowledge_patterns):
#         super().__init__()
#         self.audio_file = audio_file
#         self.language = language
#         self.meeting_subject = meeting_subject
#         self.department = department
#         self.knowledge_patterns = knowledge_patterns

#     def run(self):
#         try:
#             self.submit_audio_file()
#         except Exception as e:
#             self.error.emit(str(e))

#     def submit_audio_file(self):
#         url = "http://115.245.248.122:8051/meeting/submit-meeting"
#         files = {'audio_file': open(self.audio_file, 'rb')}
#         data = {'knowledge_patterns': self.knowledge_patterns}
#         params = {
#             'language': self.language,
#             'meeting_subject': self.meeting_subject,
#             'department': self.department
#         }

#         response = requests.post(url, params=params, files=files, data=data)
#         if response.status_code == 200:
#             result = response.json()
#             file_search_dir = result.get('dir_search_path')
#             if file_search_dir:
#                 print(f"POST Response: {file_search_dir}")
#                 self.finished.emit(file_search_dir)  # Emit the new file search path
#             else:
#                 self.error.emit("Failed to retrieve file_search_dir")
#         else:
#             self.error.emit(f"Error: {response.status_code}, {response.text}")

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.file_search_dir = None  # Store file_search_dir here
#         self.init_ui()
#         self.create_shortcuts()

#     def init_ui(self):
#         self.setWindowTitle("Meeting Transcriber")
#         self.setGeometry(200, 100, 1000, 600)  # Adjust window size
#         self.setStyleSheet("""
#             QLabel {
#                 font-size: 14px;
#                 font-family: Arial, sans-serif;
#                 color: #444;
#             }
#             QPushButton {
#                 background-color: #1976D2;
#                 color: white;
#                 padding: 12px 24px;
#                 border-radius: 8px;
#                 font-size: 16px;
#             }
#             QPushButton:hover {
#                 background-color: #1565C0;
#             }
#             QLineEdit, QComboBox, QTextEdit {
#                 padding: 10px;
#                 border-radius: 8px;
#                 border: 1px solid #ccc;
#                 font-size: 14px;
#                 background-color: #FAFAFA;
#                 color: black;
#             }
#             QWidget {
#                 background-color: #F5F5F5;
#             }
#             QStackedWidget {
#                 background-color: #FFF;
#             }
#             QVBoxLayout {
#                 spacing: 15px;
#             }
#         """)

#         central_widget = QWidget()
#         main_layout = QHBoxLayout(central_widget)

#         # Sidebar
#         sidebar = QWidget()
#         sidebar_layout = QVBoxLayout(sidebar)
#         sidebar.setFixedWidth(250)
#         sidebar.setStyleSheet("background-color: #2C3E50; padding: 10px;")

#         meeting_transcriber_btn = QPushButton("Meeting Transcriber")
#         meeting_transcriber_btn.setStyleSheet("background-color: #3498DB; color: white;")
#         sidebar_layout.addWidget(meeting_transcriber_btn)

#         transcript_search_btn = QPushButton("Search Transcript")
#         transcript_search_btn.setStyleSheet("background-color: #3498DB; color: white;")
#         sidebar_layout.addWidget(transcript_search_btn)

#         sidebar_layout.addStretch()

#         self.content_stack = QStackedWidget()
#         self.content_stack.addWidget(self.create_meeting_transcriber())
#         self.content_stack.addWidget(self.create_transcript_search())

#         meeting_transcriber_btn.clicked.connect(self.show_meeting_transcriber)
#         transcript_search_btn.clicked.connect(self.show_transcript_search)

#         main_layout.addWidget(sidebar)
#         main_layout.addWidget(self.content_stack, 1)

#         self.setCentralWidget(central_widget)

#     def create_meeting_transcriber(self):
#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         layout.setContentsMargins(30, 20, 30, 20)  # Add margins

#         title = QLabel("Meeting Transcriber")
#         title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
#         title.setStyleSheet("color: #333; margin-bottom: 20px;")
#         layout.addWidget(title)

#         layout.addWidget(QLabel("Language:"))
#         self.language_input = QLineEdit()
#         self.language_input.setPlaceholderText("Enter language code (e.g., 'en')")
#         layout.addWidget(self.language_input)

#         layout.addWidget(QLabel("Meeting Subject:"))
#         self.meeting_subject_input = QLineEdit()
#         self.meeting_subject_input.setPlaceholderText("Enter meeting subject")
#         layout.addWidget(self.meeting_subject_input)

#         layout.addWidget(QLabel("Department:"))
#         self.department_input = QComboBox()
#         self.department_input.addItems(["trademan", "dhoom Studios", "serendipity"])
#         layout.addWidget(self.department_input)

#         layout.addWidget(QLabel("Knowledge Patterns:"))
#         self.knowledge_pattern_input = QComboBox()
#         self.knowledge_pattern_input.addItems(["idea_compass", "keynote", "recommendation", "github_issues", "summary", "All of the above"])
#         layout.addWidget(self.knowledge_pattern_input)

#         upload_btn = QPushButton("Upload Audio File")
#         upload_btn.clicked.connect(self.upload_audio_file)
#         layout.addWidget(upload_btn)

#         self.file_path_label = QLabel("No file selected")
#         layout.addWidget(self.file_path_label)

#         transcribe_btn = QPushButton("Submit Audio and Transcribe")
#         transcribe_btn.clicked.connect(self.transcribe_audio)
#         layout.addWidget(transcribe_btn)

#         self.transcription_text = QTextEdit()
#         self.transcription_text.setReadOnly(True)
#         self.transcription_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Set scroll policy
#         layout.addWidget(self.transcription_text)

#         layout.addStretch()

#         return widget

#     def create_transcript_search(self):
#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         layout.setContentsMargins(30, 20, 30, 20)

#         title = QLabel("Search Transcript")
#         title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
#         title.setStyleSheet("color: #333; margin-bottom: 20px;")
#         layout.addWidget(title)

#         layout.addWidget(QLabel("File Search Directory:"))
#         self.search_input = QLineEdit()
#         self.search_input.setPlaceholderText("Enter file_search_dir")
#         layout.addWidget(self.search_input)

#         search_btn = QPushButton("Search Transcript")
#         search_btn.clicked.connect(self.search_transcript)
#         layout.addWidget(search_btn)

#         self.search_transcription_text = QTextEdit()
#         self.search_transcription_text.setReadOnly(True)
#         self.search_transcription_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Set scroll policy
#         layout.addWidget(self.search_transcription_text)

#         layout.addStretch()

#         return widget

#     def upload_audio_file(self):
#         file_dialog = QFileDialog()
#         file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.m4a)")
#         if file_path:
#             self.file_path_label.setText(f"Selected file: {file_path}")
#             self.audio_file = file_path

#     def transcribe_audio(self):
#         if not self.audio_file:
#             QMessageBox.warning(self, "No File", "Please upload an audio file first.")
#             return

#         # Other required fields
#         language = self.language_input.text()
#         meeting_subject = self.meeting_subject_input.text()
#         department = self.department_input.currentText()
#         selected_pattern = self.knowledge_pattern_input.currentText()

#         if not language or not meeting_subject or not department:
#             QMessageBox.warning(self, "Missing Fields", "Please provide all required fields.")
#             return

#         # Show the loader dialog
#         self.progress_dialog = QProgressDialog("Submitting audio and transcribing...", "Cancel", 0, 0, self)
#         self.progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
#         self.progress_dialog.show()

#         # Start the audio file submission and transcription
#         self.transcription_thread = RecordingThread(
#             self.audio_file, language, meeting_subject, department, selected_pattern)
#         self.transcription_thread.finished.connect(self.on_transcription_finished)
#         self.transcription_thread.error.connect(self.on_transcription_error)
#         self.transcription_thread.start()

#     def on_transcription_finished(self, file_search_dir):
#         self.progress_dialog.hide()  # Hide loader
#         self.file_search_dir = file_search_dir  # Set the new file search directory
#         self.transcription_text.setPlainText(f"Audio transcribed successfully! File search directory: {file_search_dir}")

#         # Set the search input field with the new file path
#         self.search_input.setText(file_search_dir)

#     def on_transcription_error(self, error_msg):
#         self.progress_dialog.hide()  # Hide loader in case of error
#         QMessageBox.critical(self, "Error", f"Failed to submit audio: {error_msg}")

#     def search_transcript(self):
#         file_search_dir = self.search_input.text()
#         if not file_search_dir:
#             QMessageBox.warning(self, "Missing Input", "Please enter a file_search_dir.")
#             return

#         # Show loader
#         self.progress_dialog = QProgressDialog("Fetching transcript...", "Cancel", 0, 0, self)
#         self.progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
#         self.progress_dialog.show()

#         # Fetch the transcript using a separate thread
#         self.transcript_thread = TranscriptFetchThread(file_search_dir)
#         self.transcript_thread.finished.connect(self.on_transcript_fetched)
#         self.transcript_thread.error.connect(self.on_transcript_fetch_error)
#         self.transcript_thread.start()

#     def on_transcript_fetched(self, transcript_text):
#         self.progress_dialog.hide()  # Hide the loader
#         self.search_transcription_text.setPlainText(transcript_text)  # Display transcript

#     def on_transcript_fetch_error(self, error_msg):
#         self.progress_dialog.hide()  # Hide the loader
#         QMessageBox.critical(self, "Error", f"Failed to fetch transcript: {error_msg}")

#     def show_meeting_transcriber(self):
#         self.content_stack.setCurrentIndex(0)

#     def show_transcript_search(self):
#         # Populate the search input field with the latest file_search_dir if available
#         if self.file_search_dir:
#             self.search_input.setText(self.file_search_dir)
#         self.content_stack.setCurrentIndex(1)

#     def create_shortcuts(self):
#         QShortcut(QKeySequence("Ctrl+M"), self, activated=self.show_meeting_transcriber)
#         QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

import sys
import os
import requests
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QComboBox, QLabel, QTextEdit, QMessageBox,
    QFileDialog, QLineEdit, QProgressDialog, QListWidget, QListWidgetItem,
    QInputDialog, QMenu, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QUrl, QDate
from PyQt6.QtGui import QFont, QShortcut, QKeySequence, QAction  # <-- Update this import
from PyQt6.QtWebEngineWidgets import QWebEngineView
import openai

# Database setup for Kanban board
def init_db():
    conn = sqlite3.connect('app_data.db')
    cursor = conn.cursor()
    # Create table with 'date_added' column if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kanban_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            date_added TEXT
        )
    ''')
    conn.commit()

    # Check if 'date_added' column exists; if not, add it
    cursor.execute("PRAGMA table_info(kanban_tasks)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'date_added' not in columns:
        cursor.execute("ALTER TABLE kanban_tasks ADD COLUMN date_added TEXT")
        conn.commit()

    conn.close()

init_db()

# Define TranscriptFetchThread for handling transcript fetching in a separate thread
class TranscriptFetchThread(QThread):
    finished = pyqtSignal(str)  # Emit transcript text when done
    error = pyqtSignal(str)

    def __init__(self, file_search_dir):
        super().__init__()
        self.file_search_dir = file_search_dir

    def run(self):
        try:
            self.fetch_transcript()
        except Exception as e:
            self.error.emit(str(e))

    def fetch_transcript(self):
        url = f"http://115.245.248.122:8051/meeting/wisdom-file/{self.file_search_dir}"
        response = requests.get(url)
        if response.status_code == 200:
            self.finished.emit(response.text)  # Pass transcript text to the main thread
        else:
            self.error.emit(f"Error fetching transcript: {response.status_code}, {response.text}")

# Define RecordingThread for handling audio submission and transcription in a separate thread
class RecordingThread(QThread):
    finished = pyqtSignal(str)  # Emit the file_search_dir when done
    error = pyqtSignal(str)

    def __init__(self, audio_file, language, meeting_subject, department, knowledge_patterns):
        super().__init__()
        self.audio_file = audio_file
        self.language = language
        self.meeting_subject = meeting_subject
        self.department = department
        self.knowledge_patterns = knowledge_patterns

    def run(self):
        try:
            self.submit_audio_file()
        except Exception as e:
            self.error.emit(str(e))

    def submit_audio_file(self):
        url = "http://115.245.248.122:8051/meeting/submit-meeting"
        with open(self.audio_file, 'rb') as f:
            files = {'audio_file': f}
            data = {'knowledge_patterns': self.knowledge_patterns}
            params = {
                'language': self.language,
                'meeting_subject': self.meeting_subject,
                'department': self.department
            }
            response = requests.post(url, params=params, files=files, data=data)
            if response.status_code == 200:
                result = response.json()
                file_search_dir = result.get('dir_search_path')
                if file_search_dir:
                    self.finished.emit(file_search_dir)
                else:
                    self.error.emit("Failed to retrieve file_search_dir")
            else:
                self.error.emit(f"Error: {response.status_code}, {response.text}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_search_dir = None
        self.init_ui()
        self.create_shortcuts()

    def init_ui(self):
        self.setWindowTitle("Productivity Suite")
        self.setGeometry(200, 100, 1400, 900)
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
                color: #444;
            }
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QLineEdit, QComboBox, QTextEdit {
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 14px;
                background-color: #FAFAFA;
                color: black;
            }
            QComboBox QAbstractItemView {
                color: black;
            }
            QWidget {
                background-color: #FFFFFF;
            }
            QStackedWidget {
                background-color: #FFFFFF;
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ddd;
                color: black;
            }
        """)

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #2C3E50; padding: 10px;")

        buttons_info = [
            ("Meeting Transcriber", self.show_meeting_transcriber),
            ("Search Transcript", self.show_transcript_search),
            ("Kanban Board", self.show_kanban_board),
            ("ChatGPT", self.show_chatgpt),
        ]

        for text, slot in buttons_info:
            btn = QPushButton(text)
            btn.setStyleSheet("background-color: #3498DB; color: white; margin-bottom: 10px;")
            btn.clicked.connect(slot)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self.create_meeting_transcriber())  # Index 0
        self.content_stack.addWidget(self.create_transcript_search())    # Index 1
        self.content_stack.addWidget(self.create_kanban_board())         # Index 2
        self.content_stack.addWidget(self.create_chatgpt_view())         # Index 3

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack, 1)

        self.setCentralWidget(central_widget)

    def create_meeting_transcriber(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("Meeting Transcriber")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addWidget(QLabel("Language:"))
        self.language_input = QLineEdit()
        self.language_input.setPlaceholderText("Enter language code (e.g., 'en')")
        layout.addWidget(self.language_input)

        layout.addWidget(QLabel("Meeting Subject:"))
        self.meeting_subject_input = QLineEdit()
        self.meeting_subject_input.setPlaceholderText("Enter meeting subject")
        layout.addWidget(self.meeting_subject_input)

        layout.addWidget(QLabel("Department:"))
        self.department_input = QComboBox()
        self.department_input.addItems(["trademan", "dhoom Studios", "serendipity"])
        layout.addWidget(self.department_input)

        layout.addWidget(QLabel("Knowledge Patterns:"))
        self.knowledge_pattern_input = QComboBox()
        self.knowledge_pattern_input.addItems(["idea_compass", "keynote", "recommendation", "github_issues", "summary", "All of the above"])
        layout.addWidget(self.knowledge_pattern_input)

        upload_btn = QPushButton("Upload Audio File")
        upload_btn.clicked.connect(self.upload_audio_file)
        layout.addWidget(upload_btn)

        self.file_path_label = QLabel("No file selected")
        layout.addWidget(self.file_path_label)

        transcribe_btn = QPushButton("Submit Audio and Transcribe")
        transcribe_btn.clicked.connect(self.transcribe_audio)
        layout.addWidget(transcribe_btn)

        self.transcription_text = QTextEdit()
        self.transcription_text.setReadOnly(True)
        layout.addWidget(self.transcription_text)

        layout.addStretch()
        return widget

    def create_transcript_search(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("Search Transcript")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addWidget(QLabel("File Search Directory:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter file_search_dir")
        layout.addWidget(self.search_input)

        search_btn = QPushButton("Search Transcript")
        search_btn.clicked.connect(self.search_transcript)
        layout.addWidget(search_btn)

        self.search_transcription_text = QTextEdit()
        self.search_transcription_text.setReadOnly(True)
        layout.addWidget(self.search_transcription_text)

        layout.addStretch()
        return widget

    def create_kanban_board(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Filter Layout
        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter tasks...")
        self.filter_input.textChanged.connect(self.filter_tasks)
        filter_layout.addWidget(QLabel("Filter:"))
        filter_layout.addWidget(self.filter_input)
        layout.addLayout(filter_layout)

        # Kanban Board Layout
        kanban_layout = QHBoxLayout()
        stages = ["To Do", "In Progress", "Done"]
        self.lists = {}

        for stage in stages:
            stage_layout = QVBoxLayout()
            label = QLabel(stage)
            label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            label.setStyleSheet("color: #1976D2;")
            stage_layout.addWidget(label)

            task_list = QListWidget()
            task_list.setAcceptDrops(True)
            task_list.setDragEnabled(True)
            task_list.viewport().setAcceptDrops(True)
            task_list.setDefaultDropAction(Qt.DropAction.MoveAction)
            task_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
            task_list.setStyleSheet("background-color: #F0F0F0;")
            task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            task_list.customContextMenuRequested.connect(self.show_task_context_menu)
            stage_layout.addWidget(task_list)
            self.lists[stage] = task_list

            add_task_btn = QPushButton(f"Add Task to {stage}")
            add_task_btn.clicked.connect(lambda checked, s=stage: self.add_task(s))
            add_task_btn.setStyleSheet("background-color: #1976D2; color: white;")
            stage_layout.addWidget(add_task_btn)

            kanban_layout.addLayout(stage_layout)

        layout.addLayout(kanban_layout)
        self.load_tasks()
        return widget

    def add_task(self, stage):
        text, ok = QInputDialog.getText(self, 'Add Task', 'Task Name:')
        if ok and text:
            current_date = QDate.currentDate().toString("yyyy-MM-dd")
            item_text = f"{text} (Added on: {current_date})"
            item = QListWidgetItem(item_text)
            self.lists[stage].addItem(item)
            self.save_task_to_db(text, stage, current_date)

    def save_task_to_db(self, title, status, date_added):
        conn = sqlite3.connect('app_data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO kanban_tasks (title, status, date_added) VALUES (?, ?, ?)', (title, status, date_added))
        conn.commit()
        conn.close()

    def load_tasks(self):
        conn = sqlite3.connect('app_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT title, status, date_added FROM kanban_tasks')
        tasks = cursor.fetchall()
        conn.close()
        for title, status, date_added in tasks:
            if status in self.lists:
                item = QListWidgetItem(f"{title} (Added on: {date_added})")
                self.lists[status].addItem(item)

    def filter_tasks(self):
        filter_text = self.filter_input.text().lower()
        for stage, task_list in self.lists.items():
            for i in range(task_list.count()):
                item = task_list.item(i)
                item.setHidden(filter_text not in item.text().lower())

    def show_task_context_menu(self, pos):
        list_widget = self.sender()
        item = list_widget.itemAt(pos)
        if item:
            menu = QMenu(self)
            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)

            edit_action.triggered.connect(lambda: self.edit_task(item))
            delete_action.triggered.connect(lambda: self.delete_task(item, list_widget))

            menu.addAction(edit_action)
            menu.addAction(delete_action)
            menu.exec(list_widget.mapToGlobal(pos))

    def edit_task(self, item):
        new_text, ok = QInputDialog.getText(self, 'Edit Task', 'New Task Name:', text=item.text())
        if ok and new_text:
            item.setText(new_text)

    def delete_task(self, item, list_widget):
        list_widget.takeItem(list_widget.row(item))
        self.delete_task_from_db(item.text())

    def delete_task_from_db(self, title):
        conn = sqlite3.connect('app_data.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM kanban_tasks WHERE title = ?', (title,))
        conn.commit()
        conn.close()

    def create_chatgpt_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        label = QLabel("ChatGPT")
        label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(label)

        self.chatgpt_view = QWebEngineView()
        self.chatgpt_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        chatgpt_url = QUrl.fromUserInput("https://chat.openai.com")
        self.chatgpt_view.load(chatgpt_url)

        layout.addWidget(self.chatgpt_view)
        return widget

    def transcribe_audio(self):
        if not hasattr(self, 'audio_file') or not self.audio_file:
            QMessageBox.warning(self, "No File", "Please upload an audio file first.")
            return

        language = self.language_input.text()
        meeting_subject = self.meeting_subject_input.text()
        department = self.department_input.currentText()
        selected_pattern = self.knowledge_pattern_input.currentText()

        if not language or not meeting_subject or not department:
            QMessageBox.warning(self, "Missing Fields", "Please provide all required fields.")
            return

        self.progress_dialog = QProgressDialog("Submitting audio and transcribing...", "Cancel", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress_dialog.show()

        self.transcription_thread = RecordingThread(
            self.audio_file, language, meeting_subject, department, selected_pattern
        )
        self.transcription_thread.finished.connect(self.on_transcription_finished)
        self.transcription_thread.error.connect(self.on_transcription_error)
        self.transcription_thread.start()

    def on_transcription_finished(self, file_search_dir):
        self.progress_dialog.hide()
        self.file_search_dir = file_search_dir
        self.transcription_text.setHtml(f"<h2>Transcribed Text</h2><p style='font-size: 14px;'>{file_search_dir}</p>")
        self.content_stack.setCurrentIndex(1)
        self.search_input.setText(file_search_dir)

    def on_transcription_error(self, error_msg):
        self.progress_dialog.hide()
        QMessageBox.critical(self, "Error", f"Failed to submit audio: {error_msg}")

    def search_transcript(self):
        file_search_dir = self.search_input.text()
        if not file_search_dir:
            QMessageBox.warning(self, "Missing Input", "Please enter a file_search_dir.")
            return

        self.progress_dialog = QProgressDialog("Fetching transcript...", "Cancel", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress_dialog.show()

        self.transcript_thread = TranscriptFetchThread(file_search_dir)
        self.transcript_thread.finished.connect(self.on_transcript_fetched)
        self.transcript_thread.error.connect(self.on_transcript_fetch_error)
        self.transcript_thread.start()

    def on_transcript_fetched(self, transcript_text):
        self.progress_dialog.hide()
        self.search_transcription_text.setHtml(f"<h2>Transcript</h2><p style='font-size: 14px;'>{transcript_text}</p>")

    def on_transcript_fetch_error(self, error_msg):
        self.progress_dialog.hide()
        QMessageBox.critical(self, "Error", f"Failed to fetch transcript: {error_msg}")

    def upload_audio_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.m4a)")
        if file_path:
            self.file_path_label.setText(f"Selected file: {file_path}")
            self.audio_file = file_path

    def show_meeting_transcriber(self):
        self.content_stack.setCurrentIndex(0)

    def show_transcript_search(self):
        if self.file_search_dir:
            self.search_input.setText(self.file_search_dir)
        self.content_stack.setCurrentIndex(1)

    def show_kanban_board(self):
        self.content_stack.setCurrentIndex(2)

    def show_chatgpt(self):
        self.content_stack.setCurrentIndex(3)

    def create_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+M"), self, activated=self.show_meeting_transcriber)
        QShortcut(QKeySequence("Ctrl+K"), self, activated=self.show_kanban_board)
        QShortcut(QKeySequence("Ctrl+C"), self, activated=self.show_chatgpt)
        QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
