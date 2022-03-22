from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.find_all(name="h3", id="title-of-a-story")
song_names = [song.getText().strip("\n") for song in song_names_spans[3:103]]

#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:3000/callback/ ",
        client_id="ad70c8a884644a76a749281ae21d63a0",
        client_secret="b078a487e70f48528445c081d9c98987",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", limit=1, type="track", market="US")
    try:
        uri = result["tracks"]["items"][0]["uri"]

    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
    else:
        song_uris.append(uri)


#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(playlist)