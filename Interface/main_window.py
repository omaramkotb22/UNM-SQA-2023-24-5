import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import requests
import sqlite3

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, 'youtube_api'))  # Adds youtube_api to path
db_path = os.path.join(parent_dir, 'Notes.db')  
import youtube

youtube = youtube.Youtube()

# adds video widget (thumbnail + title) in collection
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

    # popup video player (appears when video in collection clicked)
    def playVideo(self, id):
        embed_code = f'<iframe width="900" height="600" src="https://www.youtube.com/embed/{id}?hl=en" frameborder="0" allowfullscreen></iframe>'
        popup = QDialog(self)
        popup.setWindowTitle("YouTube Video")
        popup.setMinimumSize(1450, 650)
        layout = QHBoxLayout(popup)
        splitter2 = QSplitter(Qt.Horizontal)
        
        noteFrame = QFrame()
        self.noteLayout = QVBoxLayout(noteFrame)
        label = QLabel("Notepad")
        label.setFont(QFont("Roboto", 18))
        self.noteLayout.addWidget(label)
        
        self.noteView = QScrollArea()
        self.noteView.setWidgetResizable(True)
        self.noteView.setFrameShape(QFrame.NoFrame)
        self.noteView.setFrameShadow(QFrame.Plain)
        self.noteContainer = QWidget()
        self.containerLayout = QVBoxLayout(self.noteContainer)
        self.noteView.setWidget(self.noteContainer)
        self.noteLayout.addWidget(self.noteView)
        self.notesDisplay(self.checkDB(id), False)
        
        self.saveButton = QPushButton(noteFrame, text="Save")
        self.noteLayout.addWidget(self.saveButton)
        self.saveButton.clicked.connect(lambda: self.saveNote(id, self.saveButton))
        addButton = QPushButton(noteFrame, text="Add Note")
        addButton.clicked.connect(lambda: self.notesDisplay(self.checkDB(id), True))
        self.noteLayout.addWidget(addButton)
        
        playArea = QWebEngineView()
        playArea.setHtml(embed_code)
        
        splitter2.addWidget(playArea)
        splitter2.addWidget(noteFrame)
        splitter2.setSizes([900, 500])
        
        layout.addWidget(splitter2)
        popup.setLayout(layout)
        popup.exec_()

    # filter video collection based on keywords
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
    
    def checkDB(self, id):
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        cursor.execute('select Note from Video_Notes where id = ?', (id,))
        result = cursor.fetchall()
        if result:
            return result
         
    def saveNote(self, id, saveButton):
        note = self.textArea.toPlainText()
        try:
            db = sqlite3.connect(db_path)
            cursor = db.cursor()
            data_tuple = (id, note)
            cursor.execute('insert into Video_Notes values (?,?)', data_tuple)
            db.commit()
            saveButton.setText("Saved")
            cursor.close()

        finally:
            if db:
                db.close()

    def notesDisplay(self, notes, add):
        if add:
            if notes:
                i = 0
                while i < len(notes):
                    widget = self.containerLayout.itemAt(i).widget()
                    if widget:
                        widget.deleteLater()
                    i += 1
                    
                for x in notes:
                    self.textArea = QTextEdit()
                    self.textArea.lineWrapColumnOrWidth = 50
                    self.textArea.setText(x[0])
                    self.containerLayout.addWidget(self.textArea)
            self.textArea = QTextEdit()
            self.textArea.lineWrapColumnOrWidth = 50
            self.containerLayout.addWidget(self.textArea)
            self.saveButton.setText("Save")
        else:
            if notes:
                for x in notes:
                    self.textArea = QTextEdit()
                    self.textArea.lineWrapColumnOrWidth = 50
                    self.textArea.setText(x[0])
                    self.containerLayout.addWidget(self.textArea)
        
        add = False
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplitWindow()
    window.showMaximized()
    sys.exit(app.exec_())