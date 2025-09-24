# Filename: full_day_tracker_enhanced.py

import streamlit as st
import pandas as pd
from datetime import date
import os
import matplotlib.pyplot as plt

# File to save logs
LOG_FILE = "daily_routine_logs.csv"

# Full-day routine blocks
routine_blocks = [
    "7–8 Wake & Activate",
    "8–9 Breakfast",
    "9–11 Deep Work #1",
    "11–11:15 Break",
    "11:15–12:30 Deep Work #2",
    "12:30–1 Admin & Review",
    "1–2 Lunch",
    "2–4 Implementation Work #1",
    "4–4:30 Break",
    "4:30–6:30 Implementation Work #2",
    "6:30–7:30 Friends/Family",
    "7:30–8:30 Dinner",
    "8:30–10:30 Implementation Work #3",
    "10:30–11 Wind-Down",
    "11–12 Sleep Prep"
]

st.title("🌞 Full-Day Routine Tracker (7 AM – 12 AM)")

# Sidebar - select day
st.sidebar.header("Select Day")
day = st.sidebar.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])

# Daily reminder
st.sidebar.info("💡 Daily Coach Tip: Focus on deep work first, social/family time later. Keep phone away during blocks!")

# Initialize form
st.header(f"✅ Track Your Routine for {day}")
with st.form("routine_form"):
    task_status = {}
    notes = {}
    
    for block in routine_blocks:
        col1, col2 = st.columns([1, 3])
        with col1:
            status = st.selectbox(f"{block}:", ["Not Done", "Done", "Skipped"], key=f"{day}_{block}_status")
        with col2:
            note = st.text_input(f"Notes for {block}", key=f"{day}_{block}_note")
        task_status[block] = status
        notes[block] = note
    
    submitted = st.form_submit_button("Save Today’s Progress")

    if submitted:
        # Prepare data row
        row = {"Date": str(date.today()), "Day": day}
        for block in routine_blocks:
            row[f"{block} Status"] = task_status[block]
            row[f"{block} Notes"] = notes[block]
        
        # Save to CSV
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        else:
            df = pd.DataFrame([row])
        df.to_csv(LOG_FILE, index=False)
        st.success("✅ Progress saved successfully!")

# Show weekly summary
if os.path.exists(LOG_FILE):
    st.header("📊 Weekly Summary & Completion Graph")
    df = pd.read_csv(LOG_FILE)

    # Filter last 6 days (Mon-Sat)
    df_week = df[df['Day'] != 'Sunday'].tail(6)

    # Count Done tasks per day
    completion = []
    for i, r in df_week.iterrows():
        done_count = sum([1 for b in routine_blocks if r[f"{b} Status"] == "Done"])
        completion.append(done_count)

    # Bar chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df_week['Day'], completion, color='green')
    ax.set_ylim(0, len(routine_blocks))
    ax.set_ylabel("Tasks Completed ✅")
    ax.set_title("Weekly Task Completion")
    st.pyplot(fig)

    # Show color-coded table
    st.subheader("Detailed Status Table")
    def color_status(val):
        if val == "Done":
            color = "background-color: lightgreen"
        elif val == "Skipped":
            color = "background-color: lightcoral"
        else:
            color = "background-color: lightgray"
        return color

    df_display = df_week.copy()
    status_cols = [f"{b} Status" for b in routine_blocks]
    st.dataframe(df_display.style.applymap(color_status, subset=status_cols))
