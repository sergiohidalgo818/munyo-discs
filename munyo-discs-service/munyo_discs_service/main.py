import socket
import uvicorn
import sys
import threading

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from munyo_discs_service.api.artist.service import artist_router
from munyo_discs_service.api.disc.service import disc_router
from munyo_discs_service.api.connection.service import connection_router
from munyo_discs_service.api.spotify.service import spotify_router
from starlette.responses import FileResponse
from fastapi.responses import JSONResponse


app = FastAPI()

base_path = (
    Path(getattr(sys, "_MEIPASS", ""))
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parents[2] / "munyo-discs-cli"
)

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


@app.exception_handler(404)
async def vue_router_handler(request, exc):
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Not Found"})


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


def run_server():
    # port = find_free_port()
    port = 8218
    uvicorn.run(app, host="127.0.0.1", port=port)


def main():
    thread = threading.Thread(target=run_server)
    thread.start()
    thread.join()  # Keep Python alive


if __name__ == "__main__":
    main()
    # def run_server():
    #     port = find_free_port()
    #     uvicorn.run(app, host="127.0.0.1", port=port)
    #
    # threading.Thread(target=run_server, daemon=True).start()
