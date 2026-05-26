import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

const ProgressView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState("fetching_state");
  const [messages, setMessages] = useState([]);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // In a real app, this would poll /api/courses/status/{id}
    const pollStatus = () => {
      // Mock progress simulation
      const stages = [
        { status: "researching", message: "Researching course topic and aggregating constraints...", progress: 20 },
        { status: "building_curriculum", message: "Designing curriculum and module outlines...", progress: 40 },
        { status: "generating_content", message: "Drafting lesson content and materials...", progress: 60 },
        { status: "generating_quizzes", message: "Creating assessments and quizzes...", progress: 80 },
        { status: "completed", message: "Course generation complete! Finalizing...", progress: 100 },
      ];

      let currentStage = 0;
      
      const interval = setInterval(() => {
        if (currentStage < stages.length) {
            const stage = stages[currentStage];
            setStatus(stage.status);
            setMessages(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${stage.message}`]);
            setProgress(stage.progress);
            currentStage++;
        } else {
            clearInterval(interval);
            // Redirect to the course view once completed
            setTimeout(() => {
                navigate(`/course/${id}`);
            }, 2000);
        }
      }, 2000);
      
      return () => clearInterval(interval);
    };

    pollStatus();
  }, [id, navigate]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-sm border border-gray-200 p-8 md:p-12">
        <div className="text-center mb-10">
            <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Forging Your Course</h1>
            <p className="text-gray-500">Please wait while our AI agents construct the curriculum.</p>
        </div>

        {/* Progress Bar */}
        <div className="relative pt-1 mb-12">
            <div className="flex mb-2 items-center justify-between">
                <div>
                <span className="text-xs font-semibold inline-block py-1 px-3 uppercase rounded-full text-indigo-600 bg-indigo-100">
                    {status.replace("_", " ")}
                </span>
                </div>
                <div className="text-right">
                <span className="text-xs font-semibold inline-block text-indigo-600">
                    {progress}%
                </span>
                </div>
            </div>
            <div className="overflow-hidden h-3 mb-4 text-xs flex rounded bg-indigo-50">
                <div 
                    style={{ width: `${progress}%` }} 
                    className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-600 transition-all duration-500 ease-out"
                ></div>
            </div>
        </div>

        {/* Terminal/Log Output */}
        <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm text-green-400 h-64 overflow-y-auto shadow-inner">
             {messages.map((msg, idx) => (
                <div key={idx} className="mb-1 opacity-90 animate-fade-in-up">
                    <span className="text-gray-500 mr-2">&gt;</span>{msg}
                </div>
            ))}
             {status !== "completed" && (
                <div className="animate-pulse mt-2">
                     <span className="text-gray-500 mr-2">&gt;</span>_
                </div>
             )}
        </div>
      </div>
    </div>
  );
};

export default ProgressView;
