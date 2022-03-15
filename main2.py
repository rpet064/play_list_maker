import requests
import spotipy as spotipy
from bs4 import BeautifulSoup as BS
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
add_redirect_url = "http://localhost:5000"

date = input("Which year do you want to travel to? Type the date in format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=URL)
soup = BS(response.text, "html.parser")

song_list = soup.select(selector="div ul li ul li h3")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=add_redirect_url,
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path=".cache"
    )
)
user_id = sp.current_user()["id"]

uri_list = []
for song in song_list:
    result = sp.search(q=f"track:{song.getText().rstrip()} year:{date[:3]}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        pass




playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard Top 100", public=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=uri_list)