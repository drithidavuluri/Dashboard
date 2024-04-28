# Social Media Analysis

This is a Streamlit app that provides an interactive dashboard for analyzing social media influencers' data from Instagram and YouTube. The app allows users to explore and visualize various metrics related to followers, engagement, and other relevant statistics. It also includes machine learning models to predict follower/subscriber counts based on engagement metrics.

## Features

- YouTube Data: Visualize top YouTubers by subscriber count, distribution of subscribers, and a heatmap of subscribers across categories and countries.
- Instagram Data: Explore a word cloud of influencers' names sized by their follower count, engagement metrics by country, and the distribution of followers.
- Comparison: Compare the total follower/subscriber count between Instagram and YouTube, visualize actual vs. predicted follower/subscriber values using machine learning models, and view a global distribution map of followers/subscribers.

## Installation

1. Clone the repository: https://github.com/drithidavuluri/Dashboard
2. Install the required dependencies: pip install -r requirements.txt

## Usage

1. Run the Streamlit app: streamlit run app.py
2. The app will open in your default web browser. If not, you can access it by clicking the URL provided in the terminal output.
3. Use the sidebar to navigate between the different tabs: "YouTube Data", "Instagram Data", and "Comparison".
4. Explore the various visualizations and interact with the plots by hovering over data points or zooming in/out.

## Data

The app uses the following data files:

- `instagram.csv`: Contains Instagram influencer data, including followers, engagement metrics, and audience countries.
- `youtube.csv`: Contains YouTube influencer data, including subscribers, average views, likes, comments, and audience countries.
- `df_predicted_insta.csv`: Contains predicted follower counts for Instagram influencers based on a machine learning model.
- `df_predicted_youtube.csv`: Contains predicted subscriber counts for YouTube influencers based on a machine learning model.
- `country_youtube.csv`: Contains the number of YouTubers and their geographic coordinates for each country.
- `country_insta.csv`: Contains the number of Instagram influencers and their geographic coordinates for each country.

## Machine Learning Models

The project includes two machine learning models implemented using scikit-learn's Random Forest Regressor:

1. Instagram Follower Prediction: This model takes the "Authentic engagement" and "Engagement avg" features to predict the number of followers for Instagram influencers.
2. YouTube Subscriber Prediction: This model uses the "avg views", "avg likes", and "avg comments" features to predict the number of subscribers for YouTube influencers.

The models are trained and optimized using Grid Search Cross-Validation, and the best model parameters are selected based on the R-squared metric.

## Code Files

- `datapreprocessing.ipynb`: This script handles data preprocessing,including handling missing data, and saving processed dataframes.
- `app.py`: This is the main Streamlit application file that creates the interactive dashboard, loads data, and renders visualizations.

## Acknowledgments

- The app was deployed using [Streamlit](https://streamlit.io/), a Python library for building interactive data apps.
- Visualizations were created with [Plotly](https://plotly.com/python/) and [Matplotlib](https://matplotlib.org/).
- Machine learning models were implemented using [scikit-learn](https://scikit-learn.org/).

### Github repo link - https://github.com/drithidavuluri/Dashboard

### Link to deployed web page - https://dashboard-9g6sbpmafzempgwtu7fqcj.streamlit.app/
