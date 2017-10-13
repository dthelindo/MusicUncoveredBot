from config import *
from spotipy.oauth2 import SpotifyClientCredentials
import random
import requests
import spotipy
import sys
import time
import threading
import tweepy

auth = tweepy.OAuthHandler(twit_consumer_key, twit_consumer_secret)
auth.set_access_token(twit_access_token, twit_access_token_secret)
api = tweepy.API(auth)
client_credentials_manager = SpotifyClientCredentials(client_id=spot_client_id, client_secret=spot_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main():
    genre_list = {
        "Daily": ["Daily", "rap", "pop", "country", "edm", "post-teen pop"],
        "Hip Hop": ["Hip Hop", "rap", "trap music", "hip hop", "dwn trap", "r-n-b", "trip-hop"],
        "Pop": ["Pop", "pop", "post-teen pop", "pop christmas", "dance", "indie pop"],
        "EDM": ["EDM", "edm", "elctronic trap", "electro house", "house", "electro", "club", "dance", "electronic"],
        "Country": ["Country", "contemporary country", "country", "country road"],
    }

    tweet(genre_list["Daily"])
    tweet(genre_list["Pop"])
    tweet(genre_list["Hip Hop"])
    tweet(genre_list["EDM"])
    tweet(genre_list["Country"])


def tweet(genres):
    album_list = []
    popularity = 0
    track_genres = []
    try:
        album_list = get_releases(album_list)
        song = album_list[random.randint(0, len(album_list))]
        track_genres = find_genres(song[0], track_genres)
        popularity = find_popularity(song[1], song[0], popularity)
        if song and popularity >= 55 and any(x in track_genres for x in genres[1:]):
            tweet = api.update_status(status=genres[0] + " Pick: \n" + song[0] + " - " + song[1] + "\nListen here! " + song[2])
            return
        else:
            tweet(genres)
    except:
        tweet(genres)


#function searches for song & popularity
def find_popularity(track, artist, popularity):
    search = sp.search(q=track, type="track")
    for track in search["tracks"]["items"]:
        artist_name = track["artists"][0]["name"]
        if artist.lower() == artist_name.lower():
            popularity = track["popularity"]
    return popularity

#function searches target artist for genre
def find_genres(artist, track_genres):
    search = sp.search(q=artist, type="artist", limit=1)
    i = 0
    while i < len(search["artists"]["items"]):
        artist_name = search["artists"]["items"][i]["name"]
        i += 1
        if artist.lower() == artist_name.lower():
            track_genres = search["artists"]["items"][0]["genres"]
    return track_genres

#fetches new releases
def get_releases(album_list):
    releases = sp.new_releases()
    while releases:
            albums = releases['albums']
            for i, item in enumerate(albums['items']):
                album_type = item["album_type"]
                if album_type == "single":
                    artist = item["artists"][0]["name"]
                    album_name = item["name"]
                    link = "https://open.spotify.com/album/" + item["id"]
                    track = [artist, album_name, link]
                    album_list.append(track)
            if albums['next']:
                releases = sp.next(albums)
            else:
                releases = None
    return album_list
