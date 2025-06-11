from PyQt5 import QtGui, QtCore
import sys
import os

def create_crosshair_png(filename, width=1920, height=1080, line_color=(0, 255, 0), line_width=2):
    # Create a transparent image
    image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)
    image.fill(QtCore.Qt.transparent)

    # Draw the crosshair
    painter = QtGui.QPainter(image)
    pen = QtGui.QPen(QtGui.QColor(*line_color), line_width)
    painter.setPen(pen)

    center_x = width // 2
    center_y = height // 2
    painter.drawLine(0, center_y, width, center_y)       # Horizontal
    painter.drawLine(center_x, 0, center_x, height)      # Vertical
    painter.end()

    # Ensure output directory exists
    os.makedirs("overlays", exist_ok=True)
    full_path = os.path.join("overlays", filename)
    image.save(full_path)
    print(f"✅ Saved overlay: {full_path}")

if __name__ == "__main__":
    app = QtGui.QGuiApplication(sys.argv)

    # Example: Generate multiple styles
    create_crosshair_png("crosshair_green.png", line_color=(0, 255, 0))
    create_crosshair_png("crosshair_red.png", line_color=(255, 0, 0))
    create_crosshair_png("crosshair_white_thick.png", line_color=(255, 255, 255), line_width=4)
