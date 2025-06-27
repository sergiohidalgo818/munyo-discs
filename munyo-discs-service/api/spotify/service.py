from fastapi import APIRouter
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from api.spotify.spotify import Spotify
from api.connection.connection import Connection
from api.song.song import Song
from api.playlist.playlist import Playlist
from api.artist.artist import Artist
from fastapi.responses import JSONResponse
import os
import json
import pandas as pd
from typing import Union
import uuid

spotify_router = APIRouter()

ACCESS_DIR: str = "access"
os.makedirs(ACCESS_DIR, exist_ok=True)
token_filename: str = "spotify.json"

SPOTIFY_DIR: str = "spotify"
os.makedirs(SPOTIFY_DIR, exist_ok=True)
liked_tracks_filename: str = "liked_tracks.csv"

playlists_filename: str = "playlists.csv"
playlist_tracks_filename: str = "_playlist_tracks.csv"

artists_filename: str = "artists.csv"


@spotify_router.post("/access/spotify")
async def access_spotify(client_id: str, client_secret: str) -> Spotify:
    connection = Connection(
        "Spotify",
        "https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Primary_Logo_RGB_Green.png",
    )
    auth_path = os.path.abspath(os.path.join(ACCESS_DIR, token_filename))
    auth_dict = {"client_id": client_id, "client_secret": client_secret}
    json.dump(auth_dict, open(auth_path, "w"))

    return Spotify(client_id, client_secret, connection.connection_id)


@spotify_router.get("/spotify/get-likes")
async def get_likes() -> Union[list[Song], JSONResponse]:
    auth_path = os.path.abspath(os.path.join(ACCESS_DIR, token_filename))
    if not os.path.exists(auth_path):
        return JSONResponse(content=False)
    with open(auth_path, "r") as f:
        auth_dict = json.load(f)

    auth_manager = SpotifyClientCredentials(
        client_id=auth_dict["client_id"], client_secret=auth_dict["client_secret"]
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    tracks_names = []
    tracks_artists = []
    tracks_albums = []
    tracks_uris = []
    offset = 0
    limit = 50

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = results["items"] if results is not None else None

        if items is None:
            break

        for item in items:
            track = item["track"]
            tracks_names.append(track["name"])
            tracks_artists.append(track["artists"][0]["name"])
            tracks_albums.append(track["album"]["name"])
            tracks_uris.append(track["uri"])

        offset += len(items)  # advance by however many items were returned
    tracks_df = pd.DataFrame(
        {
            "name": tracks_names,
            "artist": tracks_artists,
            "album": tracks_albums,
            "uri": tracks_uris,
        }
    )
    tracks = []
    for _, row in tracks_df.iterrows():
        tracks.append(Song(str(row["name"]), uuid.uuid4(), uuid.uuid4()))

    tracks_df.to_csv(
        os.path.abspath(os.path.join(SPOTIFY_DIR, playlists_filename)), index=False
    )

    return tracks


@spotify_router.get("/spotify/get-playlist")
async def get_playlist(playlist_id: str) -> Union[list[Song], JSONResponse]:
    auth_path = os.path.abspath(os.path.join(ACCESS_DIR, token_filename))
    if not os.path.exists(auth_path):
        return JSONResponse(content=False)

    with open(auth_path, "r") as f:
        auth_dict = json.load(f)

    auth_manager = SpotifyClientCredentials(
        client_id=auth_dict["client_id"], client_secret=auth_dict["client_secret"]
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    tracks_names = []
    tracks_artists = []
    tracks_albums = []
    tracks_uris = []
    offset = 0
    limit = 100  # max allowed by Spotify for playlists

    while True:
        results = sp.playlist_items(playlist_id, limit=limit, offset=offset)
        items = results["items"] if results is not None else None

        if items is None:
            break

        for item in items:
            track = item.get("track")
            if track is None:
                continue  # skip local/deleted tracks

            tracks_names.append(track["name"])
            tracks_artists.append(track["artists"][0]["name"])
            tracks_albums.append(track["album"]["name"])
            tracks_uris.append(track["uri"])

        offset += len(items)

    # Convert to DataFrame
    tracks_df = pd.DataFrame(
        {
            "name": tracks_names,
            "artist": tracks_artists,
            "album": tracks_albums,
            "uri": tracks_uris,
        }
    )

    # Create Song list
    tracks = []
    for _, row in tracks_df.iterrows():
        tracks.append(Song(str(row["name"]), uuid.uuid4(), uuid.uuid4()))

    tracks_df.to_csv(
        os.path.abspath(
            os.path.join(SPOTIFY_DIR, playlist_id + playlist_tracks_filename)
        )
    )

    return tracks


@spotify_router.get("/spotify/get-playlists")
async def get_playlists() -> Union[list[Playlist], JSONResponse]:
    auth_path = os.path.abspath(os.path.join(ACCESS_DIR, token_filename))
    if not os.path.exists(auth_path):
        return JSONResponse(content=False)

    with open(auth_path, "r") as f:
        auth_dict = json.load(f)

    auth_manager = SpotifyClientCredentials(
        client_id=auth_dict["client_id"], client_secret=auth_dict["client_secret"]
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist_names = []
    playlist_spotify_ids = []

    offset = 0
    limit = 50

    while True:
        results = sp.current_user_playlists(limit=limit, offset=offset)
        items = results["items"] if results is not None else None

        if not items:
            break

        for item in items:
            playlist_names.append(item["name"])
            playlist_spotify_ids.append(item["id"])

        offset += len(items)

    # Convert to DataFrame
    playlists_df = pd.DataFrame(
        {
            "name": playlist_names,
            "spotify_id": playlist_spotify_ids,
        }
    )

    # Create Playlist objects
    playlists = []
    for _, row in playlists_df.iterrows():
        playlists.append(Playlist(name=str(row["name"])))

    # Save DataFrame to CSV
    playlists_df.to_csv(
        os.path.abspath(os.path.join(SPOTIFY_DIR, playlists_filename)), index=False
    )

    return playlists


@spotify_router.get("/spotify/get-artists")
async def get_followed_artists() -> Union[list[Artist], JSONResponse]:
    auth_path = os.path.abspath(os.path.join(ACCESS_DIR, token_filename))
    if not os.path.exists(auth_path):
        return JSONResponse(content=False)

    with open(auth_path, "r") as f:
        auth_dict = json.load(f)

    auth_manager = SpotifyClientCredentials(
        client_id=auth_dict["client_id"], client_secret=auth_dict["client_secret"]
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    artists = []
    artist_names = []
    artist_spotify_ids = []

    after = None
    limit = 50

    while True:
        results = sp.current_user_followed_artists(limit=limit, after=after)
        artist_items = (
            results.get("artists", {}).get("items", []) if results is not None else None
        )
        if not artist_items:
            break

        for artist in artist_items:
            artist_names.append(artist["name"])
            artist_spotify_ids.append(artist["id"])
            artists.append(Artist(name=artist["name"]))

        # Set `after` for pagination
        after = (
            results["artists"].get("cursors", {}).get("after")
            if results is not None
            else None
        )
        if not after:
            break

    # Convert to DataFrame and save
    artists_df = pd.DataFrame({"name": artist_names, "spotify_id": artist_spotify_ids})
    artists_df.to_csv(
        os.path.abspath(os.path.join(SPOTIFY_DIR, playlists_filename)), index=False
    )

    return artists
