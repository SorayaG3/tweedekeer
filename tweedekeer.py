import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# dataset inladen
df = pd.read_csv('exclusieve_schoenen_verkoop_met_locatie.csv')

# verwachte kolomnamen in lowercase: 'merk', 'aantal', 'land'
df.columns = df.columns.str.lower()  # zet kolomnamen in lowercase

# controleer of de verwachte kolommen aanwezig zijn
required_columns = {'merk', 'aantal', 'land'}
if not required_columns.issubset(df.columns):
    st.error(f"de dataset moet de kolommen bevatten: {required_columns}")
    st.stop()

# titel
st.title('dashboard schoenverkoop')

# filteroptie
land_optie = st.sidebar.selectbox('selecteer land', sorted(df['land'].unique()))

# filter toepassen
filtered_df = df[df['land'] == land_optie]

# tabs
tab1, tab2 = st.tabs(['tab 1', 'tab 2'])

def toon_visuals(dataframe):
    # barchart
    st.subheader('barchart: aantal per merk')
    bar_df = dataframe.groupby('merk', as_index=False)['aantal'].sum()
    fig_bar = px.bar(bar_df, x='merk', y='aantal', color='merk')
    st.plotly_chart(fig_bar, use_container_width=True)

    # line chart met targetlijn
    st.subheader('line chart: aantal per merk met targetlijn')
    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(
        x=bar_df['merk'],
        y=bar_df['aantal'],
        mode='lines+markers',
        name='aantal'
    ))

    fig_line.add_trace(go.Scatter(
        x=bar_df['merk'],
        y=[10] * len(bar_df),
        mode='lines',
        name='target',
        line=dict(dash='dash', color='red')
    ))

    fig_line.update_layout(
        yaxis_title='aantal',
        xaxis_title='merk'
    )

    st.plotly_chart(fig_line, use_container_width=True)

# beide tabs tonen dezelfde visuals
with tab1:
    toon_visuals(filtered_df)

with tab2:
    toon_visuals(filtered_df)
