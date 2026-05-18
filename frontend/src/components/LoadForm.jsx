import { useState } from 'react'
import styles from './LoadForm.module.css'  
export default function LoadForm({ onLoad }) {
  const [count, setCount] = useState(100)

  const handleSubmit = (e) => {
    e.preventDefault()
    const num = parseInt(count, 10)
    if (isNaN(num) || num < 1 || num > 5000) {
      alert('Введите число от 1 до 5000')
      return
    }
    onLoad(num)
  }

  return (
    <form onSubmit={handleSubmit} className="row g-3 align-items-end">
      <div className="col-auto">
        <label htmlFor="loadCount" className="form-label">Загрузить новых людей</label>
        <input type="number" id="loadCount" className="form-control" value={count} onChange={e => setCount(e.target.value)} min="1" max="5000" />
      </div>
      <div className="col-auto">
        <button type="submit" className="btn btn-primary">Загрузить</button>
      </div>
    </form>
  )
}