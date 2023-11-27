import pytest
from Interface.main_window import SplitWindow
from PyQt5.QtWidgets import QApplication


@pytest.fixture
def video_app():
    app = QApplication([])
    window = SplitWindow()
    yield window
    window.close()
    

def test_predefined_keywords_exists(video_app):
    # Check if the SplitWindow instance is created properly
    assert video_app is not None

    # Now check if predefined_keywords attribute is available
    predefined_keywords = getattr(video_app, 'predefined_keywords', None)

    assert predefined_keywords is not None
    assert isinstance(predefined_keywords, list)
    assert all(isinstance(keyword, str) for keyword in predefined_keywords)
    assert len(predefined_keywords) > 0

if __name__ == "__main__":
    pytest.main()