import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Social Media Influencer Analysis", layout="wide")

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

def format_sidebar_options(option):
    if option == "YouTube Data":
        return "🎥 " + option
    elif option == "Instagram Data":
        return "📷 " + option
    elif option == "Comparison":
        return "📊 " + option

def generate_wordcloud(data):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(data)
    plt.figure(figsize=(10, 5))
    plt.title('Word Cloud', fontsize=20, pad=50, fontweight='bold') 
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

instagram_df = load_data("instagram.csv")
youtube_df = load_data("youtube.csv")
predictd_insta=load_data("df_predicted_insta.csv")
predictd_youtube=load_data("df_predicted_youtube.csv")
country_youtube=load_data("country_youtube.csv")
country_insta=load_data("country_insta.csv")

quantiles = instagram_df['Followers'].quantile([0.25, 0.5, 0.75])
low, medium, high = quantiles[0.25], quantiles[0.5], quantiles[0.75]
very_high = instagram_df['Followers'].max()

selected_tab = st.sidebar.radio(
    "Choose a tab",
    ["YouTube Data", "Instagram Data", "Comparison"],
    format_func=format_sidebar_options
)


if selected_tab == "YouTube Data":
    col1, col2 = st.columns([2, 3])
    
    with col1:
        top_youtubers = youtube_df.nlargest(10, 'Subscribers')
        fig4 = px.pie(top_youtubers, names='youtuber name', values='Subscribers', title="Top 10 YouTubers by Subscriber Count", height=350)
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        country_subscriber_totals = youtube_df.groupby('Audience Country').agg({'Subscribers': 'sum'}).reset_index()
        top_10_countries = country_subscriber_totals.nlargest(10, 'Subscribers')['Audience Country']
        filtered_data = youtube_df[youtube_df['Audience Country'].isin(top_10_countries)]
        
        aggregated_data = filtered_data.groupby(['Category', 'Audience Country']).agg({'Subscribers': 'sum'}).reset_index()
        fig5 = px.density_heatmap(
            aggregated_data, x='Audience Country', y='Category', z='Subscribers', 
            color_continuous_scale='Viridis', title="Subscribers Heatmap ",
            range_color=[0, 1e9], height=300
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with st.container():
        col_a, col_b = st.columns([3, 1])
        with col_a:
            fig3 = px.histogram(filtered_data, x='Subscribers', title="Distribution of YouTube Subscribers", height=300, range_x=[0, 50000000])
            st.plotly_chart(fig3, use_container_width=True)
        
        with col_b:
        
            upper_limit = 50000000
            
            quantiles = youtube_df['Subscribers'].clip(upper=upper_limit).quantile([0.25, 0.5, 0.75])
            low, medium, high = quantiles[0.25], quantiles[0.5], quantiles[0.75]
            very_high = upper_limit 
            
            mean_subscribers = youtube_df['Subscribers'].mean()
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=mean_subscribers,
                title={'text': "Average Subscribers"},
                gauge={
                    'axis': {'range': [None, very_high]},
                    'bar': {'color': "lightgrey"},
                    'steps': [
                        {'range': [0, low], 'color': "lightblue"},  
                        {'range': [low, medium], 'color': "deepskyblue"}, 
                        {'range': [medium, high], 'color': "dodgerblue"},
                        {'range': [high, very_high], 'color': "darkblue"}
                    ],
                    'threshold': {
                        'line': {'color': "navy", 'width': 4},
                        'thickness': 0.75,
                        'value': mean_subscribers
                    }
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)

elif selected_tab == "Instagram Data":
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
    
    st.container()
    col_a, col_b = st.columns([3, 1])
    with col_a:
        fig = px.histogram(instagram_df, x='Followers', title="Distribution of Instagram Followers", height=300, range_x=[0, 50000000])
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        upper_limit = 50000000
        quantiles = instagram_df['Followers'].clip(upper=upper_limit).quantile([0.25, 0.5, 0.75])
        low, medium, high = quantiles[0.25], quantiles[0.5], quantiles[0.75]
        very_high = upper_limit
        
        mean_followers = instagram_df['Followers'].mean()
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=mean_followers,
            number={'suffix': " followers"},
            delta={'reference': mean_followers},
            title={'text': "Average Followers"},
            gauge={
                'axis': {'range': [None, very_high]},
                'bar': {'color': "lightgray"},
                'steps': [
                    {'range': [0, low], 'color': "lightblue"},  
                    {'range': [low, medium], 'color': "deepskyblue"}, 
                    {'range': [medium, high], 'color': "dodgerblue"},
                    {'range': [high, very_high], 'color': "darkblue"}  
                ],
                'threshold': {
                    'line': {'color': "navy", 'width': 1},
                    'thickness': 0.75,
                    'value': mean_followers
                }
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
elif selected_tab == "Comparison":
    col1, col2 = st.columns(2)

    with col1:
        total_instagram_followers = instagram_df['Followers'].sum()
        total_youtube_subscribers = youtube_df['Subscribers'].sum()
        comparison_data = {
            'Platform': ['Instagram', 'YouTube'],
            'Count': [total_instagram_followers, total_youtube_subscribers]
        }
        comparison_df = pd.DataFrame(comparison_data)
        fig6 = px.bar(comparison_df, x='Platform', y='Count', title="Total Followers/Subscribers Comparison", height=300)
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        instagram_data = {
            "Actual (Log)": predictd_insta['Actual Followers (Log)'],
            "Predicted (Log)": predictd_insta['Predicted Followers (Log)'],
            "Platform": "Instagram"
        }
        youtube_data = {
            "Actual (Log)": predictd_youtube['Actual Subscriber (Log)'],
            "Predicted (Log)": predictd_youtube['Predicted Subscriber (Log)'],
            "Platform": "YouTube"
        }
        
        df_instagram = pd.DataFrame(instagram_data)
        df_youtube = pd.DataFrame(youtube_data)
        df_combined = pd.concat([df_instagram, df_youtube], axis=0)
        
        fig = px.scatter(df_combined, x='Actual (Log)', y='Predicted (Log)',
                         color='Platform', labels={'Actual (Log)': 'Actual (Log)', 'Predicted (Log)': 'Predicted (Log)'},
                         title='Actual vs Predicted Followers/Subscribers (Log)',
                         hover_data={'Actual (Log)': True, 'Predicted (Log)': True},
                         template='plotly_white', height=300)

        fig.add_shape(
            type='line', 
            line=dict(dash='dash', color='green'),
            x0=df_combined['Actual (Log)'].min(), y0=df_combined['Actual (Log)'].min(),
            x1=df_combined['Actual (Log)'].max(), y1=df_combined['Actual (Log)'].max()
        )

        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        
        trace1 = go.Scattergeo(
            lat=country_insta['Latitude'],
            lon=country_insta['Longitude'],
            text=country_insta['Country'] + ": " + country_insta['Number'].astype(str),
            marker=dict(
                size=country_insta['Number']*2 ,  
                color='blue',
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area'
            ),
            name='Instagram Followers'
        )

        trace2 = go.Scattergeo(
            lat=country_youtube['Latitude'],
            lon=country_youtube['Longitude'],
            text=country_youtube['Country'] + ": " + country_youtube['Numbers'].astype(str),
            marker=dict(
                size=country_youtube['Numbers']*2 , 
                color='red',
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area'
            ),
            name='YouTube Subscribers'
        )

        fig = make_subplots(specs=[[{"type": "scattergeo"}]])
        fig.add_trace(trace1)
        fig.add_trace(trace2)

        fig.update_layout(
            title_text='Global Distribution of Instagram Followers and YouTube Subscribers',
            showlegend=True,
            geo=dict(
                showland=True,
                landcolor='rgb(217, 217, 217)'
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    