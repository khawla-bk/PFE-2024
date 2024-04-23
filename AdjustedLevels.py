import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import QRect, Qt

class CylinderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tank Level Monitoring")
        self.setGeometry(100, 100, 500, 400)
        self.tank_level = 0 # Tank level value
        self.tank_name = "Tank 1"  # Tank name

    def setTankLevel(self, level):
        self.tank_level = level
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set background color to white
        painter.setBrush(QColor(4, 12, 36))
        painter.drawRect(0, 0, self.width(), self.height())

        # Set color of the tank
        tank_color = QColor(165, 165, 165)  # Light gray color
        painter.setBrush(tank_color)
        pen = QPen(tank_color, 2)
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
        if 0 <= self.tank_level < 0.26:
            painter.setPen(QColor("#BA1301"))
            painter.setBrush(QColor("#BA1301"))
        elif 0.25 <= self.tank_level < 0.51:
            painter.setPen(QColor("#E4670B"))
            painter.setBrush(QColor("#E4670B"))
        elif 0.5 <= self.tank_level < 0.76:
            painter.setPen(QColor("#EBA104"))
            painter.setBrush(QColor("#EBA104"))
        elif 0.75 <= self.tank_level <= 1.0:
            painter.setPen(QColor("#94C816"))
            painter.setBrush(QColor("#94C816"))

        painter.drawRect(level_indicator_x, level_indicator_y - level_indicator_height // 2, level_indicator_width, level_indicator_height)  # Draw the indicator rectangle

        # Draw tank level labels
        font = QFont("Arial", 15)
        painter.setFont(font)
        painter.setPen(QPen(QColor(194,221,228), 8))
        painter.drawText(level_x + 8, tank_y + tank_height + 15, "0%")  # 0% label
        painter.drawText(level_x + 8, tank_y - 5, "100%")  # 100% label

        # Draw tank name
        painter.drawText(tank_x + 80, tank_y + tank_height + 30, self.tank_name)

        # Draw tank level
        if 0 <= self.tank_level < 0.26:
            painter.setPen(QColor("#BA1301"))
            painter.setBrush(QColor("#BA1301"))
            if self.tank_level==0:
                painter.drawText(tank_x, tank_y + tank_height-320, f"Tank Level={int(self.tank_level * 100)}% : EMPTY TANK")
            else:
                painter.drawText(tank_x, tank_y + tank_height-320, f"Tank Level={int(self.tank_level * 100)}% : CRITICAL")
        elif 0.25 <= self.tank_level < 0.51:
            painter.setPen(QColor("#E4670B"))
            painter.setBrush(QColor("#E4670B"))
            painter.drawText(tank_x, tank_y + tank_height-320, f"Tank Level={int(self.tank_level * 100)}% : MODERATE")
        elif 0.5 <= self.tank_level < 0.76:
            painter.setPen(QColor("#EBA104"))
            painter.setBrush(QColor("#EBA104"))
            painter.drawText(tank_x, tank_y + tank_height-320, f"Tank Level={int(self.tank_level * 100)}% : GOOD")
        elif 0.75 <= self.tank_level <= 1.0:
            painter.setPen(QColor("#94C816"))
            painter.setBrush(QColor("#94C816"))
            if self.tank_level==1:
                painter.drawText(tank_x, tank_y + tank_height-320, f"Tank Level={int(self.tank_level * 100)}% : FULL TANK")
            else:
                painter.drawText(tank_x, tank_y + tank_height-320, f"Tank Level={int(self.tank_level * 100)}% : HIGH")
        
        painter.drawText(level_x+20, level_indicator_y - level_indicator_height // 2, f"{int(self.tank_level * 100)}%")

        # Draw tank level indicator shape
        tank_fill_height = tank_height * self.tank_level  # Calculate the height of the filled area
        tank_fill_y = tank_y + tank_height - tank_fill_height  # Calculate the y-coordinate of the filled area

        """if self.tank_level <= 0.3:  # If the tank level is 30% or less
            # Draw only the bottom ellipse for the filled area
            painter.drawEllipse(QRect(int(tank_x), int(tank_y + tank_height - tank_width // 2), int(tank_width), int(tank_width // 2)))"""
        
        """if self.tank_level <= 0.29 and self.tank_level>0.19:  # If the tank level is 30% or less
            # Calculate the height and width of the bottom ellipse
            bottom_ellipse_height = tank_height * self.tank_level * 1.2  # Adjusting the factor (1.5) to fit visually
            # Draw the bottom ellipse for the filled area
            painter.drawEllipse(QRect(int(tank_x), int(tank_y + tank_height - bottom_ellipse_height), int(tank_width), int(bottom_ellipse_height)))
        
        elif self.tank_level<=0.19:
            bottom_ellipse_height = tank_height * self.tank_level * 1.2  # Adjusting the factor (1.5) to fit visually
            bottom_ellipse_width = tank_width*3/4 # Adjusting the factor (1.5) to fit visually
            # Draw the bottom ellipse for the filled area
            painter.drawEllipse(QRect(int(tank_x + (tank_width - bottom_ellipse_width) / 2), int(tank_y + tank_height - bottom_ellipse_height), int(bottom_ellipse_width), int(bottom_ellipse_height)))"""
        
        if self.tank_level <= 0.29 and self.tank_level > 0.19:  # If the tank level is between 20% and 30%
            # Calculate the height and width of the bottom ellipse
            bottom_ellipse_height = tank_height * self.tank_level * 1.2  # Adjusting the factor (1.5) to fit visually
            # Draw the bottom ellipse for the filled area
            painter.drawEllipse(QRect(int(tank_x), int(tank_y + tank_height - bottom_ellipse_height), int(tank_width), int(bottom_ellipse_height)))

        elif self.tank_level <= 0.19:  # If the tank level is 19% or less
            bottom_ellipse_height = tank_height * self.tank_level * 1.2  # Adjusting the factor (1.5) to fit visually
            bottom_ellipse_width = tank_width * 3 / 4  # Adjusting the factor to fit visually
            if self.tank_level==0:
                pass
            else:
                # Draw the bottom ellipse for the filled area
                painter.drawEllipse(QRect(int(tank_x + (tank_width - bottom_ellipse_width) / 2), int(tank_y + tank_height - bottom_ellipse_height), int(bottom_ellipse_width), int(bottom_ellipse_height)))

            
        else:
            # Draw the top ellipse of the filled area
            painter.drawEllipse(QRect(int(tank_x), int(tank_fill_y), int(tank_width), int(tank_width // 2)))

            # Limit the filled area to the lower edge of the bottom ellipse
            bottom_ellipse_bottom_y = tank_y + tank_height  # Y-coordinate of the bottom edge of the bottom ellipse
            if tank_fill_y + tank_fill_height > bottom_ellipse_bottom_y:
                tank_fill_height = bottom_ellipse_bottom_y - tank_fill_y

            # Draw the bottom ellipse of the filled area
            painter.drawEllipse(QRect(int(tank_x), int(tank_fill_y + tank_fill_height - tank_width // 2), int(tank_width), int(tank_width // 2)))

            # Draw the curved sides of the filled area
            painter.drawRect(int(tank_x), int(tank_fill_y + tank_width // 4), int(tank_width), int(tank_fill_height - tank_width // 2))




        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CylinderWidget()
    window.show()
    sys.exit(app.exec_())