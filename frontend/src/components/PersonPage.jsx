import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchPerson, fetchRandomPerson } from '../api'
import styles from './PersonPage.module.css'

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

  if (loading) return <div className={styles.loading}>Загрузка...</div>
  if (error || !person) return (
    <div className={styles.errorAlert}>
      <h3>Пользователь не найден</h3>
      <Link to="/" className={styles.buttonSecondary}>Вернуться на главную</Link>
    </div>
  )

  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <h2>Информация о человеке</h2>
      </div>
      <div className={styles.cardBody}>
        <p><strong>ID:</strong> {person.id}</p>
        <p><strong>Пол:</strong> {person.gender}</p>
        <p><strong>Имя:</strong> {person.first_name}</p>
        <p><strong>Фамилия:</strong> {person.last_name}</p>
        <p><strong>Телефон:</strong> {person.phone}</p>
        <p><strong>Email:</strong> {person.email}</p>
        <p><strong>Место проживания:</strong> {person.location}</p>
      </div>
      <div className={styles.cardFooter}>
        <Link to="/" className={styles.buttonSecondary}>На главную</Link>
        <Link to="/random" className={styles.buttonInfo}>Случайный человек</Link>
      </div>
    </div>
  )
}