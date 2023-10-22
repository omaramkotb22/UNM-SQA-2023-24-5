import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Class for video
class Video:
    def __init__(self, image_path, title, video_id):
        self.image_path = image_path
        self.title = title
        self.video_id = video_id

class VideoEntry(QWidget):
    def __init__(self, video):
        super().__init__()
        self.video = video
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # label for the image
        image_label = QLabel()
        image = QImage(self.video.image_path)
        image = image.scaledToWidth(400)  
        image_label.setPixmap(QPixmap.fromImage(image))

        # label for the title
        title_label = QLabel(self.video.title)
        title_label.setFont(QFont("Times New Roman", 18))

        # Add both the image and title labels to the horizontal layout
        layout.addWidget(image_label)
        layout.addWidget(title_label)

        self.setLayout(layout)
class SplitWindow(QMainWindow):
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
        right_widget = QWidget(splitter)

        left_widget.setStyleSheet("background-color: lightblue")
        left_widget.setMinimumWidth(300)

        left_layout = QVBoxLayout(left_widget)
        left_widget.setLayout(left_layout)

        title_label = QLabel("Video Collection", left_widget)
        title_label.setFont(QFont("Times New Roman", 20))
        title_label.setMinimumWidth(650)
        title_label.setAlignment(Qt.AlignCenter)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)  # Set the frame shape to NoFrame
        scroll_area.setFrameShadow(QFrame.Plain) 
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        scroll_area.setWidget(content_widget)

        # Create Video instances and add them to the content layout
        videos = [
            Video("Interface/mordo.jpg", "Video 1 Title", "video1"),
            Video("Interface/mordo.jpg", "Video 2 Title", "video2"),
            Video("Interface/mordo.jpg", "Video 3 Title", "video3"),
            Video("Interface/mordo.jpg", "Video 4 Title", "video4"),
            Video("Interface/mordo.jpg", "Video 5 Title", "video5"),
            Video("Interface/mordo.jpg", "Video 6 Title", "video6"),
            Video("Interface/mordo.jpg", "Video 7 Title", "video7"),
            Video("Interface/mordo.jpg", "Video 8 Title", "video8"),
            Video("Interface/mordo.jpg", "Video 9 Title", "video9"),
            Video("Interface/mordo.jpg", "Video 10 Title", "video10"),
            Video("Interface/mordo.jpg", "Video 11 Title", "video11"),
            Video("Interface/mordo.jpg", "Video 12 Title", "video12"),
        ]

        for video in videos:
            video_entry = VideoEntry(video)
            content_layout.addWidget(video_entry)

        left_layout.addWidget(title_label)
        left_layout.addWidget(line)
        left_layout.addWidget(scroll_area)

        right_widget.setStyleSheet("background-color: lightgray")

        right_label = QLabel("Currently Playing:", right_widget)
        right_label.setFont(QFont("Times New Roman", 20))
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(right_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        right_widget.setLayout(right_layout)
        

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        splitter.setSizes([300, 500])

        central_layout.addWidget(splitter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplitWindow()
    window.showMaximized()
    sys.exit(app.exec_())
