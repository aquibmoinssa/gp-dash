import streamlit as st
import pandas as pd
import plost
import json

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('GP Dashboard')

st.sidebar.subheader('Heat map parameters')
time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

st.sidebar.subheader('Donut chart parameters')
donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

st.sidebar.subheader('Line chart parameters')
#plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)



# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Row B

# Load the JSON file to check its format
file_path = 'https://drive.google.com/uc?export=download&id=1HccDVUokzQ8WnG4XNLD1Du_IfT2B63Wq'

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
    json_valid = True
except json.JSONDecodeError as e:
    json_valid = False
    error_message = str(e)

json_valid, error_message if not json_valid else "No errors"

# Extract the relevant data for plotting
epochs = []
periods = []

for entry in data:
    epochs.append(entry['EPOCH'])
    periods.append(float(entry['PERIOD']))

# Convert epochs to a datetime format for better plotting
epochs = pd.to_datetime(epochs)

# Create a DataFrame for easier manipulation
df = pd.DataFrame({'Epoch': epochs, 'Period': periods})

seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

c1, c2 = st.columns((7,3))
with c1:
    st.markdown('### Heatmap')
    plost.time_hist(
    data=seattle_weather,
    date='date',
    x_unit='week',
    y_unit='day',
    color=time_hist_color,
    aggregate='median',
    legend=None,
    height=345,
    use_container_width=True)
with c2:
    st.markdown('### Donut chart')
    plost.donut_chart(
        data=stocks,
        theta=donut_theta,
        color='company',
        legend='bottom', 
        use_container_width=True)

# Row C
st.markdown('### HST Orbit')
st.line_chart(df.set_index('Epoch')['Period'], height = plot_height)
