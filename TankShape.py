import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import QRect, Qt

class CylinderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tank Level Monitoring")
        self.setGeometry(100, 100, 500, 400)
        self.tank_level = 0.5  # Initial tank level (75%)
        self.tank_name = "Tank 1"  # Tank name

    def setTankLevel(self, level):
        self.tank_level = level
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set background color to white
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 0, self.width(), self.height())

        # Set color of the tank
        tank_color = QColor(176, 176, 176)  # Light gray color
        painter.setBrush(tank_color)
        pen = QPen(tank_color, 2)  # Black color, pen width 2
        painter.setPen(pen)

        # Draw tank shape
        tank_width = 200
        tank_height = 300
        tank_x = (self.width() - tank_width) // 2
        tank_y = (self.height() - tank_height) // 2

        # Fill top ellipse
        painter.drawEllipse(QRect(int(tank_x), int(tank_y), int(tank_width), int(tank_width // 2)))

        # Fill bottom ellipse
        painter.drawEllipse(QRect(int(tank_x), int(tank_y + tank_height - tank_width // 2), int(tank_width), int(tank_width // 2)))

        # Draw curved sides
        painter.drawRect(int(tank_x), int(tank_y + tank_width // 4), int(tank_width), int(tank_height - tank_width // 2))

        # Define colors for different level ranges
        colors = {
            (0, 25): QColor("#94C816"),   # Green
            (25, 50): QColor("#EBA104"),  # Yellow
            (50, 75): QColor("#E4670B"),  # Orange
            (75, 100): QColor("#BA1301")  # Red
        }

        # Draw tank level indicator line with different colors based on tank level percentage
        level_x = tank_x + tank_width + 70
        level_height = tank_height

        for (start, end), color in colors.items():
            line_color = color
            start_y = tank_y + tank_height * start / 100
            end_y = tank_y + tank_height * end / 100
            painter.setPen(QPen(line_color, 8))
            painter.drawLine(int(level_x), int(start_y), int(level_x), int(end_y))  # Vertical line


        # Draw tank level indicator
        level_indicator_height = 5  # Height of the indicator rectangle
        level_indicator_width = 20  # Width of the indicator rectangle
        level_indicator_y = int(tank_y + tank_height * (1 - self.tank_level))
        level_indicator_x = int(tank_x + tank_width + 60)  # Adjust the position of the indicator
        painter.setPen(Qt.black)  # Set the pen color to black
        painter.setBrush(Qt.black)  # Set the brush color to black
        painter.drawRect(level_indicator_x, level_indicator_y - level_indicator_height // 2, level_indicator_width, level_indicator_height)  # Draw the indicator rectangle

        # Draw tank level labels
        font = QFont("Arial", 15)
        painter.setFont(font)
        painter.setPen(QPen(QColor(0,0,0), 8))
        painter.drawText(level_x + 8, tank_y + tank_height + 15, "0%")  # 0% label
        painter.drawText(level_x + 8, tank_y - 5, "100%")  # 100% label

        # Draw tank name
        painter.drawText(tank_x + 80, tank_y + tank_height + 30, self.tank_name)

        # Draw tank level
        painter.drawText(level_x+20, level_indicator_y - level_indicator_height // 2, f"{int(self.tank_level * 100)}%")
        painter.drawText(tank_x + 40, tank_y + tank_height-320, f"Tank Level={int(self.tank_level * 100)}%")

        # Draw tank level indicator line
        tank_level_y = tank_y + tank_height * (1 - self.tank_level)
        painter.setPen(QPen(QColor(200,200,200), 5)) # Set pen color and width
        painter.drawLine(int(tank_x+2), int(tank_level_y), int(tank_x+tank_width-2), int(tank_level_y))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CylinderWidget()
    window.show()
    sys.exit(app.exec_())
