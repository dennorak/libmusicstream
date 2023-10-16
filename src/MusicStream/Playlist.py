import math

class Playlist:
    def __init__(self, name, data):
        self.name = name
        self.tracks = []
        self.total = len(data)
        for track in data:
            # remove unneded stuff
            del track["available_markets"]
            del track["external_urls"]
            del track["href"]
            del track["id"]
            del track["is_local"]
            del track["popularity"]
            del track["preview_url"]
            del track["type"]
            del track["track"]
            del track["episode"]
            del track["album"]["available_markets"]
            del track["album"]["images"]
            del track["album"]["href"]
            del track["album"]["external_urls"]
            del track["album"]["type"]
            del track["album"]["album_type"]
            del track["album"]["uri"]
            del track["album"]["id"]
            del track["album"]["release_date_precision"]
            # reformat artists
            artists = []
            for artist in track["artists"]:
                artists.append(artist["name"])
            track["artists"] = artists

            artists = []
            for artist in track["album"]["artists"]:
                artists.append(artist["name"])
            track["album"]["artists"] = artists
            
            # reformat duration
            track["duration"] = math.ceil(track["duration_ms"] / 1000)
            del track["duration_ms"]

            self.tracks.append(track)
