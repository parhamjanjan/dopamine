import api from './api'

export const notesApi = {
  list(params = {}) { return api.get('/notes/', { params }) },
  mine() { return api.get('/notes/mine/') },
  get(id) { return api.get(`/notes/${id}/`) },
  create(data) { return api.post('/notes/', data) },
  update(id, data) { return api.patch(`/notes/${id}/`, data) },
  remove(id) { return api.delete(`/notes/${id}/`) },
  bookmark(id) { return api.post(`/notes/${id}/bookmark/`) },
  getProgress(id) { return api.get(`/notes/${id}/progress/`) },
  saveProgress(id, data) { return api.put(`/notes/${id}/progress/`, data) },
  bookmarks() { return api.get('/notes/bookmarks/') },
  revisions(id) { return api.get(`/notes/${id}/revisions/`) }
}
