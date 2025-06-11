import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class FullScreenOverlay(QtWidgets.QWidget):
    def __init__(self, gif_path):
        super().__init__()

        # Get full screen geometry
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        # Make the window frameless, transparent, always on top, and non-interactive
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        # Load GIF using QMovie
        self.movie = QtGui.QMovie(gif_path)
        self.movie.start()

        # Create a label to display the GIF
        self.label = QtWidgets.QLabel(self)
        self.label.setMovie(self.movie)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # Show the window
        self.show()
        
        QtCore.QTimer.singleShot(2465, self.cleanup)

    def resizeEvent(self, event):
        # Resize the label to fit the window size
        self.label.resize(self.size())

    def cleanup(self):
        self.movie.stop()
        self.close()
        QtWidgets.QApplication.quit()

# Replace 'your_animation.gif' with the path to your GIF file
gif_path = 'flash.gif'  # Example: Replace with your GIF file path

app = QtWidgets.QApplication(sys.argv)
overlay = FullScreenOverlay(gif_path)
sys.exit(app.exec_())
