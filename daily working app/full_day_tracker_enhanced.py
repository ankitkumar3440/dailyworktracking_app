import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

st.set_page_config(page_title="Daily Work Tracker", layout="wide")
st.title("📅 Daily Work & Deep Focus Tracker")

# -------------------------
# File to save logs
# -------------------------
LOG_FILE = "daily_routine_logs.csv"

# -------------------------
# Daily routine schedule
# -------------------------
routine = [
    ("7:00-8:00", "Wake up & Morning Prep"),
    ("8:00-9:00", "Breakfast"),
    ("9:00-11:00", "Deep Work #1"),
    ("11:00-11:15", "Short Break"),
    ("11:15-12:30", "Deep Work #2"),
    ("12:30-13:00", "Admin / Review"),
    ("13:00-14:00", "Lunch"),
    ("14:00-16:00", "Implementation / Tasks"),
    ("16:00-17:00", "Talk with Family / Friends"),
    ("17:00-18:00", "Implementation / Tasks"),
    ("18:00-19:00", "Dinner"),
    ("19:00-21:00", "Deep Work / Learning"),
    ("21:00-22:00", "Relax / Plan Tomorrow"),
    ("22:00-23:00", "Sleep Prep")
]

# -------------------------
# Time-based reminder
# -------------------------
now = datetime.now()
current_hour = now.hour + now.minute / 60

reminder = ""
if 7 <= current_hour < 8:
    reminder = "⏰ Wake up & Morning Prep!"
elif 8 <= current_hour < 9:
    reminder = "⏰ Breakfast time! Fuel up for focus."
elif 9 <= current_hour < 11:
    reminder = "⏰ Deep Work #1: Focus on your top priority."
elif 11 <= current_hour < 11.25:
    reminder = "⏰ Short Break: Stretch & breathe."
elif 11.25 <= current_hour < 12.5:
    reminder = "⏰ Deep Work #2: Continue tasks."
elif 12.5 <= current_hour < 13:
    reminder = "⏰ Admin / Review: Wrap up morning tasks."
elif 13 <= current_hour < 14:
    reminder = "⏰ Lunch time!"
elif 14 <= current_hour < 16:
    reminder = "⏰ Implementation / Tasks"
elif 16 <= current_hour < 17:
    reminder = "⏰ Talk with Family / Friends"
elif 17 <= current_hour < 18:
    reminder = "⏰ Implementation / Tasks"
elif 18 <= current_hour < 19:
    reminder = "⏰ Dinner time!"
elif 19 <= current_hour < 21:
    reminder = "⏰ Deep Work / Learning"
elif 21 <= current_hour < 22:
    reminder = "⏰ Relax / Plan Tomorrow"
elif 22 <= current_hour < 23:
    reminder = "⏰ Sleep Prep"

if reminder:
    st.info(reminder)

# -------------------------
# Daily task logging
# -------------------------
st.subheader("Log your completed tasks today")
task_input = st.text_area("What did you accomplish today?")
if st.button("Log Task"):
    if task_input.strip():
        today = date.today().isoformat()
        log_entry = pd.DataFrame([[today, task_input]], columns=["Date", "Task"])
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            df = pd.concat([df, log_entry], ignore_index=True)
        else:
            df = log_entry
        df.to_csv(LOG_FILE, index=False)
        st.success("✅ Task logged!")
    else:
        st.warning("Please enter a task before logging.")

# -------------------------
# Show past week summary
# -------------------------
st.subheader("Past Tasks")
if os.path.exists(LOG_FILE):
    df = pd.read_csv(LOG_FILE)
    st.dataframe(df.tail(20))  # show last 20 entries

    # Show bar chart: tasks per day
    df['Date'] = pd.to_datetime(df['Date'])
    summary = df.groupby(df['Date'].dt.date).count()['Task'].reset_index()
    summary.rename(columns={'Task': 'Tasks Completed'}, inplace=True)
    summary.set_index('Date', inplace=True)
    
    st.bar_chart(summary)
else:
    st.info("No tasks logged yet.")

# -------------------------
# Routine overview
# -------------------------
st.subheader("📌 Daily Routine Overview")
routine_df = pd.DataFrame(routine, columns=["Time", "Activity"])
st.table(routine_df)
