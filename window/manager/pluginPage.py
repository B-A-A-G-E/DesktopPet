from PySide6.QtWidgets import QWidget

from tool.config import ConfigManager
from tool.widgetFactory import SearchStackFactory

class PluginPage(SearchStackFactory):
    def __init__(self):
        super().__init__(None, None)
