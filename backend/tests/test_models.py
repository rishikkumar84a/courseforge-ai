import pytest
from models.course import Course, Module, Lesson, QuizQuestion

def test_course_creation():
    course = Course(topic="Machine Learning")
    assert course.id is not None
    assert course.topic == "Machine Learning"
    assert course.status == "generating"
    assert isinstance(course.modules, list)
    assert len(course.modules) == 0

def test_module_lesson_relationship():
    lesson = Lesson(
        title="What is ML?", 
        content="Intro content", 
        key_points=["Concept 1"], 
        order=1
    )
    module = Module(title="Basics", order=1, lessons=[lesson])
    
    assert len(module.lessons) == 1
    assert module.lessons[0].title == "What is ML?"
    assert module.lessons[0].key_points == ["Concept 1"]
    
def test_quiz_question():
    question = QuizQuestion(
        question="What is True?",
        options=["A", "B", "C"],
        correct_answer="A",
        explanation="Since A is True."
    )
    assert question.question == "What is True?"
    assert question.correct_answer == "A"
