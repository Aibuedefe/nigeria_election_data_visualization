import streamlit as st
import pandas as pd
import plotly_express as px
import folium
from streamlit_folium import st_folium
import seaborn as sns
import plost
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('Dashboard `election`')



DASHBOARD_TITLE = 'Nigeria Election'
DASHBOARD_SUBTITLE = 'Source : https://elections.dataphyte.com/elections/2023-presidential-election?tab=results'

def display_party_facts(data, state_name, title, string_format='${:,}', is_median=False):
    #data = data[(data['Year'] == year) & (data['Quarter'] == quarter)]
    #data = data[data['Report Type'] == report_type]
    if state_name:
        data = data[data['State'] == state_name]
    data.drop_duplicates(inplace=True)
    if is_median:
        total = data['APC'].sum() / len(data['APC']) if len(data) else 0
    else:
        total = data['APC'].sum()
    st.metric(title, string_format.format(round(total)))

def display_party_filter(data, party_name):
    colum = data.columns
    # Generate a unique key based on state_name
    selectbox_key = f"state_selectbox_{party_name}"
    party_list = [''] + list(colum.unique())
    party_list.sort()
    party_index = party_list.index(party_name) if party_name and party_name in party_list else 0
    return st.sidebar.selectbox('State', party_list, party_index, key=selectbox_key)



def display_map(data, state_name):
    data = data[(data['State'] == state_name)]

    map = folium.Map(location=[9.0820, 8.6753], zoom_start=6, scrollWheelZoom=False, tiles='CartoDB positron')

    choropleth = folium.Choropleth (
        geo_data='stategeo.geojson', 
        data=data,
        columns=('State', 'APC'), 
        key_on='feature.properties.admin1Name',
        line_opacity=0.8,
        highlight=True
        )
    choropleth.geojson.add_to(map)

    data = data.set_index('State')
   
    
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['admin1Name']
        feature['properties']['apc'] = 'APC Votes   ' + str('{:,}'.format(data.loc[state_name,'APC']) if state_name in list(data.index) else 'N/A')
        feature['properties']['lp'] = 'LP Votes     ' + str('{:,}'.format(data.loc[state_name,'LP']) if state_name in list(data.index) else 'N/A')
        feature['properties']['nnpp'] = 'NNPP Votes ' + str('{:,}'.format(data.loc[state_name,'NNPP']) if state_name in list(data.index) else 'N/A')
        feature['properties']['pdp'] = 'PDP Votes   ' + str('{:,}'.format(data.loc[state_name,'PDP']) if state_name in list(data.index) else 'N/A')
        feature['properties']['a'] = 'A Votes       ' + str('{:,}'.format(data.loc[state_name,'A']) if state_name in list(data.index) else 'N/A')
        feature['properties']['aa'] = 'AA Votes     ' + str('{:,}'.format(data.loc[state_name,'AA']) if state_name in list(data.index) else 'N/A')
        feature['properties']['aac'] = 'AAC Votes   ' + str('{:,}'.format(data.loc[state_name,'AAC']) if state_name in list(data.index) else 'N/A')
        feature['properties']['adc'] = 'ADC Votes   ' + str('{:,}'.format(data.loc[state_name,'ADC']) if state_name in list(data.index) else 'N/A')
        feature['properties']['adp'] = 'ADP Votes   ' + str('{:,}'.format(data.loc[state_name,'ADP']) if state_name in list(data.index) else 'N/A')
        feature['properties']['apga'] = 'APGA Votes ' + str('{:,}'.format(data.loc[state_name,'APGA']) if state_name in list(data.index) else 'N/A')
        feature['properties']['apm'] = 'APM Votes   ' + str('{:,}'.format(data.loc[state_name,'APM']) if state_name in list(data.index) else 'N/A')
        feature['properties']['app'] = 'APP Votes   ' + str('{:,}'.format(data.loc[state_name,'APP']) if state_name in list(data.index) else 'N/A')
        feature['properties']['bp'] = 'BP Votes     ' + str('{:,}'.format(data.loc[state_name,'BP']) if state_name in list(data.index) else 'N/A')
        feature['properties']['nrm'] = 'NRM Votes   ' + str('{:,}'.format(data.loc[state_name,'NRM']) if state_name in list(data.index) else 'N/A')
        feature['properties']['prp'] = 'PRP Votes   ' + str('{:,}'.format(data.loc[state_name,'PRP']) if state_name in list(data.index) else 'N/A')
        feature['properties']['sdp'] = 'SDP Votes   ' + str('{:,}'.format(data.loc[state_name,'SDP']) if state_name in list(data.index) else 'N/A')
        feature['properties']['ypp'] = 'YPP Votes   ' + str('{:,}'.format(data.loc[state_name,'YPP']) if state_name in list(data.index) else 'N/A')
        feature['properties']['zlp'] = 'ZLP Votes   ' + str('{:,}'.format(data.loc[state_name,'ZLP']) if state_name in list(data.index) else 'N/A')


    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['admin1Name','apc','lp','nnpp','pdp','a','aac','adc','adp','apga','apm','app','bp', 'nrm', 'prp', 'sdp', 'ypp', 'zlp'], labels=False)
    )

    st_map = st_folium(map, width=700, height=450)

    state_name = ''
    if st_map['last_active_drawing']:
        state_name = st_map['last_active_drawing']['properties']['admin1Name']
    return state_name    


    

