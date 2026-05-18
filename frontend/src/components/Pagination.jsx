import styles from './Pagination.module.css';

export default function Pagination({ current, total, onPageChange }) {
  if (total <= 1) return null;
  const pages = [];
  for (let i = 1; i <= total; i++) pages.push(i);
  return (
    <nav>
      <ul className={styles.pagination}>
        <li className={`${styles.pageItem} ${current === 1 ? styles.disabled : ''}`}>
          <button className={styles.pageLink} onClick={() => onPageChange(current-1)}>Назад</button>
        </li>
        {pages.map(p => (
          <li key={p} className={`${styles.pageItem} ${p === current ? styles.active : ''}`}>
            <button className={styles.pageLink} onClick={() => onPageChange(p)}>{p}</button>
          </li>
        ))}
        <li className={`${styles.pageItem} ${current === total ? styles.disabled : ''}`}>
          <button className={styles.pageLink} onClick={() => onPageChange(current+1)}>Вперёд</button>
        </li>
      </ul>
    </nav>
  );
}