import os

from PySide6.QtCore import QObject, Signal, Slot, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class AudioPlayer(QObject):
    handleError = Signal(str)
    finished = Signal()
    
    def __init__(self, path: str):
        super().__init__()
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Audio file not found: {path}")
        
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(path))
        self.audio_output.setVolume(50)

        self.bind()
    
    def bind(self) -> None:
        def fEmit(status):
            if status == QMediaPlayer.MediaStatus.EndOfMedia:
                self.finished.emit()
        self.player.errorOccurred.connect(lambda: self.handleError.emit(f"Cannot play: {self.player.errorString()}"))
        self.player.mediaStatusChanged.connect(fEmit)
    
    def play(self) -> None:
        self.player.play()
    
    def stop(self) -> None:
        self.player.stop()

    def pause(self) -> None:
        self.player.pause()
