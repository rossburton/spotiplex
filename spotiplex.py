#! /usr/bin/env python3

# TODO use keychain or something
plex_username = ""
plex_password = ""
plex_servername = ""
spotify_username = ""

from plexapi.myplex import MyPlexAccount
account = MyPlexAccount(plex_username, plex_password)
plex = account.resource(plex_servername).connect()

import spotipy, spotipy.oauth2, spotipy.util

spotify_client_id = "30fe576d442f4976920ed06951c5dc9e"
spotify_client_secret = "80303dcc89da44908d5bd490abab15a4"

#cred_manager = spotipy.oauth2.SpotifyClientCredentials(spotify_client_id, spotify_client_secret)
#spotify = spotipy.Spotify(client_credentials_manager=cred_manager)

token = spotipy.util.prompt_for_user_token(spotify_username, "user-library-modify",
                                           spotify_client_id, spotify_client_secret,
                                           "http://localhost/callback")
spotify = spotipy.Spotify(auth=token)

def like_albums():
    queue = []

    for album in plex.library.section('Music').albums():
        # TODO year?
        print(album.parentTitle + " / " + album.title, end="... ")

        query = "artist:%s album:%s" % (album.parentTitle, album.title)    
        results = spotify.search(q=query, type="album")
        items = results['albums']['items']
        if items:
            print("found")
            queue.append(items[0]["id"])
        else:
            print("NOT found")

    def chunker(iterable, chunksize):
        return zip(*[iter(iterable)]*chunksize)

    for chunk in chunker(queue, 50):
        spotify.current_user_saved_albums_add(chunk)

def follow_album_artists():
    spotify.user_follow_artists()

like_albums()
