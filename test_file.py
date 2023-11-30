from typing import Literal
import pytest
from selenium import webdriver
from Interface.main_window import SplitWindow
from Interface.main_window import VideoEntry
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QPoint

@pytest.fixture
def video_app():
    # Setup: Create a QApplication and SplitWindow instance
    app = QApplication([])
    window = SplitWindow()
    yield window
    # Teardown: Close the SplitWindow instance
    window.close()
    
#------------------------------------------------------------------------------------------------------------

# Requirement 1.1
# Check that there are 12 videos displayed when app is launched   
def test_video_collection(video_app: SplitWindow):
    assert video_app is not None
    video_collection = getattr(video_app, 'filtered_videos')
    assert len(video_collection) == 12

#------------------------------------------------------------------------------------------------------------

# Requirement 1.2
# Check if the displayed videos have thumbnails and titles
def test_collection_display(video_app: SplitWindow):
    assert video_app is not None
    video_collection = getattr(video_app, 'filtered_videos')
    for video in video_collection:
        assert VideoEntry(video).image_label is not None
        assert VideoEntry(video).title_label is not None

#------------------------------------------------------------------------------------------------------------

# Requirement 2.1
# Clicking the aforementioned thumbnail must diplay videoplayer -------- Note: passes (when run individually) but does not automatically  close gui (cuases segmentation fault)
def test_video_play(video_app: SplitWindow):
    if video_app.video_entry.clicked.emit('xtQpNdGK6WI'):
        video_app.close()
        pass
    

#------------------------------------------------------------------------------------------------------------

# Requirement 2.2
# Check if the video player has pause, play, and back/next buttons ------- Note: fails due to CORS policy
def test_button_presence(video_app: SplitWindow):
    video_app.video_entry.clicked.emit('xtQpNdGK6WI')
    script = """
        var playButton = document.querySelector('button.ytp-large-play-button');
        playButton != null;
        """
    result = video_app.playArea.page().runJavaScript(script)

    assert result

#------------------------------------------------------------------------------------------------------------

# Requirement 3.1
# Check if the predefined keywords exists when app is launched
def test_predefined_keywords_exists(video_app: SplitWindow):
    # Check if the SplitWindow instance is created properly
    assert video_app is not None

    # Now check if predefined_keywords attribute is available
    predefined_keywords = getattr(video_app, 'predefined_keywords', None)

    assert predefined_keywords is not None
    assert isinstance(predefined_keywords, list)
    assert all(isinstance(keyword, str) for keyword in predefined_keywords)
    assert len(predefined_keywords) > 0


#------------------------------------------------------------------------------------------------------------

# Requirement 3.2
# Simulate interaction with checkboxes
@pytest.mark.parametrize("selected_keywords", [["explained"], ["tutorial", "demo"], []])
def test_select_deselect_keywords(video_app: SplitWindow, selected_keywords: list[str] | list[object]):

    # Simulate selecting and deselecting checkboxes
    for keyword in video_app.predefined_checkboxes:
        keyword.setChecked(keyword.text() in selected_keywords)

    # Trigger the updateSelectedKeywords method
    video_app.updateSelectedKeywords()

    # Check if the selected_keywords set in the SplitWindow instance is as expected
    assert set(video_app.selected_keywords) == set(selected_keywords)


# Requirement 3.2 - continued
# Check if the video list is updated based on the selected keywords
def test_update_video_list_based_on_keywords(video_app: SplitWindow):
    
    # Get the initial list of videos
    initial_video_list = video_app.search()
 
    # Simulate selecting checkboxes for "explained" and "tutorial"
    for keyword in video_app.predefined_checkboxes:
        if keyword.text() in ["explained", "tutorial"]:
            keyword.setChecked(True)
        else:
            keyword.setChecked(False)

    # Trigger the updateSelectedKeywords method
    video_app.updateSelectedKeywords()

    # Get the updated list of videos
    updated_video_list = video_app.search()

    # Check if the list of videos is updated based on the selected keywords
    assert initial_video_list != updated_video_list

#------------------------------------------------------------------------------------------------------------


# Requirement 3.3
# Simulate user adding a new custom keyword
@pytest.mark.parametrize("custom_keyword", ["CS2", "CSGO"])
def test_add_custom_keyword(video_app: SplitWindow, custom_keyword: Literal['CS2', 'CSGO']):
    # Set the text in the custom_keyword_edit QLineEdit
    video_app.custom_keyword_edit.setText(custom_keyword)

    # Trigger the addCustomKeyword method
    video_app.addCustomKeyword()

    # Check if the custom_keyword is added to the predefined_keywords
    assert custom_keyword in video_app.predefined_keywords

# Requirement 3.3 - Additional Test for Empty Custom Keyword
def test_add_empty_custom_keyword(video_app: SplitWindow):
    # Set the custom_keyword_edit to an empty string
    video_app.custom_keyword_edit.setText("")

    # Trigger the addCustomKeyword method
    video_app.addCustomKeyword()

    # Check if an empty custom_keyword is not added to the predefined_keywords
    assert "" not in video_app.predefined_keywords

#------------------------------------------------------------------------------------------------------------

#Requirement xyz
def test_notes_exist_for_video(video_app: SplitWindow):
    # Check if the SplitWindow instance is created properly
    assert video_app is not None

    # Replace 'video_id_to_test' with the actual video ID you want to test
    video_id_to_test = 'xtQpNdGK6WI'

    # Now check if notes attribute is available for the specific video
    notes_for_video = video_app.checkDB(video_id_to_test)

    # Assert that notes_for_video is not None and has at least one note
    assert notes_for_video is not None, f"No notes found for video ID: {video_id_to_test}"
    assert len(notes_for_video) > 0, f"No notes found for video ID: {video_id_to_test}"

    # Check that all notes are strings
    assert all(isinstance(note[0], str) for note in notes_for_video), "Notes should be strings"



if __name__ == "__main__":
    pytest.main()
