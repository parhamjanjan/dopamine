import api from './api'


// ================================
// Tasks
// ================================

export async function getTasks() {
  const response = await api.get('/planner/tasks/')
  return response.data
}


export async function createTask(taskData) {
  const response = await api.post(
    '/planner/tasks/',
    taskData
  )

  return response.data
}


export async function updateTask(id, taskData) {
  const response = await api.patch(
    `/planner/tasks/${id}/`,
    taskData
  )

  return response.data
}


export async function deleteTask(id) {
  await api.delete(
    `/planner/tasks/${id}/`
  )
}


// ================================
// Lists
// ================================

export async function getLists() {
  const response = await api.get('/planner/lists/')
  return response.data
}


export async function createList(listData) {
  const response = await api.post(
    '/planner/lists/',
    listData
  )

  return response.data
}


export async function updateList(id, listData) {
  const response = await api.patch(
    `/planner/lists/${id}/`,
    listData
  )

  return response.data
}


export async function deleteList(id) {
  await api.delete(
    `/planner/lists/${id}/`
  )
}