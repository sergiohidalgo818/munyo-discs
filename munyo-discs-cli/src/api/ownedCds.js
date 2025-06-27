
import api from './index'

export function uploadOwnedCds(file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload/owned-cds', formData)
}

export function getOwnedCds() {
  return api.get('/owned-cds')
}

export function downloadOwnedCds() {
  return api.get('/download/owned-cds', {
    responseType: 'blob', // important for downloading files
  })
}

