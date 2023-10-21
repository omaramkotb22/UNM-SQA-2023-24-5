import sys
sys.path.append('/Users/yenzinhlabatsi/Documents/UNM-SQA-2023-24---5-1/youtube_api')    #append path to include youtube api
import youtube
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

#Class for video
class Video:
    def __init__(self, image_path, title, video_url):
        self.image_path = image_path
        self.title = title
        self.video_url = video_url

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
        image_label.clicked.connect(self.playVideo(self.video.video_url)) #sends url of video to be displayed

        # label for the title
        title_label = QLabel(self.video.title)
        title_label.setFont(QFont("Times New Roman", 18))

        # Add both the image and title labels to the horizontal layout
        layout.addWidget(image_label)
        layout.addWidget(title_label)

        self.setLayout(layout)
class SplitWindow(QMainWindow):
    
    #list of videos and thei info (filled in by youtube api)
    global videos_list
    videos_list = []
    
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

        # Add videos from youtube search to layout
        for video in videos_list:
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
        playArea = QWebEngineView()
        right_layout.addWidget(playArea)    #dedicated play area (initially blank)
        right_widget.setLayout(right_layout)
        

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        splitter.setSizes([300, 500])

        central_layout.addWidget(splitter)
     
     #embed selected video onto dedicated play area   
    def playVideo(self, link):
        embed_code = f'<iframe width="560" height="315" src={link} frameborder="0" allowfullscreen></iframe>'
        playArea.setHtml(embed_code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplitWindow()
    window.showMaximized()
    sys.exit(app.exec_())