import api from "./index";

export function uploadOwnedCds(file) {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload/owned-cds", formData);
}

export function getOwnedCds() {
  return api.get("/owned-cds");
}

export function downloadOwnedCds() {
  return api.get("/download/owned-cds", { responseType: "blob" });
}

export function addOwnedCd(artist, disc) {
  return api.post("/add-owned-cd", { artist, disc });
}

export function deleteOwnedCd(artist, disc) {
  return api.post("/delete-owned-cd", { artist, disc });
}

export function modifyOwnedCd(artist, disc, newArtist, newDisc) {
  return api.post("/modify-owned-cd", {
    artist,
    disc,
    new_artist: newArtist,
    new_disc: newDisc,
  });
}
