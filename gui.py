from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from file_operations import create_archive, extract_archive, get_archive_size_and_compression
import os

class CreateArchiveThread(QThread):
    finished_signal = pyqtSignal(str, float)

    def __init__(self, archive_name, file_paths):
        super().__init__()
        self.archive_name = archive_name
        self.file_paths = file_paths

    def run(self):
        create_archive(self.archive_name, self.file_paths)
        original_size, compressed_size = get_archive_size_and_compression(self.archive_name, self.file_paths)
        compression_ratio = (1 - compressed_size / original_size) * 100
        self.finished_signal.emit(self.archive_name, compression_ratio)

class ExtractArchiveThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, archive_name, extract_path):
        super().__init__()
        self.archive_name = archive_name
        self.extract_path = extract_path

    def run(self):
        extract_archive(self.archive_name, self.extract_path)
        self.finished_signal.emit()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ISTziper")
        self.setGeometry(100, 100, 300, 200)

        # Установка иконки приложения
        self.setWindowIcon(QIcon('1234.png'))
        self.setWindowTitle("ISTziper")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.status_label = QLabel("Ready to work", self)
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        self.create_files_button = QPushButton("Create Archive from Files", self)
        self.create_files_button.clicked.connect(self.create_files_archive_gui)
        layout.addWidget(self.create_files_button)

        self.create_folder_button = QPushButton("Create Archive from Folder", self)
        self.create_folder_button.clicked.connect(self.create_folder_archive_gui)
        layout.addWidget(self.create_folder_button)

        self.extract_button = QPushButton("Extract Archive", self)
        self.extract_button.clicked.connect(self.extract_archive_gui)
        layout.addWidget(self.extract_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_files_archive_gui(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if file_paths:
            self.process_archive_creation(file_paths)

    def create_folder_archive_gui(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.process_archive_creation([folder_path])

    def process_archive_creation(self, paths):
        archive_name, _ = QFileDialog.getSaveFileName(self, "Save Archive", filter="Zip files (*.zip)")
        if archive_name:
            self.progress_bar.show()
            self.create_files_button.setEnabled(False)
            self.create_folder_button.setEnabled(False)
            self.extract_button.setEnabled(False)
            self.status_label.setText("Creating Archive...")
            self.progress_bar.setRange(0, 0)  # Indeterminate mode

            self.thread = CreateArchiveThread(archive_name, paths)
            self.thread.finished_signal.connect(self.on_archive_creation_done)
            self.thread.start()

    def on_archive_creation_done(self, archive_name, compression_ratio):
        self.progress_bar.hide()
        self.create_files_button.setEnabled(True)
        self.create_folder_button.setEnabled(True)
        self.extract_button.setEnabled(True)
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.status_label.setText(
            f"Done! Archive: {os.path.basename(archive_name)}, Compression: {compression_ratio:.2f}%")

    def extract_archive_gui(self):
        archive_name, _ = QFileDialog.getOpenFileName(self, "Open Archive", filter="Zip files (*.zip)")
        if archive_name:
            extract_path = QFileDialog.getExistingDirectory(self, "Select Extract Directory")
            if extract_path:
                self.progress_bar.show()
                self.create_files_button.setEnabled(False)
                self.create_folder_button.setEnabled(False)
                self.extract_button.setEnabled(False)
                self.status_label.setText("Extracting...")
                self.progress_bar.setRange(0, 0)  # Indeterminate mode

                self.extract_thread = ExtractArchiveThread(archive_name, extract_path)
                self.extract_thread.finished_signal.connect(self.on_extraction_done)
                self.extract_thread.start()

    def on_extraction_done(self):
        self.progress_bar.hide()
        self.create_files_button.setEnabled(True)
        self.create_folder_button.setEnabled(True)
        self.extract_button.setEnabled(True)
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.status_label.setText("Done!")

