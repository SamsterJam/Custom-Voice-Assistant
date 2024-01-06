import requests
from datetime import datetime, date

# A mapping of weather codes to general forecast descriptions
weather_code_descriptions = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

def get_weather(latitude, longitude, day=None):
    units = "fahrenheit"
    today = datetime.now().strftime("%Y-%m-%d")
    if day is None or day == today:
        # Fetch current weather and today's high and low temperatures
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=weathercode,temperature_2m,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&start_date={today}&end_date={today}&temperature_unit={units}"
        response = requests.get(url)
        data = response.json()
        current = data.get('current', {})
        daily = data.get('daily', {})
        weather_code = current.get('weathercode')
        weather_description = weather_code_descriptions.get(weather_code, "Unknown conditions")
        high_temp = daily.get('temperature_2m_max', [])[0]  # Today's high temperature
        low_temp = daily.get('temperature_2m_min', [])[0]  # Today's low temperature
        weather_str = (
            f"[Current weather (Today: {date.today()})]: {weather_description}. "
            f"Temperature: {current.get('temperature_2m')}°, "
            f"High: {high_temp}°, "
            f"Low: {low_temp}°, "
            f"Wind speed: {current.get('wind_speed_10m')} mph, "
        )
        
        weather_str += "(To get forcasts or historical weather, provide a date in the third parameter)"
    else:
        # Fetch forecast weather for the specified day
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max&start_date={day}&end_date={day}&units={units}"
        response = requests.get(url)
        data = response.json()
        daily = data.get('daily', {})
        time_slots = daily.get('time', [])
        
        # Find the forecast for the requested day
        try:
            day_index = time_slots.index(day)
            weather_code = daily['weathercode'][day_index]
            weather_description = weather_code_descriptions.get(weather_code, "Unknown conditions")
            weather_str = (
                f"Forecast for {day}: {weather_description}. "
                f"Max temperature: {daily['temperature_2m_max'][day_index]}°, "
                f"Min temperature: {daily['temperature_2m_min'][day_index]}°, "
                f"Total precipitation: {daily['precipitation_sum'][day_index]} inches, "
                f"Max wind speed: {daily['wind_speed_10m_max'][day_index]} mph."
            )
        except ValueError:
            weather_str = "Forecast data not available for the requested day."

    return weather_str