import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import CourseView from './pages/CourseView'

function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold tracking-tight text-blue-600">CourseForge AI</h1>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/course/:id" element={<CourseView />} />
            {/* Will add generating/:id routes in next features*/}
          </Routes>
        </div>
      </main>
    </div>
  )
}

export default App
