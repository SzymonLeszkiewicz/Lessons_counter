"""Streamlit app for counting the number of lessons in a given month."""
import streamlit as st
from datetime import datetime
from utils.gc_calendar import (authenticate_google_calendar,
                               get_events, list_calendars)

st.set_page_config(
    page_title="Lessons counter",
    page_icon=":calendar:",
    layout="wide",
    initial_sidebar_state="expanded",
)
col1, col2 = st.columns(2)

with col1:
    st.write("# GC Lessons Counter 📅")
    st.write("This app will count the number of lessons in a given month.")
    service = authenticate_google_calendar()
    calendar_lists = list_calendars(service)

    # Load calendar from session or set it
    st.write("### Select calendar:")
    if 'calendar_id' not in st.session_state:
        calendar_id = st.selectbox("Choose the calendar", calendar_lists)
        st.session_state['calendar_id'] = calendar_id
    else:
        calendar_id = st.selectbox("Choose the calendar",
                                   calendar_lists,
                                   index=calendar_lists.index(
                                       st.session_state['calendar_id'])
                                   )
        st.session_state['calendar_id'] = calendar_id
    st.write("### Select month:")

    # Load month from session or set it
    if 'month' not in st.session_state:
        month = st.selectbox("Choose the month", list(
            range(1, 13)), index=datetime.now().month - 1)
        st.session_state['month'] = month
    else:
        month = st.selectbox("Choose the month", list(
            range(1, 13)), index=st.session_state['month'] - 1)
        st.session_state['month'] = month

    # Load year from session or set it
    st.write("### Select year:")
    if 'year' not in st.session_state:
        year = st.selectbox("Choose the year", list(
            range(2021, 2025)), index=datetime.now().year - 2021)
        st.session_state['year'] = year
    else:
        year = st.selectbox("Choose the year", list(
            range(2021, 2025)), index=st.session_state['year'] - 2021)
        st.session_state['year'] = year

    try:
        events = get_events(service, calendar_id, month, year)
        st.session_state['cal_events'] = events
        if not events:
            st.write("No lessons found in this month.")
        else:
            st.write("## Lessons:")
            for event in events:
                st.write(f"- {event['summary']}")
            st.write(
                f"Total number of lessons in {month}/{year}:"
                f" {len(events)}")
    except NameError:
        st.write("Nie masz pełnych uprawnień do tego kalendarza!")

with col2:
    try:
        st.write(f"## Stats of {month}/{year} 📊")
        les_counter = len(events)
        st.write(f"Number of lessons in {month}/{year}:")
        st.write(les_counter)

    except NameError:
        st.write("Nie masz pełnych uprawnień do tego kalendarza!")
