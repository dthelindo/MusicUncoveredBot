from config import *
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep
import random
import requests
import spotipy
import threading
import tweepy

auth = tweepy.OAuthHandler(twit_consumer_key, twit_consumer_secret)
auth.set_access_token(twit_access_token, twit_access_token_secret)

client_credentials_manager = SpotifyClientCredentials(client_id=spot_client_id, client_secret=spot_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

api = tweepy.API(auth)

album_list = []
popularity = 0
genres = []

def search_song(track, artist):
    global popularity
    search = sp.search(q=track, type="track")
    for track in search["tracks"]["items"]:
        artist_name = track["artists"][0]["name"]
        if artist.lower() == artist_name.lower():
            popularity = track["popularity"]
    return popularity

def search_artist(artist):
    global popularity
    global genres
    search = sp.search(q=artist, type="artist", limit=1)
    i = 0
    while i < len(search["artists"]["items"]):
        artist_name = search["artists"]["items"][i]["name"]
        i += 1
        if artist.lower() == artist_name.lower():
            popularity = search["artists"]["items"][0]["popularity"]
            genres = search["artists"]["items"][0]["genres"]
    return popularity, genres

def get_releases():
    global album_list
    album_list = []
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

def tweet():
    print "collecting weekly..."
    song = []
    global popularity
    popularity = 0
    while popularity < 60:
        get_releases()
        try:
            song = album_list[random.randint(0, len(album_list))]
            search_song(song[1], song[0])
        except:
            print "Retrying..."
            tweet()
    if song:
        log = u"WEEK TWEET: \n Our weekly hot pick: \n" + song[0] + u" - " + song[1] + u"\n Listen here! " + song[2] + u"\nPopularity: " + str(popularity) + "\n \n"
        print log.encode("utf-8")
        #tweet = api.update_status(status="Our weekly hot pick: \n" + song[0] + " - " + song[1] + "\n Listen here! " + song[2])

def pop_tweet():
    print "collecting pop..."
    song = []
    global popularity
    global genres
    popularity = 0
    while popularity < 60 and not any(x in genres for x in ["pop", "post-teen pop", "dance pop", "pop christmas"]):
        get_releases()
        try:
            song = album_list[random.randint(0, len(album_list))]
            search_artist(song[0])
        except:
            print "Retrying..."
            pop_tweet()
    if song:
        log = u"WEEK TWEET: \n Pop Hot pick: \n" + song[0] + u" - " + song[1] + u"\n Listen here! " + song[2] + u"\nPopularity: " + str(popularity) + "\n \n"
        print log.encode("utf-8")
        #tweet = api.update_status(status="Pop Hot Pick: \n" + song[0] + " - " + song[1] + "\n Listen here! " + song[2])
        genres = []
    return genres

def rap_tweet():
    print "collecting rap..."
    song = []
    global popularity
    global genres
    popularity = 0
    while popularity < 60 and not any(x in genres for x in ["rap", "trap music", "hip hop", "dwn trap", "pop rap"]):
        get_releases()
        try:
            song = album_list[random.randint(0, len(album_list))]
            search_artist(song[0])
        except:
            print "Retrying..."
            rap_tweet()
    if song:
        log = u"WEEK TWEET: \n Hip Hop Hot pick: \n" + song[0] + u" - " + song[1] + u"\n Listen here! " + song[2] + u"\nPopularity: " + str(popularity) + "\n \n"
        print log.encode("utf-8")
        #tweet = api.update_status(status="Hip Hop Hot Pick: \n" + song[0] + " - " + song[1] + "\n Listen here! " + song[2])
        genres = []
    return genres

def set_interval(func1, func2, func3, sec):
    def func_wrapper():
        set_interval(func1, func2, func3, sec)
        func1()
        func2()
        func3()
        print "Sleeping... \n \n"
    t = threading.Timer(sec, func_wrapper)
    t.start()

def run():
    #604800
    print "First Tweet.... \n\n"
    tweet()
    pop_tweet()
    rap_tweet()
    print "Sleeping... \n \n"
    set_interval(tweet, pop_tweet, rap_tweet, 604800)

if __name__ == "__main__":
    run()
