import os
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from disc_handler.disc_set.disc_set_owned import DiscSetOwned
from disc_handler.disc_set.disc_set_wished import DiscSetWished

disc_router = APIRouter()

UPLOAD_DIR: str = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

owned_cds_filename: str = "owned-cds.csv"
owned_cds_filename_orig: str = "owned-cds-orig.csv"
wished_cds_filename: str = "wished-cds.csv"
wished_cds_filename_orig: str = "wished-cds-orig.csv"


@disc_router.post("/api/upload/owned-cds")
async def upload_owned_cds(file: UploadFile = File(...)):
    file_path_orig = os.path.abspath(os.path.join(UPLOAD_DIR, owned_cds_filename_orig))
    file_path = os.path.abspath(os.path.join(UPLOAD_DIR, owned_cds_filename))

    try:
        # Save file to disk
        contents = await file.read()
        with open(file_path_orig, "wb") as f:
            f.write(contents)

        DiscSetOwned(file_path_orig).frame_it().to_csv(
            file_path, index=False, encoding="latin1"
        )
        return {"message": "Owned CDs uploaded and saved", "path": file_path}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@disc_router.post("/api/upload/wished-cds")
async def upload_wished_cds(file: UploadFile = File(...)):
    file_path_orig = os.path.abspath(os.path.join(UPLOAD_DIR, wished_cds_filename_orig))
    file_path = os.path.abspath(os.path.join(UPLOAD_DIR, wished_cds_filename))

    try:
        # Save file to disk
        contents = await file.read()
        with open(file_path_orig, "wb") as f:
            f.write(contents)

        DiscSetWished(file_path_orig).frame_it().to_csv(
            file_path, index=False, encoding="latin1"
        )
        return {"message": "Wished CDs uploaded and saved", "path": file_path}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@disc_router.put("/api/delete-colissions")
async def delete_colissions():
    wished_file_path = os.path.abspath(os.path.join(UPLOAD_DIR, wished_cds_filename))
    owned_file_path = os.path.abspath(os.path.join(UPLOAD_DIR, owned_cds_filename))

    try:
        DiscSetWished(wished_file_path).delete_collisions(
            owned_file_path, wished_file_path
        )
        return {"message": "Wished CDs uploaded and saved", "path": owned_file_path}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@disc_router.get("/api/owned-cds")
def get_owned_cds():
    if not os.path.exists(
        os.path.abspath(os.path.join(UPLOAD_DIR, owned_cds_filename))
    ):
        return JSONResponse(content=False)
    return DiscSetOwned(os.path.join(UPLOAD_DIR, owned_cds_filename)).serialize()


@disc_router.get("/api/wished-cds")
def get_wished_cds():
    if not os.path.exists(
        os.path.abspath(os.path.join(UPLOAD_DIR, wished_cds_filename))
    ):
        return JSONResponse(content=False)
    return DiscSetOwned(os.path.join(UPLOAD_DIR, wished_cds_filename)).serialize()


@disc_router.get("/api/download/owned-cds")
def download_owned_csv():
    file_path = os.path.abspath(os.path.join(UPLOAD_DIR, owned_cds_filename))
    if not os.path.exists(file_path):
        return JSONResponse(
            content={"error": "Owned CDs file not found"}, status_code=404
        )

    return StreamingResponse(
        open(file_path, mode="rb"),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=owned-cds.csv"},
    )


@disc_router.get("/api/download/wished-cds")
def download_wished_csv():
    file_path = os.path.abspath(os.path.join(UPLOAD_DIR, wished_cds_filename))
    if not os.path.exists(file_path):
        return JSONResponse(
            content={"error": "Wished CDs file not found"}, status_code=404
        )

    return StreamingResponse(
        open(file_path, mode="rb"),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=wished-cds.csv"},
    )
