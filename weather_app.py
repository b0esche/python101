import requests

def get_weather(city, api_key):
    """
    Fetch current weather data for a city using OpenWeatherMap API.
    Sign up at https://openweathermap.org/api to get a free API key.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('cod') == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            print(f"Weather in {city}: {temp}°C, {desc}")
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"Error fetching weather: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your actual API key
    api_key = 'your_openweathermap_api_key'
    get_weather('London', api_key)