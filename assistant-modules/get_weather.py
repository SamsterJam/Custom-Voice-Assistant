import requests
import json

# Get api_key from config
with open('config.json') as config_file:
    config = json.load(config_file)

api_key=config['custom']['openweathermap_api_key']

# Module function
def get_weather(location):
    """
    Get the current weather for a location using the OpenWeatherMap API.

    :param api_key: API key for the OpenWeatherMap service.
    :param location: The city to get the weather for.
    :return: A string containing weather information or an error message.
    """
    # Construct the API endpoint with the location and API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
    
    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        # Parse the JSON response
        weather_data = response.json()
        
        # Format the weather information into a readable string
        weather_info = (
            f"Weather in {location}: {weather_data['weather'][0]['description']}. "
            f"Temperature: {weather_data['main']['temp']}°F, "
            f"Humidity: {weather_data['main']['humidity']}%, "
            f"Wind Speed: {weather_data['wind']['speed']} mph."
        )
        
        return weather_info
    
    except requests.RequestException as e:
        # Handle any errors that occur during the API request
        return f"Failed to get weather data for {location}: {e}"