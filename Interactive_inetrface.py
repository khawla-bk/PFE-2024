import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QComboBox
)
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QIcon
from PyQt5.QtCore import QRect, QSize, Qt, QTimer
from sensor_simulation import get_pressure

class CylinderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tank Level Monitoring")
        self.setGeometry(100, 100, 700, 600)
        self.setWindowIcon(QIcon('IrWise.png'))
        self.tank_level = 0.0  # Initial tank level (percentage)
        self.tank_name = "Tank 1"  # Tank name
        self.liquid_type = "Essence Sans Plomb"  # Default liquid type
        self.density = 0.74  # Default density
        self.radius = 1.0  # Default radius
        self.pressure = 0.0  # Initial pressure
        self.height = 3.0 # Tank Height
        self.initUI()

        # Set up a timer to update the pressure periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePressure)
        self.timer.start(3000)  # Update every 3 seconds

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.tank_display = TankDisplayWidget(self)
        self.layout.addWidget(self.tank_display)
        
        self.info_layout = QHBoxLayout()
                
        self.volume_label = QLabel("Volume: 0.0 m³")
        self.volume_label.setStyleSheet("font-size: 16px;padding: 10px")
        self.info_layout.addWidget(self.volume_label)
        
        self.level_label = QLabel("Level: 0.0 %")
        self.level_label.setStyleSheet("font-size: 16px;padding: 10px")
        self.info_layout.addWidget(self.level_label)
        
        self.layout.addLayout(self.info_layout)
        self.setLayout(self.layout)

        self.button_layout = QHBoxLayout()

        self.parameter_btn = QPushButton("Configure")
        self.parameter_btn.setStyleSheet("background-color: #C2DDE4; color: #040C24;")
        self.parameter_btn.setStyleSheet("font-size: 15px;padding: 5px; color: #111212")
        self.parameter_btn.setIcon(QIcon('parameter.png'))
        self.parameter_btn.setIconSize(QSize(40, 40))
        self.parameter_btn.setFixedSize(120, 50)
        self.parameter_btn.clicked.connect(self.showSettings)
        self.button_layout.addWidget(self.parameter_btn, alignment=Qt.AlignCenter)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def updatePressure(self):
        self.pressure = get_pressure()
        self.updateCalculations()
        self.updateLabelColors()

    def updateLabelColors(self):
        if 0 <= self.tank_level < 0.26:
            color = "#BA1301"
        elif 0.25 <= self.tank_level < 0.51:
            color = "#E4670B"
        elif 0.5 <= self.tank_level < 0.76:
            color = "#EBA104"
        elif 0.75 <= self.tank_level <= 1.0:
            color = "#94C816"
        
        self.volume_label.setStyleSheet(f"font-size: 16px; color: {color}; padding: 10px;")
        self.level_label.setStyleSheet(f"font-size: 16px; color: {color}; padding: 10px;")

    def showSettings(self):
        self.settings_widget = SettingsWidget(self)
        self.settings_widget.show()

    def setTankLevel(self, level):
        self.tank_level = level
        self.tank_display.update()  # Trigger repaint

    def updateCalculations(self):
        # Perform calculations based on current pressure, density, and radius
        g = 9.81  # Acceleration due to gravity in m/s^2
        height = self.pressure / (self.density * g)  # Calculate the height of the liquid column
        area = 3.14159 * (self.radius ** 2)  # Calculate the area of the tank base
        tank_volume = area * self.height  # Assuming tank height is 3 meters
        volume = area * height  # Calculate the volume of the liquid
        if volume >= 0 and volume <= tank_volume:
            self.tank_level = volume / tank_volume  # Update tank level as a percentage
            self.volume = volume  # Update volume
            self.tank_display.update()  # Trigger repaint
            self.volume_label.setText(f"Volume: {self.volume:.2f} m³")
            self.level_label.setText(f"Level: {self.tank_level * 100:.2f} %")
            self.tank_display.update()  # Trigger repaint
        else:
            pass
        

class TankDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cylinder_widget = parent
        self.setMinimumSize(700, 500)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set background color to blue
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
        level_indicator_y = int(tank_y + tank_height * (1 - self.cylinder_widget.tank_level))
        level_indicator_x = int(tank_x + tank_width + 60)  # Adjust the position of the indicator
        if 0 <= self.cylinder_widget.tank_level < 0.26:
            painter.setPen(QColor("#BA1301"))
            painter.setBrush(QColor("#BA1301"))
        elif 0.25 <= self.cylinder_widget.tank_level < 0.51:
            painter.setPen(QColor("#E4670B"))
            painter.setBrush(QColor("#E4670B"))
        elif 0.5 <= self.cylinder_widget.tank_level < 0.76:
            painter.setPen(QColor("#EBA104"))
            painter.setBrush(QColor("#EBA104"))
        elif 0.75 <= self.cylinder_widget.tank_level <= 1.0:
            painter.setPen(QColor("#94C816"))
            painter.setBrush(QColor("#94C816"))

        painter.drawRect(level_indicator_x, level_indicator_y - level_indicator_height // 2, level_indicator_width, level_indicator_height)  # Draw the indicator rectangle

        # Draw tank level labels
        font = QFont("Arial", 15)
        painter.setFont(font)
        painter.setPen(QPen(QColor(194, 221, 228), 8))
        painter.drawText(level_x + 5, tank_y + tank_height + 25, "0%")  # 0% label
        painter.drawText(level_x + 5, tank_y - 20, "100%")  # 100% label

        # Draw tank name
        painter.drawText(tank_x + 80, tank_y + tank_height + 30, self.cylinder_widget.tank_name)

        # Draw liquid type
        if self.cylinder_widget.liquid_type == "Essence Sans Plomb":
            painter.drawText(tank_x + 10, tank_y + tank_height + 60, self.cylinder_widget.liquid_type)
        elif self.cylinder_widget.liquid_type == "LPG":
            painter.drawText(tank_x + 90, tank_y + tank_height + 60, self.cylinder_widget.liquid_type)
        elif self.cylinder_widget.liquid_type == "Gasoil 50":
            painter.drawText(tank_x + 60, tank_y + tank_height + 60, self.cylinder_widget.liquid_type)
        else:
            painter.drawText(tank_x + 30, tank_y + tank_height + 60, self.cylinder_widget.liquid_type)

        # Draw tank level
        if 0 <= self.cylinder_widget.tank_level < 0.26:
            painter.setPen(QColor("#BA1301"))
            painter.setBrush(QColor("#BA1301"))
            if self.cylinder_widget.tank_level == 0:
                painter.drawText(tank_x - 20, tank_y + tank_height - 322, f"Tank Level={int(self.cylinder_widget.tank_level * 100)}% : EMPTY TANK")
            else:
                painter.drawText(tank_x - 20, tank_y + tank_height - 322, f"Tank Level={int(self.cylinder_widget.tank_level * 100)}% : CRITICAL")
        elif 0.25 <= self.cylinder_widget.tank_level < 0.51:
            painter.setPen(QColor("#E4670B"))
            painter.setBrush(QColor("#E4670B"))
            painter.drawText(tank_x - 20, tank_y + tank_height - 322, f"Tank Level={int(self.cylinder_widget.tank_level * 100)}% : MODERATE")
        elif 0.5 <= self.cylinder_widget.tank_level < 0.76:
            painter.setPen(QColor("#EBA104"))
            painter.setBrush(QColor("#EBA104"))
            painter.drawText(tank_x - 20, tank_y + tank_height - 322, f"Tank Level={int(self.cylinder_widget.tank_level * 100)}% : GOOD")
        elif 0.75 <= self.cylinder_widget.tank_level <= 1.0:
            painter.setPen(QColor("#94C816"))
            painter.setBrush(QColor("#94C816"))
            if self.cylinder_widget.tank_level == 1:
                painter.drawText(tank_x-20, tank_y + tank_height-322, f"Tank Level={int(self.cylinder_widget.tank_level * 100)}% : FULL TANK")
            else:
                painter.drawText(tank_x-20, tank_y + tank_height-322, f"Tank Level={int(self.cylinder_widget.tank_level * 100)}% : HIGH")
        
        painter.drawText(level_x + 20, level_indicator_y - level_indicator_height // 2, f"{int(self.cylinder_widget.tank_level * 100)}%")

        # Draw tank level indicator shape
        tank_fill_height = tank_height * self.cylinder_widget.tank_level  # Calculate the height of the filled area
        tank_fill_y = tank_y + tank_height - tank_fill_height  # Calculate the y-coordinate of the filled area


        if self.cylinder_widget.tank_level <= 0.29 and self.cylinder_widget.tank_level > 0.19:  # If the tank level is between 20% and 30%
            # Calculate the height and width of the bottom ellipse
            bottom_ellipse_height = tank_height * self.cylinder_widget.tank_level * 1.2  # Adjusting the factor (1.2) to fit visually
            # Draw the bottom ellipse for the filled area
            painter.drawEllipse(QRect(int(tank_x), int(tank_y + tank_height - bottom_ellipse_height), int(tank_width), int(bottom_ellipse_height)))

        elif self.cylinder_widget.tank_level <= 0.19 and self.cylinder_widget.tank_level> 0:  # If the tank level is 19% or less
            if self.cylinder_widget.tank_level>0.09 and self.cylinder_widget.tank_level<=0.19:
                bottom_ellipse_height = tank_height * self.cylinder_widget.tank_level * 1.2  # Adjusting the factor (1.2) to fit visually
                bottom_ellipse_width = tank_width * 3 / 4  # Adjusting the factor to fit visually
            elif self.cylinder_widget.tank_level>0.02 and self.cylinder_widget.tank_level<=0.09:
                bottom_ellipse_height = tank_height * self.cylinder_widget.tank_level * 1.2   # Adjusting the factor (1.2) to fit visually
                bottom_ellipse_width = tank_width * 0.4  # Adjusting the factor to fit visually
            elif self.cylinder_widget.tank_level>0 and self.cylinder_widget.tank_level<=0.02:
                bottom_ellipse_height = tank_height * self.cylinder_widget.tank_level * 1.2   # Adjusting the factor (1.2) to fit visually
                bottom_ellipse_width = tank_width * 0.3  # Adjusting the factor to fit visually
            # Draw the bottom ellipse for the filled area
            painter.drawEllipse(QRect(int(tank_x + (tank_width - bottom_ellipse_width) / 2), int(tank_y + tank_height - bottom_ellipse_height), int(bottom_ellipse_width), int(bottom_ellipse_height)))
        
        elif self.cylinder_widget.tank_level == 0:
            pass   
            
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


class SettingsWidget(QWidget):

    def __init__(self, parent_widget):
        super().__init__()
        self.cylinder_widget = parent_widget  # Store the parent widget (CylinderWidget)
        self.setWindowTitle("Settings")
        #self.setStyleSheet("background-color: #a5a5a5")
        self.setWindowIcon(QIcon('IrWise.png')) 
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setText(str(self.cylinder_widget.tank_name))
        self.layout.addSpacing(10)
        self.layout.addWidget(self.createLabel("Tank Name"))
        self.name_input.setStyleSheet("color: #000000; font-size: 10pt; font-family: Arial, sans-serif;")
        self.layout.addWidget(self.name_input)

        self.density_input = QComboBox()
        self.density_input.addItem("Essence Sans Plomb", 0.74)
        self.density_input.addItem("Gasoil (Diesel)", 0.85)
        self.density_input.addItem("Gasoil 50", 0.85)
        self.density_input.addItem("LPG", 0.51)
        self.setDensityValue(self.cylinder_widget.density)  # Set initial selection
        self.layout.addSpacing(10)
        self.layout.addWidget(self.createLabel("Select Liquid Type"))
        self.density_input.setStyleSheet("color: #000000; font-size: 10pt; font-family: Arial, sans-serif;")
        self.layout.addWidget(self.density_input)

        self.radius_input = QLineEdit()
        self.radius_input.setText(str(self.cylinder_widget.radius))
        self.layout.addSpacing(10)
        self.layout.addWidget(self.createLabel("Tank Radius (m)"))
        self.radius_input.setStyleSheet("color: #000000; font-size: 10pt; font-family: Arial, sans-serif;")
        self.layout.addWidget(self.radius_input)

        self.height_input = QLineEdit()
        self.height_input.setText(str(self.cylinder_widget.height))
        self.layout.addSpacing(10)
        self.layout.addWidget(self.createLabel("Tank Height (m)"))
        self.height_input.setStyleSheet("color: #000000; font-size: 10pt; font-family: Arial, sans-serif;")
        self.layout.addWidget(self.height_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.saveSettings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def createLabel(self, text):
        label = QLabel(text)
        label.setStyleSheet("color: #000000; font-size: 11pt; font-family: Arial, sans-serif;")
        return label
        
    def setDensityValue(self, density):
        # Set the current index of the QComboBox based on density value
        index = self.density_input.findData(density)
        if index != -1:
            self.density_input.setCurrentIndex(index)
        self.setLayout(self.layout)

    def saveSettings(self):
        self.cylinder_widget.liquid_type = self.density_input.currentText()
        self.cylinder_widget.tank_name= self.name_input.text()
        self.cylinder_widget.density = float(self.density_input.currentData())
        self.cylinder_widget.radius = float(self.radius_input.text())
        self.cylinder_widget.height = float(self.height_input.text())
        self.cylinder_widget.pressure = get_pressure()
        self.cylinder_widget.updateCalculations()
        self.close()

    def updateSettings(self):
        try:
            self.cylinder_widget.liquid_type = self.density_input.currentText()
            self.cylinder_widget.tank_name=self.name_input.text()
            self.cylinder_widget.pressure = get_pressure()
            self.cylinder_widget.density = float(self.density_input.text())
            self.cylinder_widget.radius = float(self.radius_input.text())
            self.cylinder_widget.updateCalculations()
        except ValueError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = CylinderWidget()
    widget.show()
    sys.exit(app.exec_())