def main():
    st.title(DASHBOARD_TITLE)
    st.caption(DASHBOARD_SUBTITLE)

    #LOAD DATA
    data = pd.read_excel("data.xlsx")

    #DISPLAY METRICS


    colum = data.columns
    party_list = list(colum.unique())
    with st.sidebar:
        st.subheader("Configure the plot")
        party = st.sidebar.selectbox(label = "Choose a party", options = party_list)



    

    # Row A
    st.subheader(party)
    #col1, col2, col3 = st.columns(3)

    #col1.metric("Total Number of votes", "69,999", "2.345")
    #col2.metric("Total Number of in Abia", "69,999", "99")
    #col3.metric("Total Number of Sokoto", "69,999", "999")
    #with col1:
    #    display_party_facts(data, state_name, 'State Fraud/Other Count', f'# of {state_name} Reports', string_format='{:,}')
    #with col2:
    #    display_party_facts(data, state_name, 'Overall Median Losses Qtr', 'Median $ Loss', is_median=True)
    #with col3:
    #    display_party_facts(data, state_name, 'Total Number of Votes', 'Total $ Loss')        



    #DiSPLAY FILTER AND MAP
    state_name = data['State']
    state_name = display_map(data,state_name)
    colum = data.columns
    #party_name =  display_party_filter(data, colum)
    #party = display_party_filter()

    

    st.set_option('deprecation.showPyplotGlobalUse', False)
    fig, ax_bar =  plt.subplots()

    sns.barplot(
        x=data.index, y=party, data=data,palette='YlGnBu', ax=ax_bar
        )
    
    ax_bar.set_title("Bar Chart")
   

    fig.set_tight_layout(True)
    st.pyplot(fig)

    
    fig6, (ax_line) =  plt.subplots()

    sns.lineplot(
        x=data.index, y=party, data=data, ax=ax_line
        )
    
    ax_line.set_title("Line Plot")
   

    fig6.set_tight_layout(True)
    st.pyplot(fig6)

    fig8, (ax_scatter) =  plt.subplots()

    sns.scatterplot(
        x=data.index, y=party, data=data, ax=ax_scatter
        )

    
    fig8.set_tight_layout(True)
    st.pyplot(fig8)

    fig1, (ax_hist) =  plt.subplots()

    sns.histplot(
        x=data[party], kde=True,bins=15, ax=ax_hist
        )
    
    ax_hist.set_title("Histogram Plot")
   

    fig1.set_tight_layout(True)
    st.pyplot(fig1)

    fig2, (ax_scatter,ax_heat) =  plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(20,15)
    )
    
    sns.jointplot(
        x=data.index, y=party, data=data,kind='kde', fill= True, cmap='YlGnBu', ax=ax_heat
        )
    sns.scatterplot(
        x=data.index, y=party, data=data, ax=ax_scatter
        )
    fig2.set_tight_layout(True)
    st.pyplot()

    fig5 = px.pie(data, names="State", values=party, hole=0.5 )
    fig5.update_layout(title_text= party, title_x=0.2)
       
    st.plotly_chart(fig5)

    # create the plot
    title = f" {party}"
    fig = px.line(data, x = "State", y = party, title = title, labels={"value": f"{party}"})

    # display the plot
    st.plotly_chart(fig, use_container_width=True)

    


if __name__ == '__main__':
    main()