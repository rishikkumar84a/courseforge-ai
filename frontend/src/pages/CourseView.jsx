import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

const CourseView = () => {
  const { id } = useParams();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeModule, setActiveModule] = useState(0);

  useEffect(() => {
    // In a real app, this would fetch from /api/courses/{id}
    const fetchCourse = async () => {
      setLoading(true);
      try {
        // Mock data for now until API is connected
        setTimeout(() => {
          setCourse({
            id,
            title: "Advanced Artificial Intelligence",
            description: "A comprehensive guide to modern AI techniques and applications.",
            modules: [
              {
                title: "Introduction to Machine Learning",
                lessons: [
                  "What is Machine Learning?",
                  "Types of Learning (Supervised, Unsupervised, RL)",
                ],
                content: "This module covers the basics of ML... (simulated content)",
              },
              {
                title: "Deep Learning Foundations",
                lessons: ["Neural Networks", "Backpropagation", "Activation Functions"],
                content: "Deep learning involves multiple layers... (simulated content)",
              },
            ],
            quiz: [
              { question: "What is the capital of AI?", options: ["Data", "Code", "Compute", "All"], answer: 3 },
            ],
          });
          setLoading(false);
        }, 1000);
      } catch (error) {
        console.error("Failed to fetch course", error);
        setLoading(false);
      }
    };

    fetchCourse();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-xl font-semibold text-gray-600 animate-pulse">Loading course content...</p>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-xl font-semibold text-red-600">Course not found.</p>
        <Link to="/" className="ml-4 text-indigo-600 hover:underline">Go back home</Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col md:flex-row">
      {/* Sidebar Navigation */}
      <aside className="w-full md:w-64 bg-white border-r border-gray-200 p-4 h-auto md:h-screen sticky top-0 overflow-y-auto shadow-sm tracking-tight">
        <div className="mb-8">
            <Link to="/" className="text-sm text-indigo-600 font-semibold uppercase tracking-wider mb-2 block hover:text-indigo-800 transition-colors">
                ← Back to Courses
            </Link>
            <h2 className="text-xl font-extrabold text-gray-900 leading-tight">{course.title}</h2>
        </div>
        
        <nav>
          <ul className="space-y-2">
            {course.modules.map((mod, idx) => (
              <li key={idx}>
                <button
                  onClick={() => setActiveModule(idx)}
                  className={`w-full text-left px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                    activeModule === idx
                      ? "bg-indigo-50 text-indigo-700 border-l-4 border-indigo-600 shadow-sm"
                      : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                  }`}
                >
                  <span className="block text-xs opacity-70 mb-1 font-semibold uppercase tracking-wider">Module {idx + 1}</span>
                  {mod.title}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 p-6 md:p-12 overflow-y-auto">
        <div className="max-w-4xl mx-auto">
            
            <header className="mb-10 pb-6 border-b border-gray-200">
                <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4">{course.modules[activeModule].title}</h1>
            </header>

            <article className="prose prose-indigo prose-lg max-w-none text-gray-700">
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 mb-8">
                     <h3 className="text-xl font-bold text-gray-900 mb-4 border-b border-gray-100 pb-2">Lessons</h3>
                     <ul className="list-disc pl-5 space-y-2 mb-6 text-gray-600">
                        {course.modules[activeModule].lessons.map((lesson, idx) => (
                            <li key={idx}>{lesson}</li>
                        ))}
                    </ul>
                    
                    <h3 className="text-xl font-bold text-gray-900 mb-4 border-b border-gray-100 pb-2 mt-8">Content</h3>
                    <p className="whitespace-pre-line leading-relaxed">{course.modules[activeModule].content}</p>
                </div>
            </article>

            {/* Quick nav buttons */}
            <div className="mt-12 flex justify-between items-center pt-8 border-t border-gray-200">
              <button 
                disabled={activeModule === 0}
                onClick={() => setActiveModule(prev => prev - 1)}
                className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
                  activeModule === 0 
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                  : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 shadow-sm'
                }`}
              >
                Previous Module
              </button>
              <button 
                 disabled={activeModule === course.modules.length - 1}
                 onClick={() => setActiveModule(prev => prev + 1)}
                className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
                  activeModule === course.modules.length - 1 
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                  : 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm hover:shadow-md'
                }`}
              >
                Next Module
              </button>
            </div>
            
        </div>
      </main>
    </div>
  );
};

export default CourseView;
