# video_entry.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import pyqtSignal, Qt
import requests
import pyperclip

class VideoEntry(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, video):
        super().__init__()
        self.video = video
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        image_label = QLabel(self)
        response = requests.get(self.video.image_path)
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        image_label.setPixmap(pixmap)

        title_label = QLabel(self.video.title)
        title_label.setFont(QFont("Roboto", 18))
        image_label.mousePressEvent = lambda event: (self.clicked.emit(self.video.video_id))

        layout.addWidget(image_label)
        layout.addWidget(title_label)
        self.setLayout(layout)
