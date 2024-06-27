import streamlit as st
import pandas as pd
import plost
import json
import altair as alt

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('GP Dashboard')

st.sidebar.subheader('Heat map parameters')
#time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

st.sidebar.subheader('Donut chart parameters')
donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

st.sidebar.subheader('Line chart parameters')
# Sidebar slider to specify plot height
plot_height = st.sidebar.slider('Specify plot height', 300, 600, 400)
#plot_width = st.sidebar.slider('Specify plot width', 600, 1000, 700)



# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Row B

# URL to the JSON file on Google Drive
file_url = 'https://drive.google.com/uc?export=download&id=1HccDVUokzQ8WnG4XNLD1Du_IfT2B63Wq'

# Load the JSON file directly into a DataFrame
data = pd.read_json(file_url)

# Extract the relevant data for plotting
epochs = data['EPOCH']
periods = data['PERIOD'].astype(float)
eccentricity = data['ECCENTRICITY'].astype(float)

# Convert epochs to a datetime format for better plotting
epochs = pd.to_datetime(epochs)

# Create a DataFrame for easier manipulation
df = pd.DataFrame({'Epoch': epochs, 'Period': periods, 'Eccentricity': eccentricity})

seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

# Create a heatmap for Period
heatmap_period = alt.Chart(df).mark_rect().encode(
    x=alt.X('yearmonthdate(Epoch):O', title='Date'),
    y=alt.Y('hoursminutes(Epoch):O', title='Time of Day'),
    color=alt.Color('Period:Q', scale=alt.Scale(scheme='viridis'), title='Period (minutes)')
).properties(
    title='Heatmap of Period Over Time',
    height=300,
    width=400  # Adjust width to fit in the column
)

# Create a heatmap for Eccentricity
heatmap_eccentricity = alt.Chart(df).mark_rect().encode(
    x=alt.X('yearmonthdate(Epoch):O', title='Date'),
    y=alt.Y('hoursminutes(Epoch):O', title='Time of Day'),
    color=alt.Color('Eccentricity:Q', scale=alt.Scale(scheme='viridis'), title='Eccentricity')
).properties(
    title='Heatmap of Eccentricity Over Time',
    height=300,
    width=400  # Adjust width to fit in the column
)

# Create two columns
c1, c2 = st.columns((5, 5))

# Display the heatmaps in the Streamlit app
with c1:
    st.altair_chart(heatmap_period, use_container_width=True)

with c2:
    st.altair_chart(heatmap_eccentricity, use_container_width=True)

# Row C
# Set up the Streamlit app
st.title('Orbital Period of Hubble Space Telescope Over Time')

# Create an Altair chart with customizable height and width
chart = alt.Chart(df).mark_line().encode(
    x=alt.X('Epoch:T', title='Epoch'),
    y=alt.Y('Period:Q', title='Orbital Period (minutes)', scale=alt.Scale(domain=[94.8, 95.2]))
).properties(
    height=plot_height,
    width=700  # Adjust width as well
)

# Display the chart in the Streamlit app
st.altair_chart(chart, use_container_width=True)

#st.markdown('### HST Orbit')
#st.line_chart(df.set_index('Epoch')['Period'])
