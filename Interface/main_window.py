import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import sys
import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, 'youtube_api'))  # Adds youtube_api to path
import youtube

youtube = youtube.Youtube()

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

class SplitWindow(QMainWindow):
    selected_keywords = set()  # Set to store selected keywords

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 1920, 1080)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget(splitter)

        left_widget.setStyleSheet("background-color: lightblue")
        left_widget.setMinimumWidth(300)

        left_layout = QVBoxLayout(left_widget)
        left_widget.setLayout(left_layout)

        title_label = QLabel("Video Collection", left_widget)
        title_label.setFont(QFont("Roboto", 20))
        title_label.setMinimumWidth(650)
        title_label.setAlignment(Qt.AlignCenter)

        filter_frame = QFrame()
        filter_frame.setFrameShape(QFrame.StyledPanel)
        filter_layout = QVBoxLayout(filter_frame)

        keyword_label = QLabel("Keywords")
        keyword_label.setFont(QFont("Roboto", 14))
        filter_layout.addWidget(keyword_label)

        self.predefined_keywords = ["explained", "tutorial", "demo"]
        self.predefined_checkboxes = []

        for keyword in self.predefined_keywords:
            checkbox = QCheckBox(keyword)
            checkbox.setFont(QFont("Roboto", 12))
            checkbox.stateChanged.connect(self.updateSelectedKeywords)
            self.predefined_checkboxes.append(checkbox)
            filter_layout.addWidget(checkbox)


        left_layout.addWidget(title_label)
        left_layout.addWidget(filter_frame)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setFrameShadow(QFrame.Plain)
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        scroll_area.setWidget(content_widget)

        left_layout.addWidget(line)
        left_layout.addWidget(scroll_area)

        splitter.addWidget(left_widget)
        central_layout.addWidget(splitter)

        self.updateVideoList(youtube.search())

    def playVideo(self, id):
        embed_code = f'<iframe width="900" height="600" src="https://www.youtube.com/embed/{id}?hl=en" frameborder="0" allowfullscreen></iframe>'
        popup = QDialog(self)
        popup.setWindowTitle("YouTube Video")
        popup.setMinimumSize(950, 650)
        layout = QVBoxLayout(popup)
        playArea = QWebEngineView()
        playArea.setHtml(embed_code)
        layout.addWidget(playArea)
        popup.setLayout(layout)
        popup.exec_()

    def updateSelectedKeywords(self):
        self.selected_keywords.clear()
        for checkbox in self.predefined_checkboxes:
            if checkbox.isChecked():
                self.selected_keywords.add(checkbox.text())
        self.applyKeywordFilter()

    def applyKeywordFilter(self):
        selected_keywords = list(self.selected_keywords)  # Convert set to list

        if not selected_keywords:  # If no keywords are selected, show all 12 videos
            self.updateVideoList(youtube.search())
        else:
            filtered_videos = [video for video in youtube.search() if any(keyword in video.title.lower() for keyword in selected_keywords)]
            self.updateVideoList(filtered_videos)

    def updateVideoList(self, filtered_videos):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for video in filtered_videos:
            video_entry = VideoEntry(video)
            video_entry.clicked.connect(self.playVideo)
            self.content_layout.addWidget(video_entry)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplitWindow()
    window.showMaximized()
    sys.exit(app.exec_())
