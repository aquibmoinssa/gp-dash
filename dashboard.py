import streamlit as st
import pandas as pd
import plost
import json
import altair as alt
from sklearn.ensemble import IsolationForest

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.title('Mission Parameters Dashboard')

#st.sidebar.subheader('Heat map parameters')
#time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

#st.sidebar.subheader('Donut chart parameters')
#donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

st.sidebar.header('ML-powered Anomaly Detection')
st.sidebar.header('Mission: Hubble Space Telescope')
st.sidebar.header('Example: Orbital Parameters from TLEs')
st.sidebar.header('Source: Space-Track.org')
st.sidebar.markdown('''
---
''')
st.sidebar.subheader('Parameter Selection')
parameter = st.sidebar.selectbox(
    'Select parameter to visualize anomalies:',
    ('Period', 'Eccentricity', 'Mean Anomaly', 'Inclination')
)
# Sidebar slider for plot controls
st.sidebar.subheader('ML Plot Controls')
plot_height = st.sidebar.slider('Plot height', 300, 600, 400)
plot_width = st.sidebar.slider('Plot width', 600, 1000, 700)


# Row B

# URL to the JSON file on Google Drive
file_url = 'https://drive.google.com/uc?export=download&id=1HccDVUokzQ8WnG4XNLD1Du_IfT2B63Wq'

# Load the JSON file directly into a DataFrame
data = pd.read_json(file_url)

# Extract the relevant data for plotting
epochs = data['EPOCH']
periods = data['PERIOD'].astype(float)
eccentricity = data['ECCENTRICITY'].astype(float)
mean_anomaly = data['MEAN_ANOMALY'].astype(float)
mean_motion = data['MEAN_MOTION'].astype(float)
mean_motion_dot = data['MEAN_MOTION_DOT'].astype(float)
mean_motion_ddot = data['MEAN_MOTION_DDOT'].astype(float)
inclination = data['INCLINATION'].astype(float)

# Convert epochs to a datetime format for better plotting
epochs = pd.to_datetime(epochs)

# Create a DataFrame for easier manipulation
df = pd.DataFrame({
    'Epoch': epochs,
    'Period': periods,
    'Eccentricity': eccentricity,
    'Mean Anomaly': mean_anomaly,
    'Mean Motion': mean_motion,
    'Mean Motion Dot': mean_motion_dot,
    'Mean Motion DDot': mean_motion_ddot,
    'Inclination': inclination
})

# Train Isolation Forest model for anomaly detection
features = ['Period', 'Eccentricity', 'Mean Anomaly', 'Inclination']
model = IsolationForest(contamination=0.05, random_state=42)
df['Anomaly'] = model.fit_predict(df[features])

# Map anomaly labels to actual values (1 for normal, -1 for anomaly)
df['Anomaly'] = df['Anomaly'].map({1: 'Normal', -1: 'Anomaly'})

# Row A - Display the most recent values
st.markdown('### Most Recent Values:')
col1, col2, col3, col4, col5 = st.columns(5)

# Get the most recent values
latest_values = df.iloc[-1]

col1.metric("Period", f"{latest_values['Period']:.2f} minutes")
col2.metric("Eccentricity", f"{latest_values['Eccentricity']:.4f}")
col3.metric("Mean Anomaly", f"{latest_values['Mean Anomaly']:.2f} degrees")
col4.metric("Inclination", f"{latest_values['Inclination']:.2f} degrees")
col4.metric("Epoch", f"{latest_values['Epoch']}")
st.markdown("""<br><br>""", unsafe_allow_html = True)

# Create two columns
c1, c2 = st.columns((5, 5))

with c1:
    st.markdown('### HST Mean Anomaly June 2023 - June 2024')
    line_chart_period = alt.Chart(df).mark_line(color='orange').encode(
        x='Epoch:T',
        y='Mean Anomaly:Q'
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(line_chart_period, use_container_width=True)

with c2:
    st.markdown('### HST Eccentricity June 2023 - June 2024')
    line_chart_eccentricity = alt.Chart(df).mark_line(color='blue').encode(
        x='Epoch:T',
        y='Eccentricity:Q'
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(line_chart_eccentricity, use_container_width=True)

# Row C as two columns
c3, c4 = st.columns((7, 3))

with c3:
    st.markdown('### HST Orbital Period June 2023 - June 2024')
    chart = alt.Chart(df).mark_line(color='green').encode(
        x=alt.X('Epoch:T', title='Epoch'),
        y=alt.Y('Period:Q', title='Orbital Period (minutes)', scale=alt.Scale(domain=[94.8, 95.2]))
    ).properties(
        height=400,
        width=600  # Adjust width as well
    )
    st.altair_chart(chart, use_container_width=True)

with c4:
    st.markdown('### HST Inclination June 2023 - June 2024')
    line_chart_inclination = alt.Chart(df).mark_line(color='red').encode(
        x=alt.X('Epoch:T', title='Epoch'),
        y=alt.Y('Inclination:Q', title='Inclination', scale=alt.Scale(domain=[28.45, 28.49]))
    ).properties(
        height=400,
        width=600  # Adjust width as well
    )
    st.altair_chart(line_chart_inclination, use_container_width=True)

st.title('Anomaly Detection Using ML')

# Row D - Anomaly Detection Results
st.markdown(f'### Anomaly Detection Results for {parameter}')
anomaly_chart = alt.Chart(df).mark_point().encode(
    x=alt.X('Epoch:T', title='Epoch'),
    y=alt.Y(f'{parameter}:Q', title='Orbital Period (minutes)', scale=alt.Scale(domain=[94.8, 95.2])),
    color=alt.Color('Anomaly:N', scale=alt.Scale(domain=['Normal', 'Anomaly'], range=['green', 'red'])),
    tooltip=['Epoch', parameter, 'Anomaly']
).properties(
    width=plot_width,
    height=plot_height
)
st.altair_chart(anomaly_chart, use_container_width=True)
