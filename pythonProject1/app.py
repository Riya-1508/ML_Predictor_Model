import streamlit as st
import pickle
import pandas as pd

st.title('IPL Win Predictor')

teams = ['Chennai Super Kings',
 'Delhi Capitals',
 'Gujarat Titans',
 'Kolkata Knight Riders',
 'Lucknow Super Giants',
 'Mumbai Indians',
 'Punjab Kings',
 'Rajasthan Royals',
 'Royal Challengers Bangalore',
 'Sunrisers Hyderabad']

cities = ['Ahmedabad', 'Kolkata', 'Mumbai', 'Navi Mumbai', 'Pune', 'Dubai',
       'Sharjah', 'Abu Dhabi', 'Delhi', 'Chennai', 'Hyderabad',
       'Visakhapatnam', 'Bengaluru', 'Jaipur', 'Bangalore', 'Raipur',
       'Ranchi', 'Cuttack', 'Nagpur', 'Johannesburg', 'Centurion',
       'Durban', 'Bloemfontein', 'Port Elizabeth', 'Kimberley',
       'East London', 'Cape Town']
pipe = pickle.load(open('pipe.pkl','rb'))
col1, col2 = st.columns(2)

def is_valid_input(score, overs, wickets, target):
    if score > target:
        st.error('Error: Score cannot be greater than the target!')
        return False
    elif overs > 20:
        st.error('Error: Overs completed cannot be greater than 20!')
        return False
    elif wickets > 10:
        st.error('Error: Wickets out cannot be greater than 10!')
        return False
    elif overs == 0:
        st.error('Error: Overs cannot be zero')
    return True

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))
selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.number_input('Wickets out')

if st.button('Predict Probability'):
    if is_valid_input(score, overs, wickets, target):
        runs_left = target - score
        balls_left = 120 - (overs*6)
        wickets = 10 - wickets
        crr = score/overs
        rrr = (runs_left*6)/balls_left

        input_df = pd.DataFrame({'BattingTeam':[batting_team],'BowlingTeam':[bowling_team],'City':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_run_x':[target],'crr':[crr],'rrr':[rrr]})

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header("Predicted Probabilities")
        st.markdown(f"<span style='font-size: 24px;'>{batting_team} - <span style='color: green;'>{round(win * 100)}%</span></span>",unsafe_allow_html=True)
        st.markdown(f"<span style='font-size: 24px;'>{bowling_team} - <span style='color: red;'>{round(loss * 100)}%</span></span>",unsafe_allow_html=True)