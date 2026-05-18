import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchPerson, fetchRandomPerson } from '../api'
import styles from './PeopleTable.module.css';
export default function PersonPage({ random }) {
  const { id } = useParams()
  const [person, setPerson] = useState(null)
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        let data
        if (random) {
          data = await fetchRandomPerson()
        } else if (id) {
          data = await fetchPerson(id)
        } else {
          setError(true)
          setLoading(false)
          return
        }
        setPerson(data)
      } catch (err) {
        setError(true)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id, random])

  if (loading) return <div className="text-center mt-4">Загрузка...</div>
  if (error || !person) return (
    <div className="alert alert-danger mt-4">
      <h3>Пользователь не найден</h3>
      <Link to="/">Вернуться на главную</Link>
    </div>
  )

  return (
    <div className="card mt-3">
      <div className="card-header bg-primary text-white">
        <h2>Информация о человеке</h2>
      </div>
      <div className="card-body">
        <p><strong>ID:</strong> {person.id}</p>
        <p><strong>Пол:</strong> {person.gender}</p>
        <p><strong>Имя:</strong> {person.first_name}</p>
        <p><strong>Фамилия:</strong> {person.last_name}</p>
        <p><strong>Телефон:</strong> {person.phone}</p>
        <p><strong>Email:</strong> {person.email}</p>
        <p><strong>Место проживания:</strong> {person.location}</p>
      </div>
      <div className="card-footer">
        <Link to="/" className="btn btn-secondary">На главную</Link>
        <Link to="/random" className="btn btn-info ms-2">Случайный человек</Link>
      </div>
    </div>
  )
}