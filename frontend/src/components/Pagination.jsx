import styles from './Pagination.module.css';

export default function Pagination({ current, total, onPageChange }) {
  if (total <= 1) return null;
  const getVisiblePages = () => {
    const delta = 5;
    const range = [];
    const rangeWithDots = [];
    let l;
    for (let i = 1; i <= total; i++) {
      if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
        range.push(i);
      }
    }
    range.forEach((i) => {
      if (l) {
        if (i - l === 2) {
          rangeWithDots.push(l + 1);
        } else if (i - l !== 1) {
          rangeWithDots.push('...');
        }
      }
      rangeWithDots.push(i);
      l = i;
    });
    return rangeWithDots;
  };

  const visiblePages = getVisiblePages();
  return (
    <nav>
      <ul className={styles.pagination}>
        {/* Кнопка "Назад" */}
        <li className={`${styles.pageItem} ${current === 1 ? styles.disabled : ''}`}>
          <button className={styles.pageLink} onClick={() => onPageChange(current - 1)}>
            Назад
          </button>
        </li>

        {visiblePages.map((page, index) => (
          <li
            key={index}
            className={`${styles.pageItem} ${page === current ? styles.active : ''} ${
              page === '...' ? styles.dots : ''
            }`}
          >
            {page === '...' ? (
              <span className={styles.dotsSpan}>...</span>
            ) : (
              <button className={styles.pageLink} onClick={() => onPageChange(page)}>
                {page}
              </button>
            )}
          </li>
        ))}
        <li className={`${styles.pageItem} ${current === total ? styles.disabled : ''}`}>
          <button className={styles.pageLink} onClick={() => onPageChange(current + 1)}>
            Вперёд
          </button>
        </li>
      </ul>
    </nav>
  );
}