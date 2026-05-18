// import { useState, useEffect } from 'react'
// import { Link } from 'react-router-dom'
// import { fetchPeople, loadPeople } from '../api'
// import Pagination from './Pagination'
// import LoadForm from './LoadForm'

// export default function PeopleTable() {
//   const [people, setPeople] = useState([])
//   const [currentPage, setCurrentPage] = useState(1)
//   const [totalPages, setTotalPages] = useState(1)
//   const [loading, setLoading] = useState(false)
//   const limit = 20

//   const loadData = async (page) => {
//     setLoading(true)
//     try {
//       const data = await fetchPeople(page, limit)
//       setPeople(data.items)
//       setCurrentPage(data.page)
//       setTotalPages(data.pages)
//     } catch (err) {
//       console.error(err)
//     } finally {
//       setLoading(false)
//     }
//   }

//   useEffect(() => {
//     loadData(1)
//   }, [])

//   const handlePageChange = (page) => {
//     loadData(page)
//   }

//   const handleLoad = async (count) => {
//     try {
//       await loadPeople(count)
//       loadData(1) 
//     } catch (err) {
//       alert('Ошибка загрузки')
//     }
//   }

//   if (loading) return <div className="text-center">Загрузка...</div>

//   return (
//     <>
//       <LoadForm onLoad={handleLoad} />
//       <table className="table table-striped table-bordered mt-3">
//         <thead className="table-dark">
//           <tr>
//             <th>Пол</th><th>Имя</th><th>Фамилия</th>
//             <th>Телефон</th><th>Email</th><th>Место проживания</th><th>Детали</th>
//           </tr>
//         </thead>
//         <tbody>
//           {people.map(p => (
//             <tr key={p.id}>
//               <td>{p.gender}</td>
//               <td>{p.first_name}</td>
//               <td>{p.last_name}</td>
//               <td>{p.phone}</td>
//               <td>{p.email}</td>
//               <td>{p.location}</td>
//               <td><Link to={`/person/${p.id}`} className="btn btn-sm btn-outline-info">Открыть</Link></td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//       <Pagination current={currentPage} total={totalPages} onPageChange={handlePageChange} />
//     </>
//   )
// }
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { fetchPeople, loadPeople } from '../api'
import Pagination from './Pagination'
import LoadForm from './LoadForm'
import styles from './PeopleTable.module.css'  

export default function PeopleTable() {
  const [people, setPeople] = useState([])
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(false)
  const limit = 20

  const loadData = async (page) => {
    setLoading(true)
    try {
      const data = await fetchPeople(page, limit)
      setPeople(data.items)
      setCurrentPage(data.page)
      setTotalPages(data.pages)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData(1)
  }, [])

  const handlePageChange = (page) => {
    loadData(page)
  }

  const handleLoad = async (count) => {
    try {
      await loadPeople(count)
      loadData(1) 
    } catch (err) {
      alert('Ошибка загрузки')
    }
  }
  if (loading) return <div className="text-center">Загрузка...</div>

  return (
    <>
      <LoadForm onLoad={handleLoad} />
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead className={styles.thead}>
            <tr>
              <th className={styles.th}>Пол</th>
              <th className={styles.th}>Имя</th>
              <th className={styles.th}>Фамилия</th>
              <th className={styles.th}>Телефон</th>
              <th className={styles.th}>Email</th>
              <th className={styles.th}>Место проживания</th>
              <th className={styles.th}>Детали</th>
            </tr>
          </thead>
          <tbody>
            {people.map(p => (
              <tr key={p.id} className={styles.rowHover}>
                <td className={styles.td}>{p.gender}</td>
                <td className={styles.td}>{p.first_name}</td>
                <td className={styles.td}>{p.last_name}</td>
                <td className={styles.td}>{p.phone}</td>
                <td className={styles.td}>{p.email}</td>
                <td className={styles.td}>{p.location}</td>
                <td className={styles.td}>
                  <Link to={`/person/${p.id}`} className={styles.detailButton}>
                    Открыть
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Pagination current={currentPage} total={totalPages} onPageChange={handlePageChange} />
    </>
  )
}