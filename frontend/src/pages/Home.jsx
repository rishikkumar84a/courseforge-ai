import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { BookOpen } from 'lucide-react'

export default function Home() {
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [recentCourses, setRecentCourses] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    // Fetch recent courses (Placeholder till API is linked properly in separate branch or here)
    fetch('http://localhost:8000/api/courses/')
      .then(res => res.json())
      .then(data => {
        if(Array.isArray(data)) setRecentCourses(data)
      })
      .catch(err => console.error("Could not fetch recent courses", err))
  }, [])

  const handleGenerate = async (e) => {
    e.preventDefault()
    if (!topic.trim()) return
    
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/courses/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
      })
      const data = await response.json()
      if (data.course_id) {
        navigate(`/generating/${data.course_id}`)
      }
    } catch (error) {
      console.error(error)
      alert('Failed to generate course')
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Generate your next course
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Powered by autonomous AI agents.
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleGenerate}>
          <div className="rounded-md shadow-sm -space-y-px">
            <input
              name="topic"
              type="text"
              required
              className="appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="e.g. Machine Learning for Beginners"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
          </div>
          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {loading ? 'Starting Agents...' : 'Generate Course'}
            </button>
          </div>
        </form>

        {recentCourses.length > 0 && (
          <div className="mt-10">
            <h3 className="text-xl font-bold mb-4">Recent Courses</h3>
            <ul className="space-y-3">
              {recentCourses.map((course) => (
                <li key={course.id} className="bg-white p-4 rounded shadow flex justify-between items-center cursor-pointer hover:bg-gray-50" onClick={() => navigate(course.status === 'complete' ? `/course/${course.id}` : `/generating/${course.id}`)}>
                  <div className="flex items-center space-x-3">
                    <BookOpen className="h-5 w-5 text-blue-500" />
                    <span className="font-medium text-gray-900">{course.topic}</span>
                  </div>
                  <span className="text-xs text-gray-500 ml-4 py-1 px-2 bg-gray-100 rounded-full">{course.status}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
