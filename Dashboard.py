import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Ensure Streamlit uses cache efficiently
st.set_page_config(page_title="Social Media Influencer Analysis", layout="wide")

# Data loading and preprocessing
@st.cache_data
def load_data(filename):
    df = pd.read_csv(filename, encoding='utf-8', skipinitialspace=True)
    df.columns = df.columns.str.strip().str.replace("\n", " ").str.replace("  ", " ")

    def convert_k_m_to_number(x):
        if isinstance(x, str):
            x = x.strip()  # Clean any leading/trailing whitespace
            if 'K' in x:
                return float(x.replace('K', '')) * 1e3
            elif 'M' in x:
                return float(x.replace('M', '')) * 1e6
            elif x.isdigit():
                return float(x)  # Ensure string digits are converted to float
        try:
            return float(x)
        except (ValueError, TypeError):
            return None  # Return None if conversion fails

    numeric_cols = ['Followers', 'Authentic engagement', 'Engagement avg', 'Subscribers', 'avg views', 'avg likes', 'avg comments']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(convert_k_m_to_number)
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Use coerce to handle any remaining non-numeric values

    return df

def generate_wordcloud(data):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(data)
    plt.figure(figsize=(5, 1.5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Example usage:
instagram_df = load_data("instagram.csv")
youtube_df = load_data("youtube.csv")

# Aggregate data and identify top 10 countries
country_subscriber_totals = youtube_df.groupby('Audience Country').agg({'Subscribers': 'sum'}).reset_index()
top_10_countries = country_subscriber_totals.nlargest(10, 'Subscribers')['Audience Country']
filtered_data = youtube_df[youtube_df['Audience Country'].isin(top_10_countries)]

# Data Visualization in Streamlit
with st.container():
    tab1, tab2 = st.tabs(["Instagram Data", "YouTube Data"])

    with tab1:
        # First row for scatter plot and word cloud
        row1_col1, row1_col2 = st.columns([1, 1])
        with row1_col1:
            #st.write("### Word Cloud of Instagram Names")
            names = instagram_df['instagram name'].dropna()
            followers = instagram_df['Followers'].dropna()
            frequencies = dict(zip(names, followers))
            st.set_option('deprecation.showPyplotGlobalUse', False)
            generate_wordcloud(frequencies)
            st.pyplot()

        with row1_col2:
            fig2 = px.scatter(instagram_df, x='Authentic engagement', y='Engagement avg',
                              size='Followers', color='Audience country(mostly)', title="Engagement by Country", height=300)
            st.plotly_chart(fig2, use_container_width=True)

        # Second row for histogram
        with st.container():
            #bin_size_ig = st.slider('Select bin size for Instagram Followers', min_value=10, max_value=100, value=50, step=5, key='ig_bins')
            fig = px.histogram(instagram_df, x='Followers', title="Distribution of Instagram Followers")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns([2, 3])
        with col1:
            top_youtubers = youtube_df.nlargest(10, 'Subscribers')
            fig4 = px.pie(top_youtubers, names='youtuber name', values='Subscribers', title="Top 10 YouTubers by Subscriber Count")
            st.plotly_chart(fig4, use_container_width=True)

        with col2:
            aggregated_data = filtered_data.groupby(['Category', 'Audience Country']).agg({'Subscribers': 'sum'}).reset_index()
            fig5 = px.density_heatmap(
                aggregated_data, x='Audience Country', y='Category', z='Subscribers', 
                color_continuous_scale='Viridis', 
                title="Subscribers Heatmap by Category and Country for Top 10 Countries",
                range_color=[0, 1e9]  # Set range from 0 to 1 billion
            )
            st.plotly_chart(fig5, use_container_width=True)

        col3 = st.container()
        with col3:
            bin_size_yt = st.slider('Select bin size for YouTube Subscribers', min_value=10, max_value=100, value=50, step=5, key='yt_bins')
            fig3 = px.histogram(filtered_data, x='Subscribers', nbins=bin_size_yt, title="Distribution of YouTube Subscribers")
            st.plotly_chart(fig3, use_container_width=True)
