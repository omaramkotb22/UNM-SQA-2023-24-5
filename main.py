from youtube_api import youtube
from Interface.VideoPlayer.video_player import YoutubePlayer
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys


yt = youtube.Youtube("AIzaSyD6Wp2WzfDrSnnpOq-Mxb2m3QDFfisBlqY")

ls = yt.search("Software Quality Assurance", 12)

video = random.choice(ls)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YoutubePlayer(video_id=video['id'])
    window.show()
    sys.exit(app.exec_())


