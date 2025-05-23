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
import os

# Load the questions from the docs/qa.json file
st.title("100 Civic Test")

# Initialize session state variables if they don't exist
if 'questions' not in st.session_state:
    with open('docs/qa.json', 'r') as f:
        st.session_state.questions = json.load(f)['questions']
    st.session_state.current_index = 0
    st.session_state.test_mode = False
    st.session_state.user_answers = {}
    st.session_state.show_results = False

# Sidebar for mode selection
st.sidebar.title("Mode Selection")
if st.sidebar.button("Study Mode"):
    st.session_state.test_mode = False
    st.session_state.show_results = False
if st.sidebar.button("Test Mode"):
    st.session_state.test_mode = True
    st.session_state.show_results = False
    st.session_state.user_answers = {}

# Navigation buttons
col1, col2, col3 = st.columns(3)
if col1.button("Previous"):
    st.session_state.current_index = (st.session_state.current_index - 1) % len(st.session_state.questions)
if col2.button("Shuffle"):
    random.shuffle(st.session_state.questions)
    st.session_state.current_index = 0
if col3.button("Next"):
    st.session_state.current_index = (st.session_state.current_index + 1) % len(st.session_state.questions)

# Get current question
current_question = st.session_state.questions[st.session_state.current_index]

# Display question information
st.subheader(f"Question {st.session_state.current_index + 1} of {len(st.session_state.questions)}")
st.write(f"**Section:** {current_question['section']}")
st.write(f"**Category:** {current_question['category']}")
st.write(f"**Question:** {current_question['question']}")

if not st.session_state.test_mode:
    # Study mode - show the answer
    st.write(f"**Answer:** {current_question['answer']}")
else:
    # Test mode - collect user's answer
    user_answer = st.text_input("Your answer:", key=f"answer_{st.session_state.current_index}")
    st.session_state.user_answers[st.session_state.current_index] = user_answer

    # Show results button in test mode
    if st.button("Show Results"):
        st.session_state.show_results = True

    # Display results if requested
    if st.session_state.show_results:
        st.subheader("Test Results")
        correct_count = 0
        for idx, question in enumerate(st.session_state.questions):
            user_answer = st.session_state.user_answers.get(idx, "").strip().lower()
            correct_answer = question['answer'].lower()
            is_correct = user_answer in correct_answer
            if is_correct:
                correct_count += 1
            
            st.write(f"Q{idx + 1}: {'✅' if is_correct else '❌'}")
            st.write(f"Your answer: {user_answer}")
            st.write(f"Correct answer: {correct_answer}")
            st.write("---")
        
        score = (correct_count / len(st.session_state.questions)) * 100
        st.write(f"**Final Score: {score:.1f}%**")