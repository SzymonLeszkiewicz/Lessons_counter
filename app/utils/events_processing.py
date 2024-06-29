"""This module is responsible for processing the events data."""
import pandas as pd
import streamlit as st


def save_lessons_to_df(events):
    """Save lessons to a DataFrame.

    Args:
        ''events'' (list): List of events.
    Returns:
        ''lessons'' (DataFrame): DataFrame with lessons.
    """
    lessons = pd.DataFrame(columns=['Date', 'Time', 'Student'], index=[])
    for event in events:
        student = event['summary']
        start = event['start'].get('dateTime', event['start'].get('date'))

        if 'dateTime' not in event['start']:
            st.warning(
                f'Wykryto wydarzenie całodobowe! -----> '
                f'{student} {start} |popraw to wydarzenie w kalendarzu',
                icon="⚠️")
            continue
        date = start.split('T')[0]
        time = start.split('T')[1].split('+')[0]

        lessons = pd.concat([lessons, pd.DataFrame({'Date': [date],
                                                    'Time': [time],
                                                    'Student': [student]})])
        lessons = lessons.sort_values(by='Student')
    return lessons
