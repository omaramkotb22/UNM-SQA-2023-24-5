import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

class YoutubePlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Player")
        self.setGeometry(100, 100, 800, 600)

        # Create widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)
        self.layout.addWidget(self.play_button)

        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

    def play_video(self):
        video_id = self.url_input.text()
        embed_code = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
        self.web_view.setHtml(embed_code)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YoutubePlayer()
    window.show()
    sys.exit(app.exec_())
