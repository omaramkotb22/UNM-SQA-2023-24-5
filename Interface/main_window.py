
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
sys.path.append(os.path.join(parent_dir, 'youtube_api')) #adds youtube_api to path
import youtube

youtube = youtube.Youtube()

# Class for video
# class Video:
#     def __init__(self, image_path, title, video_id):
#         self.image_path = image_path
#         self.title = title
#         self.video_id = video_id


class VideoEntry(QWidget):
    clicked = pyqtSignal(str)
    def __init__(self, video):
        super().__init__() # Inherits from the constructor of the QWidget class
        self.video = video # Video object
        self.initUI() # Call the initUI method to initialize the user interface

    def initUI(self):
        layout = QHBoxLayout()
        # label for the image
        image_label = QLabel(self) # creates label
        response = requests.get(self.video.image_path) # gets image from url
        image_data = response.content # gets image data
        pixmap = QPixmap()
        pixmap.loadFromData(image_data) #sets image to pixmap
        image_label.setPixmap(pixmap) #sets image to label
        # label for the title
        title_label = QLabel(self.video.title)
        title_label.setFont(QFont("Roboto", 18))
        image_label.mousePressEvent = lambda event: (self.clicked.emit(self.video.video_id))

        # Add both the image and title labels to the horizontal layout
        layout.addWidget(image_label)
        layout.addWidget(title_label)

        self.setLayout(layout)
class SplitWindow(QMainWindow):
    #list of videos and their info (filled in by youtube api)
    global videos_list
    videos_list = youtube.search()  #searches for videos with "Software Quality Assurance" in the title
    for video in videos_list:
        print(video.title)
        print(video.video_id)
        print(video.image_path)
        print()
    def __init__(self):
        super().__init__() # Inherits from the constructor of the QMainWindow class

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 1920, 1080)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget(splitter)
        # right_widget = QWidget(splitter)

        left_widget.setStyleSheet("background-color: lightblue")
        left_widget.setMinimumWidth(300)

        left_layout = QVBoxLayout(left_widget)
        left_widget.setLayout(left_layout)

        title_label = QLabel("Video Collection", left_widget)
        title_label.setFont(QFont("Roboto", 20))
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
            video_entry.clicked.connect(self.playVideo)
            content_layout.addWidget(video_entry)
            

        left_layout.addWidget(title_label)
        left_layout.addWidget(line)
        left_layout.addWidget(scroll_area)

        # right_widget.setStyleSheet("background-color: lightgray")

        # right_label = QLabel("Currently Playing:", right_widget)
        # right_label.setFont(QFont("Roboto", 20))
        # right_layout = QVBoxLayout(right_widget)
        # right_layout.addWidget(right_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        # playArea = QWebEngineView()
        # right_layout.addWidget(playArea)    #dedicated play area (initially blank)
        # right_widget.setLayout(right_layout)
        

        splitter.addWidget(left_widget)
        # splitter.addWidget(right_widget)

        splitter.setSizes([300, 500])

        central_layout.addWidget(splitter)
     
     #embed selected video onto dedicated play area   
    def playVideo(self, id):
            embed_code = f'<iframe width="900" height="600" src="https://www.youtube.com/embed/{id}?hl=en" frameborder="0" allowfullscreen></iframe>'

            # Create a popup with a dedicated play area
            popup = QDialog(self)
            popup.setWindowTitle("YouTube Video")
            popup.setMinimumSize(950, 650)
            layout = QVBoxLayout(popup)
            playArea = QWebEngineView()
            playArea.setHtml(embed_code)
            layout.addWidget(playArea)
            popup.setLayout(layout)
            popup.exec_()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplitWindow()
    window.showMaximized()
    sys.exit(app.exec_())