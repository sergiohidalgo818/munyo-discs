
import api from './index'

export function uploadWishedCds(file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload/wished-cds', formData)
}

export function getWishedCds() {
  return api.get('/wished-cds')
}

export function deleteCollisions() {
  return api.put('/delete-colissions')
}

export function downloadWishedCds() {
  return api.get('/download/wished-cds', {
    responseType: 'blob',
  })
}

