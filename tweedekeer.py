import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======= Header toevoegen ========
st.title("Dashboard Schoenverkoop")

# ======= Dummy dataset maken ========
df = pd.read_csv("exclusieve_schoenen_verkoop_met_locatie.csv")

# ======= Filters ========
st.sidebar.header("Filters")
selected_land = st.sidebar.selectbox("Selecteer Land", sorted(df['Land'].unique()))

# Filter toepassen
filtered_df = (df['Land'] == selected_land)]

# ======= Tabs ========
tab1, tab2 = st.tabs(["Aantal per Merk", "Aantal per Maand + Targetlijn"])

with tab1:
    st.subheader("Totaal aantal per Merk")
    grouped_merk = filtered_df.groupby('merk', as_index=False)['aantal'].sum()
    
    fig_merk = px.bar(grouped_merk, x='merk', y='aantal', color='merk',
                      title='Aantal per Merk',
                      labels={'Aantal': 'Aantal', 'Merk': 'Merk'})
    
    st.plotly_chart(fig_merk, use_container_width=True)

with tab2:
    st.subheader("Aantal per land met Targetlijn")
    grouped_maand = filtered_df.groupby('land', as_index=False)['aantal'].sum()
    
    # Kleurcodering per regel
    grouped_maand['Kleur'] = grouped_maand['aantal'].apply(lambda x: 'red' if x < 20 else 'green')
    
    fig_maand = go.Figure()
    fig_maand.add_trace(go.Bar(
        x=grouped_maand['aantal'],
        y=grouped_maand['maand'],
        orientation='h',
        marker_color=grouped_maand['Kleur'],
        name='aantal'
    ))
    
    # Targetlijn toevoegen
    fig_maand.add_shape(
        type='line',
        x0=20, x1=20,
        y0=-0.5, y1=len(grouped_maand)-0.5,
        line=dict(color='blue', width=2, dash='dash'),
        name='Target'
    )

    fig_maand.update_layout(
        title='Aantal per land met Targetlijn (20)',
        xaxis_title='aantal',
        yaxis_title='land',
        showlegend=False
    )

    st.plotly_chart(fig_maand, use_container_width=True)
