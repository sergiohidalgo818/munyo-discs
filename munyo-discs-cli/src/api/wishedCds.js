import api from "./index";

export function uploadWishedCds(file) {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload/wished-cds", formData);
}

export function getWishedCds() {
  return api.get("/wished-cds");
}

export function deleteCollisions() {
  return api.put("/delete-colissions");
}

export function downloadWishedCds() {
  return api.get("/download/wished-cds", { responseType: "blob" });
}

export function addWishedCd(artist, disc, stars = 0) {
  return api.post("/add-wished-cd", { artist, disc, stars });
}

export function deleteWishedCd(artist, disc) {
  return api.post("/delete-wished-cd", { artist, disc });
}

export function modifyWishedCd(artist, disc, newArtist, newDisc, stars = 0) {
  return api.post("/modify-wished-cd", {
    artist,
    disc,
    new_artist: newArtist,
    new_disc: newDisc,
    stars: stars,
  });
}
