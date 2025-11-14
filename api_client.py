import requests
import json
from typing import Dict, Any, Optional, List
import time
import os

class APIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
        else:
            self.session.headers.update({
                'Content-Type': 'application/json'
            })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {"status": "success"}
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        return self._make_request('POST', endpoint, json=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        return self._make_request('PUT', endpoint, json=data)
    
    def delete(self, endpoint: str) -> Optional[Dict[str, Any]]:
        return self._make_request('DELETE', endpoint)

class JSONPlaceholderClient(APIClient):
    def __init__(self):
        super().__init__("https://jsonplaceholder.typicode.com")
    
    def get_posts(self) -> Optional[List[Dict[str, Any]]]:
        response = self.get('/posts')
        return response if isinstance(response, list) else None
    
    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        return self.get(f'/posts/{post_id}')
    
    def get_comments(self, post_id: int) -> Optional[List[Dict[str, Any]]]:
        response = self.get(f'/posts/{post_id}/comments')
        return response if isinstance(response, list) else None
    
    def create_post(self, title: str, body: str, user_id: int) -> Optional[Dict[str, Any]]:
        data = {
            'title': title,
            'body': body,
            'userId': user_id
        }
        return self.post('/posts', data)
    
    def update_post(self, post_id: int, title: Optional[str] = None, body: Optional[str] = None) -> Optional[Dict[str, Any]]:
        data = {}
        if title:
            data['title'] = title
        if body:
            data['body'] = body
        
        return self.put(f'/posts/{post_id}', data)
    
    def delete_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        return self.delete(f'/posts/{post_id}')

class WeatherClient(APIClient):
    def __init__(self, api_key: str):
        super().__init__("https://api.openweathermap.org/data/2.5", api_key)
    
    def get_current_weather(self, city: str, units: str = 'metric') -> Optional[Dict[str, Any]]:
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units
        }
        return self.get('/weather', params)
    
    def get_forecast(self, city: str, units: str = 'metric') -> Optional[Dict[str, Any]]:
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units
        }
        return self.get('/forecast', params)

def demo_jsonplaceholder():
    print("JSONPlaceholder API Demo")
    print("=" * 40)
    
    client = JSONPlaceholderClient()
    
    print("\n1. Getting all posts...")
    posts = client.get_posts()
    if posts:
        print(f"Found {len(posts)} posts")
        print(f"First post: {posts[0]['title']}")
    
    print("\n2. Getting post with ID 1...")
    post = client.get_post(1)
    if post:
        print(f"Title: {post['title']}")
        print(f"Body: {post['body'][:100]}...")
    
    print("\n3. Getting comments for post 1...")
    comments = client.get_comments(1)
    if comments:
        print(f"Found {len(comments)} comments")
        print(f"First comment: {comments[0]['email']}")
    
    print("\n4. Creating a new post...")
    new_post = client.create_post(
        title="My New Post",
        body="This is the body of my new post",
        user_id=1
    )
    if new_post:
        print(f"Created post with ID: {new_post.get('id')}")
    
    print("\n5. Updating post 1...")
    updated_post = client.update_post(1, title="Updated Title")
    if updated_post:
        print(f"Updated title: {updated_post['title']}")

def demo_weather():
    print("\nWeather API Demo")
    print("=" * 40)
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("OpenWeather API key not found. Set OPENWEATHER_API_KEY environment variable to test.")
        return
    
    client = WeatherClient(api_key)
    
    cities = ["London", "New York", "Tokyo"]
    
    for city in cities:
        print(f"\nGetting weather for {city}...")
        weather = client.get_current_weather(city)
        if weather:
            temp = weather['main']['temp']
            description = weather['weather'][0]['description']
            print(f"Temperature: {temp}°C")
            print(f"Description: {description}")

def rate_limited_request(client: APIClient, endpoint: str, max_retries: int = 3, delay: float = 1.0):
    for attempt in range(max_retries):
        response = client.get(endpoint)
        if response:
            return response
        
        if attempt < max_retries - 1:
            wait_time = delay * (2 ** attempt)
            print(f"Request failed, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    print("Max retries reached")
    return None

def main():
    print("API Client Examples")
    print("=" * 50)
    
    demo_jsonplaceholder()
    demo_weather()
    
    print("\nRate Limiting Demo")
    print("=" * 40)
    
    client = JSONPlaceholderClient()
    result = rate_limited_request(client, '/posts/1')
    if result:
        print("Successfully retrieved data with retry logic")

if __name__ == "__main__":
    main()