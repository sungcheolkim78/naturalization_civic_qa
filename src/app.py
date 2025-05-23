"""
This is streamlit app for the 100 Civic Test.

It will load the questions from the docs/qa.json file and display them in a random order.
It will have buttons to navigate through the questions (next, previous, shuffle)
It will initially show the answer so that user can learn the knowledge.
In the 'test' mode it will ask the users to fill the form with the answers.
It will show the results and the score.
"""

import streamlit as st
import json
import random
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Question:
    question: str
    answer: str
    section: str
    category: str

class QuizManager:
    def __init__(self, questions: List[Question]):
        self.questions = questions
        self.filtered_questions = questions.copy()
        self.current_index = 0
        self.test_mode = False
        self.user_answers: Dict[int, str] = {}
        self.show_results = False

    def filter_questions(self, section: str, category: str) -> None:
        if section == "All" and category == "All":
            self.filtered_questions = self.questions.copy()
        else:
            self.filtered_questions = [
                q for q in self.questions
                if (section == "All" or q.section == section) and
                   (category == "All" or q.category == category)
            ]
        self.current_index = 0

    def get_current_question(self) -> Question:
        return self.filtered_questions[self.current_index]

    def next_question(self) -> None:
        self.current_index = (self.current_index + 1) % len(self.filtered_questions)

    def previous_question(self) -> None:
        self.current_index = (self.current_index - 1) % len(self.filtered_questions)

    def shuffle_questions(self) -> None:
        random.shuffle(self.filtered_questions)
        self.current_index = 0

    def calculate_score(self) -> float:
        correct_count = sum(
            1 for idx, question in enumerate(self.filtered_questions)
            if self.user_answers.get(idx, "").strip().lower() in question.answer.lower()
        )
        return (correct_count / len(self.filtered_questions)) * 100

class UIComponents:
    @staticmethod
    def render_navigation(quiz_manager: QuizManager) -> None:
        col1, col2, col3 = st.columns(3)
        if col1.button("Previous"):
            quiz_manager.previous_question()
        if col2.button("Shuffle"):
            quiz_manager.shuffle_questions()
        if col3.button("Next"):
            quiz_manager.next_question()

    @staticmethod
    def render_question_info(quiz_manager: QuizManager) -> None:
        current_question = quiz_manager.get_current_question()
        st.subheader(f"Question {quiz_manager.current_index + 1} of {len(quiz_manager.filtered_questions)}")
        st.write(f"**Section:** {current_question.section} | **Category:** {current_question.category}")

    @staticmethod
    def render_question(question: Question) -> None:
        st.markdown("""
            <style>
            .question-box {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                margin: 10px 0;
            }
            </style>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="question-box"><h4>Question:</h4>{question.question}</div>', unsafe_allow_html=True)

    @staticmethod
    def render_answer(question: Question) -> None:
        st.markdown("""
            <style>
            .answer-box {
                background-color: #e6f3ff;
                padding: 20px;
                border-radius: 10px;
                margin: 10px 0;
            }
            </style>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="answer-box"><h4>Answer:</h4>{question.answer}</div>', unsafe_allow_html=True)

    @staticmethod
    def render_test_results(quiz_manager: QuizManager) -> None:
        st.subheader("Test Results")
        for idx, question in enumerate(quiz_manager.filtered_questions):
            user_answer = quiz_manager.user_answers.get(idx, "").strip().lower()
            correct_answer = question.answer.lower()
            is_correct = user_answer in correct_answer

            st.markdown("""
                <style>
                .result-box {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 5px 0;
                }
                </style>
            """, unsafe_allow_html=True)
            st.markdown(f'''
                <div class="result-box">
                    <h4>Q{idx + 1}: {'✅' if is_correct else '❌'}</h4>
                    <p><strong>Your answer:</strong> {user_answer}</p>
                    <p><strong>Correct answer:</strong> {correct_answer}</p>
                </div>
            ''', unsafe_allow_html=True)

        score = quiz_manager.calculate_score()
        st.markdown(f"<h2>Final Score: {score:.1f}%</h2>", unsafe_allow_html=True)

def load_questions() -> List[Question]:
    with open('docs/qa.json', 'r') as f:
        data = json.load(f)
        return [Question(**q) for q in data['questions']]

def initialize_session_state() -> QuizManager:
    if 'quiz_manager' not in st.session_state:
        questions = load_questions()
        st.session_state.quiz_manager = QuizManager(questions)
    return st.session_state.quiz_manager

def main():
    st.title("100 Civic Test")
    quiz_manager = initialize_session_state()
    ui = UIComponents()

    # Sidebar for mode selection and filtering
    st.sidebar.title("Mode Selection")
    if st.sidebar.button("Study Mode"):
        quiz_manager.test_mode = False
        quiz_manager.show_results = False
    if st.sidebar.button("Test Mode"):
        quiz_manager.test_mode = True
        quiz_manager.show_results = False
        quiz_manager.user_answers = {}

    # Add filtering options
    st.sidebar.title("Filter Questions")
    sections = sorted(list(set(q.section for q in quiz_manager.questions)))
    categories = sorted(list(set(q.category for q in quiz_manager.questions)))
    
    selected_section = st.sidebar.selectbox("Select Section", ["All"] + sections)
    selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)
    
    quiz_manager.filter_questions(selected_section, selected_category)

    # Navigation
    ui.render_navigation(quiz_manager)
    ui.render_question_info(quiz_manager)

    # Display current question
    current_question = quiz_manager.get_current_question()
    ui.render_question(current_question)

    if not quiz_manager.test_mode:
        ui.render_answer(current_question)
    else:
        # Test mode - collect user's answer
        user_answer = st.text_input("Your answer:", key=f"answer_{quiz_manager.current_index}")
        quiz_manager.user_answers[quiz_manager.current_index] = user_answer

        if st.button("Show Results"):
            quiz_manager.show_results = True

        if quiz_manager.show_results:
            ui.render_test_results(quiz_manager)

if __name__ == "__main__":
    main()