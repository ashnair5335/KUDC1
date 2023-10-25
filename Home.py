import random
import streamlit as st
import sqlite3
from streamlit_calendar import calendar
import datetime
import pandas as pd

# Create or connect to an SQLite database
conn = sqlite3.connect('planner.db')
cursor = conn.cursor()

# Create tables for tasks, notes, and subjects if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS due_date (
        id INTEGER PRIMARY KEY,
        due_date_input TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urgency_rating
        id INTERGER PRIMARY KEY,
        urgency TEXT
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        note TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        subject TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasklist (
        id INTEGER PRIMARY KEY,
        task_list TEXT
    )
''')

conn.commit()

# Title and introduction
st.title("High School Planner")
st.write("Welcome to your digital planner!")

# To-Do List
st.subheader("To-Do List")
task = st.text_input("Add a new task:")
urgency = st.text_input ("Add urgency rating, 1-9") 
due_date_input = st.date_input("Due date:", value=None)

if st.button("Add Task"):
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    cursor.execute("INSERT INTO due_date (due_date_input) VALUES (?)", (due_date_input,))
    cursor.execute("INSERT INTO urgency_rating (urgency) VALUES (?)", (urgency)

    
    st.write(f"Task added: {task}")



# View all tasks
#if st.button("View All Tasks"):
st.subheader("All Tasks")
tasks = cursor.execute("SELECT task FROM tasks").fetchall()
due_dates = cursor.execute("SELECT due_date_input FROM due_date").fetchall()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Name")
    for i, task in enumerate(tasks):
        st.write(f"{list(task)[0]}")

with col2:
    st.subheader("Due Date")
    for i, due_date_input in enumerate(due_dates):
        st.write(f"{list(due_date_input)[0]}")

with col3:
    st.subheader("Done?")
    for i, task in enumerate(tasks):
        st.checkbox("", key=i)

with col4:
    st.subheader("Urgency")
    for i, task in enumerate(tasks):
        st.number_input("", label_visibility="collapsed", min_value=0, max_value=9, key=random.random())

# Notes and Resources
st.subheader("Notes and Resources")
note = st.text_area("Add a note or resource:")
if st.button("Save Note"):
    cursor.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    st.write(f"Note saved: {note}")

# View all notes/resources
if st.button("View All Notes"):
    st.subheader("All Notes")
    notes = cursor.execute("SELECT note FROM notes").fetchall()
    #due_date_db = cursor.execute("SELECT ")
    for i, note in enumerate(notes):
        st.write(f"{i + 1}. {note[0]}")

# Subjects and Courses
st.subheader("Subjects and Courses")
subject = st.text_input("Add a subject or course:")
if st.button("Add Subject"):
    cursor.execute("INSERT INTO subjects (subject) VALUES (?)", (subject,))
    conn.commit()
    st.write(f"Subject added: {subject}")

# View all subjects/courses
if st.button("View All Subjects"):
    st.subheader("All Subjects")
    subjects = cursor.execute("SELECT subject FROM subjects").fetchall()
    for i, subject in enumerate(subjects):
        st.write(f"{i + 1}. {subject[0]}")

# Close the database connection
conn.close()
