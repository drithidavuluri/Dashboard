import pandas as pd
import streamlit as st
import plotly.express as px
#from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Setting the page config
st.set_page_config(page_title="Social Media Influencer Analysis", layout="wide")

# Custom CSS to reduce padding and margins in the layout
def load_css():
    css = """
    <style>
        /* Reduce margins and padding globally */
        .main .block-container {
            
            padding-bottom: 0rem;
        }
        .stMarkdown, .stDataFrame, .stPlotlyChart {
            margin-bottom: -40px;  /* Reduce space below the elements */
        }
        /* Specific targeting of padding and margins around plot containers */
        .element-container {
            margin-bottom: -40px;
            padding-bottom: -40px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

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

# def generate_wordcloud(data):
#     wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(data)
#     plt.figure(figsize=(10, 5))
#     #plt.title('Word Cloud', fontsize=30)
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis('off')
#     plt.show()

# Load data
instagram_df = load_data("instagram.csv")
youtube_df = load_data("youtube.csv")

# Sidebar for tab selection
selected_tab = st.sidebar.radio("Choose a tab", ["Instagram Data", "YouTube Data"])

if selected_tab == "Instagram Data":
    col1, col2 = st.columns(2)
    
    with col1:
        top_instagram_influencers = instagram_df.nlargest(10, 'Followers')  # Get top 10 influencers by follower count
        fig1 = px.bar(top_instagram_influencers, x='instagram name', y='Followers', height=300,
                      title="Top 10 Instagram Influencers by Followers", labels={'instagram name': 'Instagram Name', 'Followers': 'Followers'})
        fig1.update_layout(xaxis_title="Instagram Name", yaxis_title="Number of Followers")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.scatter(instagram_df, x='Authentic engagement', y='Engagement avg',
                          size='Followers', color='Audience country(mostly)', title="Engagement by Country", height=300)
        st.plotly_chart(fig2, use_container_width=True)
    
    with st.container():
        fig = px.histogram(instagram_df, x='Followers', title="Distribution of Instagram Followers")
        st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "YouTube Data":
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
    with st.container():
        fig3 = px.histogram(filtered_data, x='Subscribers', nbins=bin_size_yt, title="Distribution of YouTube Subscribers")
        st.plotly_chart(fig3, use_container_width=True)
