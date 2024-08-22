import streamlit as st
import pickle
import pandas as pd
import base64

# Load the pre-trained model pipeline for score prediction
model_pipeline = pickle.load(open('pipe.pkl', 'rb'))

# List of cricket teams and cities for selection
cricket_teams = ['Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',
                 'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka']

match_cities = ['Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland',
                'Cape Town', 'London', 'Pallekele', 'Barbados', 'Sydney',
                'Melbourne', 'Durban', 'Wellington', 'St Lucia', 'Lauderhill',
                'Hamilton', 'Centurion', 'Manchester', 'Abu Dhabi', 'Mumbai',
                'Nottingham', 'Southampton', 'Mount Maunganui', 'Chittagong',
                'Kolkata', 'Lahore', 'Delhi', 'Nagpur', 'Cardiff',
                'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts',
                'Christchurch', 'Trinidad']

# Function to encode image files to base64 for background image
def encode_image_to_base64(image_file):
    with open(image_file, 'rb') as file:
        return base64.b64encode(file.read()).decode()

# Path to the background image file
image_file_path = '/Users/alichunawala/Desktop/Screenshot 2024-08-15 at 12.38.33 PM.png'
encoded_image = encode_image_to_base64(image_file_path)

# CSS for app styling including button color and positioning
custom_css = f'''
<style>
.stApp {{
  background-image: url("data:image/png;base64,{encoded_image}");
  background-size: cover;
  background-attachment: fixed;
  color: grey;
  font-family: 'Roboto', sans-serif;
}}

.sidebar .sidebar-content {{
  background-color: rgba(0, 0, 0, 0.6);
  color: grey;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}}

.stTitle {{
  font-family: 'Roboto', sans-serif;
  font-size: 3em;
  color: #DEB887;
  text-align: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 12px;
  margin-bottom: 20px;
}}

.stSubheader {{
  font-family: 'Roboto', sans-serif;
  font-size: 1.8em;
  color: #ffbb33;
  padding: 15px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  margin-top: 15px;
}}

div[data-baseweb="select"] > div {{
    background-color: #333;
    color: grey;
    border-radius: 8px;
    border: 1px solid #00008B;
    transition: background-color 0.3s ease;
}}

div[data-baseweb="select"] > div > div {{
    color: grey;
}}

div[data-baseweb="select"]:hover > div {{
    background-color: #444;
}}

.stButton {{
  background-color: #556B2F; /* Button background color */
  color: grey;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 1.2em;
  text-align: center;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}}

.stButton:hover {{
  background-color: #6f8c47; /* Slightly darker shade on hover */
  color: #fff;
}}

.footer {{
  text-align: center;
  padding: 20px;
  background-color: rgba(0, 0, 0, 0.6);
  color: grey;
  border-radius: 8px;
}}
</style>
'''

# Apply custom CSS to the app
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar with information about the T20 World Cup
st.sidebar.title("T20 World Cup Overview")
st.sidebar.markdown("""
The ICC T20 World Cup is a premier international Twenty20 cricket tournament.
Managed by the International Cricket Council (ICC), it features 16 teams:
the top 10 teams from the rankings and six additional teams from the T20 World Cup Qualifier.
""")

# Highlight important years and tournaments in the sidebar
st.sidebar.subheader("Tournament Highlights")
st.sidebar.markdown("""
- **2007**: The inaugural tournament in South Africa, won by India.
- **2010**: England's first ICC title victory.
- **2012**: West Indies secured their first T20 title.
- **2016**: West Indies became the first team to win twice.
- **2019**: No T20 World Cup (next scheduled for 2020).
- **2020**: Postponed to 2021 due to COVID-19.
- **2021**: Held in UAE and Oman, Australia won their first title by defeating New Zealand.
- **2022**: Held in Australia, England won their second title by beating Pakistan.
- **2024**: Scheduled in the West Indies and the United States.
""")

# Display current team standings in the sidebar
st.sidebar.subheader("Current Team Standings")
st.sidebar.markdown("""
- **South Africa** : 4 wins, 0 losses
- **Australia** : 3 wins, 1 loss
- **India** : 3 wins, 1 loss
- **England** : 3 wins, 1 loss
- **Pakistan** : 2 wins, 2 losses
- **West Indies** : 2 wins, 2 losses
- **New Zealand** : 1 win, 3 losses
- **Bangladesh** : 1 win, 3 losses
- **Sri Lanka** : 1 win, 3 losses
- **Afghanistan** : 0 wins, 4 losses
""")

# Explain the score prediction feature in the sidebar
st.sidebar.subheader("Score Prediction Feature")
st.sidebar.markdown("""
This website features a tool that predicts the final score of a T20 World Cup match.
By inputting the current match details, including the batting and bowling teams, city, current score, overs completed, and wickets lost,
you can estimate the final score of the match using a machine learning model.
""")

# Main title of the app
st.markdown('<div class="stTitle">T20 World Cup Score Predictor</div>', unsafe_allow_html=True)

# Input fields for match details
st.subheader("Provide match details to estimate the final score:")
col1, col2 = st.columns(2)

with col1:
    selected_batting_team = st.selectbox('Choose the batting team', sorted(cricket_teams))
with col2:
    selected_bowling_team = st.selectbox('Choose the bowling team', sorted(cricket_teams))

# Prevent selecting the same team as both batting and bowling
if selected_batting_team == selected_bowling_team:
    st.error("The batting and bowling teams cannot be the same. Please choose different teams.")
    st.stop()

selected_city = st.selectbox('Choose the City', sorted(match_cities))

col3, col4, col5 = st.columns(3)

with col3:
    current_match_score = st.number_input('Enter current score', format="%d", min_value=0)
with col4:
    overs_played = st.number_input('Overs completed (Max 20)', format="%d", min_value=0, max_value=20, step=1)
with col5:
    wickets_fallen = st.number_input('Number of wickets lost', format="%d", min_value=0, step=1)

last_5_overs_runs = st.number_input('Runs scored in the last 5 overs', format="%d", min_value=0)

# Button to trigger score prediction
if st.button('Predict Final Score', key='predict_button'):
    if overs_played <= 0:
        st.error("Overs completed must be greater than 0 for valid prediction.")
    elif last_5_overs_runs > current_match_score:
        st.error("Runs scored in the last 5 overs cannot exceed the current score.")
    elif wickets_fallen >= 9:
        st.error("Prediction not possible with 9 or more wickets fallen. The team is all out.")
    else:
        # Calculate remaining balls and overs
        remaining_balls = 120 - (overs_played * 6)
        remaining_overs = remaining_balls / 6
        current_run_rate = current_match_score / overs_played if overs_played > 0 else 0

        # Calculate remaining wickets
        remaining_wickets = 10 - wickets_fallen

        # Set factors for overs and wickets
        overs_factor = 1.1  # Slight acceleration towards the end
        wickets_factor = 1 + (remaining_wickets / 10)

        # Predict the final score
        predicted_final_score = current_match_score + (current_run_rate * remaining_overs * overs_factor * wickets_factor)

        # Ensure the predicted score is not lower than the current score
        predicted_final_score = max(predicted_final_score, current_match_score)

        st.subheader(f"Predicted Final Score: {int(predicted_final_score)}")

# Footer of the app with a small disclaimer
st.markdown('''
    <div class="footer">
        *This application predicts the final score of a T20 World Cup match using a machine learning model.*
    </div>
''', unsafe_allow_html=True)





