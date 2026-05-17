import axios from 'axios'
const api = axios.create({
  baseURL: '/api',
})
export const fetchPeople = (page, limit = 20) =>
  api.get(`/people?page=${page}&limit=${limit}`).then(res => res.data)

// export const loadPeople = (count) =>
//   api.post('/load', { count }).then(res => res.data)
// export const loadPeople = (count) =>
//   api.post(`/load?count=${count}`).then(res => res.data)
export const loadPeople = (count) =>
  api.post('/load', { count }).then(res => res.data)
export const fetchPerson = (id) =>
  api.get(`/person/${id}`).then(res => res.data)

export const fetchRandomPerson = () =>
  api.get('/person/random').then(res => res.data)