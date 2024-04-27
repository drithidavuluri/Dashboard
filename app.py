import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Social Media Influencer Analysis", layout="wide")

@st.cache_data
def load_data(filename):
    df = pd.read_csv(filename, encoding='utf-8', skipinitialspace=True)
    df.columns = df.columns.str.strip().str.replace("\n", " ").str.replace("  ", " ")

    def convert_k_m_to_number(x):
        if isinstance(x, str):
            x = x.strip()
            if 'K' in x:
                return float(x.replace('K', '')) * 1e3
            elif 'M' in x:
                return float(x.replace('M', '')) * 1e6
            elif x.isdigit():
                return float(x)
        try:
            return float(x)
        except (ValueError, TypeError):
            return None

    numeric_cols = ['Followers', 'Authentic engagement', 'Engagement avg', 'Subscribers', 'avg views', 'avg likes', 'avg comments']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(convert_k_m_to_number)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def generate_wordcloud(data):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(data)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Load data
instagram_df = load_data("instagram.csv")
youtube_df = load_data("youtube.csv")

# Sidebar for tab selection
selected_tab = st.sidebar.radio("Choose a tab", ["Instagram Data", "YouTube Data"])

if selected_tab == "Instagram Data":
    #st.header("Instagram Data Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        names = instagram_df['instagram name'].dropna()
        followers = instagram_df['Followers'].dropna()
        frequencies = dict(zip(names, followers))
        st.set_option('deprecation.showPyplotGlobalUse', False)
        generate_wordcloud(frequencies)
        st.pyplot()
    
    with col2:
        fig2 = px.scatter(instagram_df, x='Authentic engagement', y='Engagement avg',
                          size='Followers', color='Audience country(mostly)', title="Engagement by Country", height=300)
        st.plotly_chart(fig2, use_container_width=True)
    
    fig = px.histogram(instagram_df, x='Followers', title="Distribution of Instagram Followers")
    st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "YouTube Data":
    #st.header("YouTube Data Analysis")
    col1, col2 = st.columns([2, 3])
    
    with col1:
        top_youtubers = youtube_df.nlargest(10, 'Subscribers')
        fig4 = px.pie(top_youtubers, names='youtuber name', values='Subscribers', title="Top 10 YouTubers by Subscriber Count")
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        country_subscriber_totals = youtube_df.groupby('Audience Country').agg({'Subscribers': 'sum'}).reset_index()
        top_10_countries = country_subscriber_totals.nlargest(10, 'Subscribers')['Audience Country']
        filtered_data = youtube_df[youtube_df['Audience Country'].isin(top_10_countries)]
        
        aggregated_data = filtered_data.groupby(['Category', 'Audience Country']).agg({'Subscribers': 'sum'}).reset_index()
        fig5 = px.density_heatmap(
            aggregated_data, x='Audience Country', y='Category', z='Subscribers', 
            color_continuous_scale='Viridis', title="Subscribers Heatmap by Category and Country for Top 10 Countries",
            range_color=[0, 1e9]
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    bin_size_yt = st.slider('Select bin size for YouTube Subscribers', min_value=10, max_value=100, value=50, step=5, key='yt_bins')
    fig3 = px.histogram(filtered_data, x='Subscribers', nbins=bin_size_yt, title="Distribution of YouTube Subscribers")
    st.plotly_chart(fig3, use_container_width=True)
