from YoutubeMusic import YoutubeMusic
from Metadata import *
from Playlist import Playlist
from Spotify import Spotify
from os.path import exists
import json
import copy

THREAD_COUNT = 10

def main():
    sp = Spotify()
    ytm = YoutubeMusic()
    playlist = sp.get_playlist("5ITsgpdHuP4vJgSRAeC1Dq")
    all_tracks = [] # to be saved as cache
    new_tracks = [] # to be downloaded, dupes in all_tracks

    # load/update cache
    if exists("items.json"):    
        print("Loading from cache")
        with open("items.json", "r") as f:
            try:
                cached_tracks = json.loads(f.read())
                uris = []
                for track in cached_tracks:
                    uris.append(track["uri"])
                new_tracks = [track for track in playlist.tracks if track["uri"] not in uris]
                all_tracks = copy.deepcopy(new_tracks + cached_tracks)
                print("Loaded", len(cached_tracks), "of", len(all_tracks), "from cache (", str(len(cached_tracks)/len(all_tracks)*100) + "% )")
            except json.decoder.JSONDecodeError:
                print("Failed to read cache data!")
                return
    else:
        new_tracks = playlist.tracks
        all_tracks = new_tracks

    # download
    ytm.threaded_search(new_tracks, THREAD_COUNT)
    with open("items.json", "w+") as f:
        f.write(json.dumps(all_tracks))
    ytm.download(new_tracks, THREAD_COUNT)

    threaded_add_metadata(new_tracks)

if __name__ == "__main__":
    main()