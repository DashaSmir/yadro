export default function Pagination({ current, total, onPageChange }) {
  if (total <= 1) return null
  const pages = []
  for (let i = 1; i <= total; i++) pages.push(i)
  return (
    <nav>
      <ul className="pagination">
        <li className={`page-item ${current === 1 ? 'disabled' : ''}`}>
          <button className="page-link" onClick={() => onPageChange(current-1)}>Назад</button>
        </li>
        {pages.map(p => (
          <li key={p} className={`page-item ${p === current ? 'active' : ''}`}>
            <button className="page-link" onClick={() => onPageChange(p)}>{p}</button>
          </li>
        ))}
        <li className={`page-item ${current === total ? 'disabled' : ''}`}>
          <button className="page-link" onClick={() => onPageChange(current+1)}>Вперёд</button>
        </li>
      </ul>
    </nav>
  )
}