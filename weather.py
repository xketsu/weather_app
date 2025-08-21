import sys
import os
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

# Load environment variables from .env file
load_dotenv()

class WeatherApp(QWidget):
    """
    A PyQt5-based weather application that fetches and displays weather data
    from OpenWeatherMap API.
    """
    
    def __init__(self):
        """Initialize the WeatherApp with all necessary UI components."""
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        """Initialize and configure the user interface."""
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        # Set widget alignments
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)   
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Set object names for styling
        self.city_label.setObjectName("cityLabel")
        self.city_input.setObjectName("cityInput")
        self.get_weather_button.setObjectName("getWeatherButton")
        self.temperature_label.setObjectName("temperatureLabel")
        self.emoji_label.setObjectName("emojiLabel")
        self.description_label.setObjectName("descriptionLabel")

        # Apply modern dark theme stylesheet
        self.setStyleSheet(
            """
            QWidget { background:#0f172a; color:#e2e8f0; }
            QLabel, QPushButton { font-family: 'Segoe UI', Arial; }
            #cityLabel { font-size:24px; font-weight:600; }
            #cityInput { font-size:20px; padding:6px 10px; border:2px solid #334155; border-radius:6px; background:#1e293b; }
            #cityInput:focus { border-color:#3b82f6; }
            #getWeatherButton { font-size:20px; padding:8px 18px; background:#2563eb; border:none; border-radius:6px; font-weight:600; }
            #getWeatherButton:hover { background:#1d4ed8; }
            #getWeatherButton:pressed { background:#1e40af; }
            #temperatureLabel { font-size:56px; font-weight:700; margin-top:8px; }
            #emojiLabel { font-size:64px; }
            #descriptionLabel { font-size:24px; font-style:italic; }
            """
        )

        # Connect button click to weather fetch function
        self.get_weather_button.clicked.connect(self.get_weather)


    def get_weather(self):
        """
        Fetch weather data from OpenWeatherMap API and display it.
        Handles various error scenarios with appropriate error messages.
        """
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            self.display_error("Error: API key not found. Please set WEATHER_API_KEY in .env file.")
            return
            
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError:
            # Handle different HTTP error codes with specific messages
            match response.status_code:
                case 400:
                    self.display_error("Error: Bad request. Please check the city name.")
                case 401:
                    self.display_error("Error: Unauthorized. Please check your API key.")
                case 403:
                    self.display_error("Error: Forbidden. You don't have permission to access this resource.")
                case 404:
                    self.display_error("Error: City not found.")
                case 500:
                    self.display_error("Error: Internal server error. Please try again later.")
                case 502:
                    self.display_error("Error: Bad gateway. Please try again later.")
                case 503:
                    self.display_error("Error: Service unavailable. Please try again later.")
                case 504:
                    self.display_error("Error: Gateway timeout. Please try again later.")
                case _:
                    self.display_error(f"Error: An unexpected error occurred. Status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.display_error("Error: Unable to connect to the weather service. Please check your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Error: The request timed out. Please try again later.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Error: Too many redirects. Please check the URL.")
        except requests.exceptions.RequestException:
            self.display_error("Error: Unable to retrieve weather data.")



    def display_error(self, message):
        """
        Display error message in the temperature label.
        
        Args:
            message (str): Error message to display
        """
        self.temperature_label.setStyleSheet("font-size:20px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        """
        Display weather information from API response.
        
        Args:
            data (dict): Weather data from OpenWeatherMap API
        """
        self.temperature_label.setStyleSheet("font-size:75px;")
        # Convert temperature from Kelvin to Celsius
        temperature = data["main"]["temp"] - 273.15  
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        
        self.temperature_label.setText(f"{temperature:.1f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description.title())

    @staticmethod
    def get_weather_emoji(weather_id):
        """
        Get appropriate emoji for weather condition based on weather ID.
        
        Args:
            weather_id (int): Weather condition ID from OpenWeatherMap API
            
        Returns:
            str: Weather emoji
        """
        if 200 <= weather_id < 300:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id < 400:
            return "🌦"   # Drizzle
        elif 500 <= weather_id < 600:
            return "🌧"   # Rain
        elif 600 <= weather_id < 700:
            return "❅"   # Snow
        elif 700 <= weather_id < 800:
            return "🌫"   # Atmosphere (fog, mist, etc.)
        elif weather_id == 800:
            return "☀️"  # Clear sky
        elif 801 <= weather_id < 900:
            return "⛅"  # Clouds
        return "❓"      # Unknown


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())