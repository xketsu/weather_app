# Weather App 🌤️

A modern and user-friendly weather application built with PyQt5.

## Features

- 🌍 Weather lookup by city name
- 🌡️ Temperature display (Celsius)
- 🌈 Weather emojis
- 📱 Modern and responsive design
- ⚡ Fast and reliable API integration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/username/weather-app.git
cd weather-app
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your OpenWeatherMap API key:
```bash
WEATHER_API_KEY=your_api_key_here
```

**How to get an API Key?**
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Create a free account
3. Get your API key and add it to the `.env` file

## Usage

```bash
python weather.py
```


## Technologies

- **Python 3.7+**
- **PyQt5** - GUI framework
- **Requests** - For HTTP requests
- **python-dotenv** - For environment variables
- **OpenWeatherMap API** - Weather data source
