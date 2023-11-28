import pytest
from Interface.main_window import SplitWindow
from PyQt5.QtWidgets import QApplication

@pytest.fixture
def video_app():
    # Setup: Create a QApplication and SplitWindow instance
    app = QApplication([])
    window = SplitWindow()
    yield window
    # Teardown: Close the SplitWindow instance
    window.close()

# Requirement 3.1
# Check if the predefined keywords exists when app is launched
def test_predefined_keywords_exists(video_app):
    # Check if the SplitWindow instance is created properly
    assert video_app is not None

    # Now check if predefined_keywords attribute is available
    predefined_keywords = getattr(video_app, 'predefined_keywords', None)

    assert predefined_keywords is not None
    assert isinstance(predefined_keywords, list)
    assert all(isinstance(keyword, str) for keyword in predefined_keywords)
    assert len(predefined_keywords) > 0




# Requirement 3.2.1
# Simulate interaction with checkboxes
@pytest.mark.parametrize("selected_keywords", [["explained"], ["tutorial", "demo"], []])
def test_select_deselect_keywords(video_app, selected_keywords):

    # Simulate selecting and deselecting checkboxes
    for keyword in video_app.predefined_checkboxes:
        keyword.setChecked(keyword.text() in selected_keywords)

    # Trigger the updateSelectedKeywords method
    video_app.updateSelectedKeywords()

    # Check if the selected_keywords set in the SplitWindow instance is as expected
    assert set(video_app.selected_keywords) == set(selected_keywords)


# Requirement 3.2.2 - Additional Test
# Check if the video list is updated based on the selected keywords
def test_update_video_list_based_on_keywords(video_app):
    
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





# Requirement 3.3.1
# Simulate user adding a new custom keyword
@pytest.mark.parametrize("custom_keyword", ["CS2", "CSGO"])
def test_add_custom_keyword(video_app, custom_keyword):
    # Set the text in the custom_keyword_edit QLineEdit
    video_app.custom_keyword_edit.setText(custom_keyword)

    # Trigger the addCustomKeyword method
    video_app.addCustomKeyword()

    # Check if the custom_keyword is added to the predefined_keywords
    assert custom_keyword in video_app.predefined_keywords

#  Requirement 3.3.2
#  Additional Test for Empty Custom Keyword
def test_add_empty_custom_keyword(video_app):
    # Set the custom_keyword_edit to an empty string
    video_app.custom_keyword_edit.setText("")

    # Trigger the addCustomKeyword method
    video_app.addCustomKeyword()

    # Check if an empty custom_keyword is not added to the predefined_keywords
    assert "" not in video_app.predefined_keywords

if __name__ == "__main__":
    pytest.main()
