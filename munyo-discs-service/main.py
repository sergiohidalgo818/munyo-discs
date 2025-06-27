from fastapi import FastAPI
from api.artist.service import artist_router
from api.disc.service import disc_router
from api.connection.service import connection_router
from api.spotify.service import spotify_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(artist_router)
app.include_router(disc_router)
app.include_router(connection_router)
app.include_router(spotify_router)
