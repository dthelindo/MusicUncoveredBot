"""Main functionailty for Twiiter/Spotify bot.

MusicUncovered is a twitter bot that collects data using the Spotipy API,
bringing users new, popular music weekly. Currently, MusicUncovered is guided
to collect data for new, popular tracks in hip hop, pop, country and edm.
"""

import os
import pymongo
import requests
import random
from requests_oauthlib import OAuth1
from entry import Entry

# Set up mongo db
mongo_url = "mongodb+srv://dlindo28:{}@cluster0.lc5ad.mongodb.net/musicuncovered?retryWrites=true&w=majority".format(
    os.environ.get("MONGO_PASS"))
client = pymongo.MongoClient(mongo_url)
db = client["musicuncovered"]
used_links = db["used_links"]

def get_spotify_header():
    """Returns the access_token header needed for Spotify API."""
    url = "https://accounts.spotify.com/api/token"
    params = {"grant_type": "client_credentials"}
    auth_tokens = (os.environ.get("SPOTIFY_CLIENT_ID"),
                   os.environ.get("SPOTIFY_CLIENT_SECRET"))
    res = requests.post(url, data=params, auth=auth_tokens).json()
    return {"Authorization": "Bearer " + res["access_token"]}


spotify_access_header = get_spotify_header()


def get_new_releases():
    """Fetches list of newly released tracks and albums.

    Returns:
        List of newly released singles and albums. Each element is a dict mapping
        the entry's attributes to it corresponding values. Relavent attributes
        include:
            id (str): Spotify ID for the album
            album_type (str): type of entry, album or single
            name (str): title of the album/single
            artists (dict[]): list of dicts giving details on artists on the album/single
            external_urls (dict): external urls for the entry. "spotify" key maps to
                web link for the track(s)
    """
    url = "https://api.spotify.com/v1/browse/new-releases"
    res = requests.get(url, headers=spotify_access_header).json()
    return res["albums"]["items"]


def get_entries():
    """Returns lists of new released singles and albums with relevant information

    Returns:
        singles_list (tuple[]): list of potential singles picks. Each tuple will carry
            information pertaining to what is needed for making tweets. See:

            (artist, artist_id, title, Spotify link, popularity score)

        albums_list (tuple[]): list of potential album picks (see singles_list
            for details)
    """
    singles_list = []
    albums_list = []
    releases = get_new_releases()

    for release in releases:
        artist = release["artists"][0]["name"]
        artist_id = release["artists"][0]["id"]
        title = release["name"]
        link = release["external_urls"]["spotify"]
        genres = get_genres(artist_id)

        if used_links.find_one({"link": link}) == None:
            if release["album_type"] == "single":
                tracks_url = "https://api.spotify.com/v1/albums/" + \
                    release["id"] + "/tracks"
                tracks = requests.get(
                    tracks_url, headers=spotify_access_header).json()
                track_id = tracks["items"][0]["id"]

                pop_url = "https://api.spotify.com/v1/tracks/" + track_id
                popularity = requests.get(
                    pop_url, headers=spotify_access_header).json()
                popularity = popularity["popularity"]

                entry = Entry(artist, title, "single",
                              link, popularity, genres)
                singles_list.append(entry)
            elif release["album_type"] == "album":
                pop_url = "https://api.spotify.com/v1/albums/" + release["id"]
                popularity = requests.get(
                    pop_url, headers=spotify_access_header).json()
                popularity = popularity["popularity"]

                entry = Entry(artist, title, "album", link, popularity, genres)
                albums_list.append(entry)

    return singles_list, albums_list


def get_genres(artist_id):
    """Returns list of genres for given artist by id"""
    url = "https://api.spotify.com/v1/artists/" + artist_id
    res = requests.get(url, headers=spotify_access_header).json()
    genres = res["genres"]
    return genres


def tweet_singles(singles):
    """Returns list of singles which will be chosen to be tweeted

    We continue choosing random tracks from the singles list until each genre
    has been found and tweeted.
    """
    genres_left = {"Daily", "Hip Hop", "Pop", "Electronic", "Country"}
    for _ in range(len(singles)):
        if not genres_left:
            break
        choice = singles[random.randint(0, len(singles) - 1)]
        if "Daily" in genres_left:
            send_tweet(choice, is_daily=True)
            genres_left.remove("Daily")
        else:
            if choice.parent_genre in genres_left:
                send_tweet(choice)
                genres_left.remove(choice.parent_genre)


def tweet_album(albums):
    """Chooses random album from list to be tweeted"""
    choice = albums[random.randint(0, len(albums) - 1)]
    send_tweet(choice)


def send_tweet(entry, is_daily=False):
    """Posts status update (tweet) with the entry's corresponging tweet_string"""
    url = "https://api.twitter.com/1.1/statuses/update.json"
    params = {
        "status": entry.get_tweet_str(is_daily)
    }
    auth = OAuth1(
        os.environ.get("TWITTER_API_KEY"),
        os.environ.get("TWITTER_SECRET"),
        os.environ.get("TWITTER_ACCESS_TOKEN"),
        os.environ.get("TWITTER_ACCESS_SECRET")
    )
    res = requests.post(url, params=params, auth=auth)
    used_links.insert_one(
        {"link": entry.link, "artist": entry.artist, "title": entry.title})
    return res


if __name__ == "__main__":
    singles, albums = get_entries()
    singles = sorted(singles, key=lambda e: e.popularity, reverse=True)
    albums = sorted(albums, key=lambda e: e.popularity, reverse=True)
    tweet_singles(singles)
    tweet_album(albums)

    if used_links.count_documents({}) > 1000:
        used_links.delete_many({})
