import os, random
import ctypes
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia

class FullScreenCrosshair(QtWidgets.QWidget):
    roll_requested = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowDoesNotAcceptFocus |
            QtCore.Qt.ToolTip |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint 
            
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setGeometry(QtWidgets.QApplication.primaryScreen().geometry())

        self.overlays = self.load_overlays()
        self.crosshair_pixmap = None

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.roll_tick)

        self.roll_sequence = []
        self.roll_index = 0

        self.crate_sound = self.load_sound('crate_open.wav')

        self.roll_requested.connect(self.start_crate_roll)

        self.show()
        hwnd = int(self.winId())
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, 0x00000080 | 0x00000020)  # WS_EX_TRANSPARENT | WS_EX_LAYERED

    def load_overlays(self):
        path = 'overlays'
        return [os.path.join(path, f) for f in os.listdir(path)
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    def load_sound(self, path):
        effect = QtMultimedia.QSoundEffect()
        effect.setSource(QtCore.QUrl.fromLocalFile(path))
        return effect

    def start_crate_roll(self):
        if not self.overlays: return
        self.crate_sound.play()
        self.roll_sequence = self.generate_roll_timing()
        self.roll_index = 0
        self.roll_tick()

    def generate_roll_timing(self, duration_ms=7000, min_interval=30, max_interval=300):
        sequence, elapsed, t = [], 0, 0
        while elapsed < duration_ms:
            step = min_interval + int((max_interval - min_interval) * (t / 100) ** 2)
            sequence.append(step)
            elapsed += step
            t += 1
        return sequence

    def roll_tick(self):
        if self.roll_index < len(self.roll_sequence):
            self.crosshair_pixmap = QtGui.QPixmap(random.choice(self.overlays))
            self.update()
            QtCore.QTimer.singleShot(self.roll_sequence[self.roll_index], self.roll_tick)
            self.roll_index += 1
        else:
            self.crosshair_pixmap = QtGui.QPixmap(random.choice(self.overlays))
            self.update()

    def paintEvent(self, event):
        if self.crosshair_pixmap:
            painter = QtGui.QPainter(self)
            x = (self.width() - self.crosshair_pixmap.width()) // 2
            y = (self.height() - self.crosshair_pixmap.height()) // 2
            painter.drawPixmap(x, y, self.crosshair_pixmap)
