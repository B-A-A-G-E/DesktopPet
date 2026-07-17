from PySide6.QtWidgets import QWidget

from tool.widgetFactory import SearchStackFactory

class DocPage(SearchStackFactory):
    def __init__(self):
        super().__init__(None, None)
