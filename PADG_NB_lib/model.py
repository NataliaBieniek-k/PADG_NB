import requests
from bs4 import BeautifulSoup

class User:
    def __init__(self, name: str, location: str, posts: int, img_url: str, map_widget):
        self.name = name
        self.location = location
        self.posts = posts
        self.img_url = img_url
        self.map_widget = map_widget
        self.coords = self.get_coordinates()
        self.marker = self.map_widget.set_marker(self.coords[0], self.coords[1], text=self.name)

    def get_coordinates(self):
        url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitudes = response_html.select('.latitude')
        longitudes = response_html.select('.longitude')

        if len(latitudes) == 0 or len(longitudes) == 0:
            return [52.0, 21.0]

        lat = float(latitudes[-1].text.replace(",", "."))
        lon = float(longitudes[-1].text.replace(",", "."))
        return [lat, lon]
