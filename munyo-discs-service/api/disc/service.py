import json
import uuid
import os
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from api.disc.disc import Disc, DiscValoration
from typing import List
from dataclasses import asdict
from disc_handler.disc_set.disc_set_obtained import DiscSetObtained
from disc_handler.disc_set.disc_set_preference import DiscSetPreference

disc_router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

owned_cds: List[Disc] = []
wished_cds: List[DiscValoration] = []


@disc_router.post("/api/upload/owned-cds")
async def upload_owned_cds(file: UploadFile = File(...)):
    global owned_cds
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save file to disk
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        DiscSetObtained(file_path).frame_it()
        return {"message": "Owned CDs uploaded and saved", "count": len(owned_cds)}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@disc_router.post("/api/upload/wished-cds")
async def upload_wished_cds(file: UploadFile = File(...)):
    global wished_cds
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save file to disk
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        DiscSetPreference(file_path).frame_it()

        return {"message": "Wished CDs uploaded and saved", "count": len(wished_cds)}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@disc_router.get("/api/owned-cds")
def get_owned_cds():
    if not owned_cds:
        return JSONResponse(content=False)
    return [asdict(d) for d in owned_cds]


@disc_router.get("/api/wished-cds")
def get_wished_cds():
    if not wished_cds:
        return JSONResponse(content=False)
    return [asdict(w) for w in wished_cds]
