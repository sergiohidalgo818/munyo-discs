import socket
import uvicorn
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.artist.service import artist_router
from api.disc.service import disc_router
from api.connection.service import connection_router
from api.spotify.service import spotify_router

app = FastAPI()

# Determine base path for static files
base_path = (
    Path(getattr(sys, "_MEIPASS", ""))  # If frozen by PyInstaller
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parents[1]
)

# Vue app build output (bundled by PyInstaller as 'dist')
frontend_dir = base_path / "dist"

if not frontend_dir.exists():
    raise RuntimeError(f"Vue frontend not found at: {frontend_dir}")


# Enable CORS for dev/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routers
app.include_router(artist_router)
app.include_router(disc_router)
app.include_router(connection_router)
app.include_router(spotify_router)
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


if __name__ == "__main__":
    port = find_free_port()
    uvicorn.run(app, host="127.0.0.1", port=port)
