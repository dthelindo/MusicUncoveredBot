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


album_list = []
popularity = 0
genres = []

#function searches for song & popularity
def search_song(track, artist):
    global popularity
    search = sp.search(q=track, type="track")
    for track in search["tracks"]["items"]:
        artist_name = track["artists"][0]["name"]
        if artist.lower() == artist_name.lower():
            popularity = track["popularity"]
    return popularity

#function searches target artist for genre and popularity
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

#fetches new releases
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
    song = []
    global popularity
    popularity = 0
    while popularity < 55:
        get_releases()
        try:
            song = album_list[random.randint(0, len(album_list))]
            search_song(song[1], song[0])
        except:
            tweet()
    if song:
        tweet = api.update_status(status="Today\'s hot pick: \n" + song[0] + " - " + song[1] + "\n Listen here! " + song[2])

def pop_tweet():
    song = []
    global popularity
    global genres
    popularity = 0
    while popularity < 55 and not any(x in genres for x in ["pop", "post-teen pop", "pop christmas"]):
        get_releases()
        try:
            song = album_list[random.randint(0, len(album_list))]
            search_artist(song[0])
        except:
            pop_tweet()
    if song:
        tweet = api.update_status(status="Pop Hot Pick: \n" + song[0] + " - " + song[1] + "\n Listen here! " + song[2])
        genres = []
    return genres

def rap_tweet():
    song = []
    global popularity
    global genres
    popularity = 0
    while popularity < 55 and not any(x in genres for x in ["rap", "trap music", "hip hop", "dwn trap"]):
        get_releases()
        try:
            song = album_list[random.randint(0, len(album_list))]
            search_artist(song[0])
        except:
            rap_tweet()
    if song:
        tweet = api.update_status(status="Hip Hop Hot Pick: \n" + song[0] + " - " + song[1] + "\n Listen here! " + song[2])
        genres = []
    return genres

def edm_tweet():
    song = []
    global popularity
    global genres
    popularity = 0
    while popularity < 55 and not any(x in genres for x in ["edm", "electronic trap", "electro house"]):
        get_releases()
        try:
            song = album_list[random.randint(0, len(album_list))]
            search_artist(song[0])
        except:
            edm_tweet()
    if song:
        tweet = api.update_status(status="EDM Hot Pick: \n" + song[0] + " - " + song[1] + "\n Listen here! " + song[2])
        genres = []
    return genres

def country_tweet():
    song = []
    global popularity
    global genres
    popularity = 0
    while popularity < 55 and not any(x in genres for x in ["contemporary country", "country", "country road"]):
        get_releases()
        try:
            song = album_list[random.randint(0, len(album_list))]
            search_artist(song[0])
        except:
            country_tweet()
    if song:
        tweet = api.update_status(status="Country Daily Pick: \n" + song[0] + " - " + song[1] + "\n Listen here! " + song[2])
        genres = []
    return genres

#set interval for sending tweets
def set_interval(func1, func2, func3, func4, func5, sec):
    #set up wrapper to hold repeating functions
    def func_wrapper():
        set_interval(func1, func2, func3, sec)
        func1()
        func2()
        func3()
        func4()
        func5()
    t = threading.Timer(sec, func_wrapper)
    t.start()

#follow function calls each x seconds
def follow(sec):
    def wrapper():
        follow(sec)
        for follower in tweepy.Cursor(api.followers).items():
            follower.follow()
    threading.Timer(sec, wrapper).start()


def run():
    #initial tweets before sleep
    tweet()
    pop_tweet()
    rap_tweet()
    edm_tweet()
    country_tweet()
    #recursive tweet functions
    set_interval(tweet, pop_tweet, rap_tweet, edm_tweet, country_tweet, 86400)
    #follow new followers every 10 secs
    follow(10)


if __name__ == "__main__":
    run()
