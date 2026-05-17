import { Routes, Route } from 'react-router-dom'
import PeopleTable from './components/PeopleTable'
import PersonPage from './components/PersonPage'

function App() {
  return (
    <div className="container mt-4">
      <h1>База данных людей</h1>
      <Routes>
        <Route path="/" element={<PeopleTable />} />
        <Route path="/person/:id" element={<PersonPage />} />
        <Route path="/random" element={<PersonPage random />} />
      </Routes>
    </div>
  )
}

export default App