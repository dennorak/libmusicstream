from YoutubeMusic import YoutubeMusic
from Playlist import Playlist
from Spotify import Spotify
from os.path import exists
import json
import copy

THREAD_COUNT = 10

def main():
    sp = Spotify()
    ytm = YoutubeMusic()
    playlist = sp.get_playlist("0Ng0C62gBR7izpiEcKLIMy")
    all_tracks = [] # to be saved as cache
    new_tracks = [] # to be downloaded, dupes in all_tracks

    # check file exists for song in cache
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
    
    for track in all_tracks:
        print(track["yid"])

    # isrc check passed!
    #for track in playlist.tracks:
    #    try:
    #        print(track["external_ids"]["isrc"])
    #    except:
    #        print("no isrc:", track["name"])
    #        break

    # note: all this works! working on ISRC
    '''
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
    '''

if __name__ == "__main__":
    main()