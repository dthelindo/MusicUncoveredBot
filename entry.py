"""Functionality for Entry Class, used to build Spotify entries"""


import random


class Entry:
    """Builds Entry object to represent a track or album"""

    def __init__(self, artist,  title, entry_type, link, popularity, genres):
        """Inits Entry with attributes fetched from Spotify"""
        self.artist = artist
        self.title = title
        self.type = entry_type
        self.link = link
        self.popularity = popularity
        self.genres = genres
        self.parent_genre = self.get_parent_genre()

    def __repr__(self):
        """Represents Entry in a more readable format with attributes"""
        return "Artist: {} \nTitle: {} \nPopularity: {} \nGenres: {}\nLink: {}\n".format(
            self.artist,
            self.title,
            self.popularity,
            ", ".join(self.genres),
            self.link
        )

    def get_parent_genre(self):
        """Gets parent genres for the entry's list of fetched genres

        The parent genre is the larger genre in which subgenres fall under. For
        example, "Pop" is the parent genre that "Art Pop" falls under.
        """
        if len(self.genres) == 0:
            return "None"

        genre_dict = {
            "Hip Hop": {"Hip Hop", "rap", "trap music", "hip hop", "dwn trap", "r-n-b", "trip-hop"},
            "Pop": {"Pop", "pop", "post-teen pop", "pop christmas", "dance", "indie pop"},
            "Electronic": {"EDM", "edm", "elctronic trap", "electro house", "house", "electro", "club", "dance", "electronic"},
            "Country": {"Country", "contemporary country", "country", "country road"},
        }

        for genre in self.genres:
            for key, val in dict.items(genre_dict):
                if genre in val:
                    return key

        return "None"

    def get_tweet_str(self, is_daily=False):
        """Formats entry for a tweet for the given genre"""
        if self.type == "single":
            return "Today's {} Pick: \n{} - {} \nListen Here! {}".format(
                "Hot" if is_daily else self.parent_genre,
                self.artist,
                self.title,
                self.link
            )
        else:
            return "Hot Album This Week: \n{} - {} \nListen Here! {}".format(
                self.artist,
                self.title,
                self.link
            )
