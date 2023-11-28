
import sys
from PyQt5.QtWidgets import *

from PyQt5.QtGui import *

from PyQt5.QtCore import *

import pyperclip


from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import requests
import sqlite3
import pyperclip
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, 'youtube_api'))  # Adds youtube_api to path
db_path = os.path.join(parent_dir, 'Notes.db')  
import youtube

youtube = youtube.Youtube()


def copyURL(id):
    url = f'https://www.youtube.com/watch?v={id}'
    pyperclip.copy(url)
    print("url copied to clipboard")
    

# adds video widget (thumbnail + title) in collection
class VideoEntry(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, video):

        super().__init__() # Inherits from the constructor of the QWidget class

        self.video = video # Video object

        self.initUI() # Call the initUI method to initialize the user interface


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
        self.custom_keyword_edit = QLineEdit()
        self.setWindowTitle("Video Player")

        self.setGeometry(100, 100, 1920, 1080)

        self.search = youtube.search

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


        self.setupFilterSection(left_layout)
        self.setupVideoCollectionSection(left_layout)

        splitter.addWidget(left_widget)
        central_layout.addWidget(splitter)

        self.updateVideoList(youtube.search())

    def setupFilterSection(self, layout):
        title_label = QLabel("Video Collection", self)
        title_label.setFont(QFont("Roboto", 20))
        title_label.setMinimumWidth(650)

        title_label.setAlignment(Qt.AlignCenter)


        filter_frame = QFrame()
        filter_frame.setFrameShape(QFrame.StyledPanel)
        self.filter_layout = QVBoxLayout(filter_frame)

        keyword_label = QLabel("Keywords")
        keyword_label.setFont(QFont("Roboto", 14))
        self.filter_layout.addWidget(keyword_label)

        self.filter_layout.addWidget(self.custom_keyword_edit)

        add_keyword_button = QPushButton("Add Keyword")
        add_keyword_button.clicked.connect(self.addCustomKeyword)
        self.filter_layout.addWidget(add_keyword_button)

        self.predefined_keywords = ["explained", "tutorial", "demo"]
        self.predefined_checkboxes = []

        for keyword in self.predefined_keywords:
            checkbox = QCheckBox(keyword)
            checkbox.setFont(QFont("Roboto", 12))
            checkbox.stateChanged.connect(self.updateSelectedKeywords)
            self.predefined_checkboxes.append(checkbox)
            self.filter_layout.addWidget(checkbox)

        layout.addWidget(title_label)
        layout.addWidget(filter_frame)

    def setupVideoCollectionSection(self, layout):
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
        layout.addWidget(line)
        layout.addWidget(scroll_area)

    def addCustomKeyword(self):
        custom_keyword = self.custom_keyword_edit.text().strip()
        if custom_keyword:
            # Add the custom keyword to the predefined list and create a new checkbox
            self.predefined_keywords.append(custom_keyword)
            self.addCheckboxForCustomKeyword(custom_keyword)

    def addCheckboxForCustomKeyword(self, custom_keyword):
        checkbox = QCheckBox(custom_keyword)
        checkbox.setFont(QFont("Roboto", 12))
        checkbox.stateChanged.connect(self.updateSelectedKeywords)
        self.predefined_checkboxes.append(checkbox)
        self.filter_layout.addWidget(checkbox)

    def updateSelectedKeywords(self):
        self.selected_keywords.clear()

        # Check predefined checkboxes
        for checkbox in self.predefined_checkboxes:
            if checkbox.isChecked():
                self.selected_keywords.add(checkbox.text())
        # Apply the keyword filter
        self.applyKeywordFilter()

    def applyKeywordFilter(self):
        selected_keywords = list(self.selected_keywords)  # Convert set to list

        if not selected_keywords:  # If no keywords are selected, show all 12 videos
            print("No keywords selected. Showing all videos.")
            self.updateVideoList(youtube.search())
        else:
            selected_keywords_string = str(selected_keywords)
            print(selected_keywords_string)
            self.updateVideoList(youtube.search(selected_keywords_string))

    def updateVideoList(self, filtered_videos):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for video in filtered_videos:
            video_entry = VideoEntry(video)
            video_entry.clicked.connect(self.playVideo)
            self.content_layout.addWidget(video_entry)

    def playVideo(self, id):
        embed_code = f'''
        <!DOCTYPE html>
            <html>
            <body>
            <iframe 
                width="900" 
                height="600" 
                src="https://www.youtube.com/embed/{id}?hl=en" 
                frameborder="0" 
                allowfullscreen>
            </iframe>
            </body>
            </html>
        '''
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

        self.playArea = QWebEngineView()
        self.playArea.setHtml(embed_code)

        splitter2.addWidget(self.playArea)
        splitter2.addWidget(noteFrame)
        splitter2.setSizes([900, 500])
        copy_button = QPushButton("Copy URL", self)
        copy_button.setFont(QFont("Roboto", 12))
        copy_button.setStyleSheet("background-color: lightblue")
        copy_button.resize(100, 32)
        copy_button.move(900, 600)
        copy_button.clicked.connect(lambda: copyURL(id))
        layout.addWidget(copy_button)
        layout.addWidget(splitter2)
        popup.setLayout(layout)
        popup.exec_()

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
                    for i in reversed(range(self.containerLayout.count())):
                        widget = self.containerLayout.itemAt(i).widget()
                        if widget:
                            widget.deleteLater()

                    for note in notes:
                        self.textArea = QTextEdit()
                        self.textArea.lineWrapColumnOrWidth = 50
                        self.copyNoteButton = QPushButton("Copy")
                        self.textArea.setText(note[0])
                        # copylist.append(note[0])
                        string = note[0]
                        self.copyNoteButton.clicked.connect(lambda _,s=string : pyperclip.copy(s))
                        self.containerLayout.addWidget(self.textArea) 
                        self.containerLayout.addWidget(self.copyNoteButton)

                self.textArea = QTextEdit()
                self.textArea.lineWrapColumnOrWidth = 50
                self.containerLayout.addWidget(self.textArea)
                self.saveButton.setText("Save")

            else:
                if notes:
                    for note in notes:
                        self.textArea = QTextEdit()
                        self.textArea.lineWrapColumnOrWidth = 50
                        self.copyNoteButton = QPushButton("Copy")
                        self.containerLayout.addWidget(self.textArea)
                        self.textArea.setText(note[0])
                        string = note[0]
                        self.copyNoteButton.clicked.connect(lambda _,s=string: pyperclip.copy(s))
                        self.containerLayout.addWidget(self.textArea)
                        self.containerLayout.addWidget(self.copyNoteButton)
            add = False

    def checkVideoTime(self):
        # Get the current video time (in seconds)
        script = """
        var player = document.querySelector('iframe');
        var currentTime = player.contentWindow.document.querySelector('video').currentTime;
        currentTime;
        """
        self.playArea.page().runJavaScript(script, self.handleVideoTime)

    def handleVideoTime(self, result):
        # Handle the current video time
        current_time = int(result)
        if current_time >= self.event_time_threshold:
            print(f"Event occurred at {current_time} seconds.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplitWindow()
    window.showMaximized()
    sys.exit(app.exec_())