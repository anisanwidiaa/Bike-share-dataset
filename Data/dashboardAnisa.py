import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# load dataset
bike_sharing = pd.read_csv("https://raw.githubusercontent.com/anisanwidiaa/Bike-share-dataset/main/Data/bike_sharing.csv")
bike_sharing['dateday'] = pd.to_datetime(bike_sharing['dateday'])

# set title
st.set_page_config(page_title="Dashboard of Bike-Sharing",
                   page_icon="🕸️",
                   layout="wide")

#weather total
def create_weather_total(bike_sharing):
    weather_total = bike_sharing.groupby("weather_daily").agg({
        "total_count_hourly": "sum"
    })
    weather_total= weather_total.reset_index()
    weather_total.rename(columns={
        "total_count_hourly": "total_rides",
    }, inplace=True)

    weather_total['weather_daily'] = pd.Categorical(weather_total['weather_daily'],
                                             categories=['Misty', 'Clear', 'Light_RainSnow'])  
    weather_total = weather_total.sort_values('weather_daily')

    return weather_total



#weather data
def create_weather_data(bike_sharing):
    weather_data = bike_sharing.groupby("weather_daily").agg({
        "nonmember_hourly": "sum",
        "member_hourly": "sum",
        "total_count_hourly": "sum"
    })
    weather_data = weather_data.reset_index()
    weather_data.rename(columns={
        "nonmember_hourly": "nonmember_rides",
        "member_hourly": "member_rides",
        "total_count_hourly": "total_rides"
    }, inplace=True)
    
    weather_data = pd.melt(weather_data,
                                      id_vars=['weather_daily'],
                                      value_vars=['nonmember_rides', 'member_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')

    weather_data = weather_data.sort_values('weather_daily')
    
    return weather_data

# season total
def create_season_total(bike_sharing):
    season_total = bike_sharing.groupby("season_daily").agg({
        "total_count_hourly": "sum"
    })
    season_total = season_total.reset_index()
    season_total.rename(columns={
        "total_count_hourly": "total_rides",
    }, inplace=True)

    season_total['season_daily'] = pd.Categorical(season_total['season_daily'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])  
    season_total = season_total.sort_values('season_daily')

    return season_total

# seasonly data
def create_season_data(bike_sharing):
    season_data = bike_sharing.groupby("season_daily").agg({
        "nonmember_hourly": "sum",
        "member_hourly": "sum",
        "total_count_hourly": "sum"
    })
    season_data = season_data.reset_index()
    season_data.rename(columns={
        "nonmember_hourly": "nonmember_rides",
        "member_hourly": "member_rides",
        "total_count_hourly": "total_rides"
    }, inplace=True)
    
    season_data = pd.melt(season_data,
                                      id_vars=['season_daily'],
                                      value_vars=['nonmember_rides', 'member_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')

    season_data = season_data.sort_values('season_daily')
    
    return season_data

#MONTH DATA
def create_month_data(bike_sharing):
    month_data = bike_sharing.resample(rule='M', on='dateday').agg({
        "nonmember_hourly": "sum",
        "member_hourly": "sum",
        "total_count_hourly": "sum"
    })
    month_data.index = month_data.index.strftime('%b-%y')
    month_data = month_data.reset_index()
    month_data.rename(columns={
        "dateday": "date_day",
        "total_count_hourly": "total_rides",
        "nonmember_hourly": "nonmember_rides",
        "member_hourly": "member_rides"
    }, inplace=True)

    month_data['month_daily'] = month_data['date_day'].str.split('-').str[0]

    # Melting DataFrame
    month_data = pd.melt(month_data,
                           id_vars=['month_daily'],  # Mengubah ini sesuai dengan nama kolom yang diinginkan
                           value_vars=['nonmember_rides', 'member_rides'],
                           var_name='type_of_rides',
                           value_name='count_rides')
    
    return month_data
# hour data
def create_hour_data(bike_sharing):
    hour_data = bike_sharing.groupby(["weekday_hourly", "hour"]).agg({
        "total_count_hourly": "sum"
    }).reset_index()

    

    return hour_data
# week data
def create_weekday_data(bike_sharing):
    weekday_data = bike_sharing.groupby("weekday_daily").agg({
        "nonmember_hourly": "sum",
        "member_hourly": "sum",
        "total_count_hourly": "sum"
    }).reset_index()

    weekday_data.rename(columns={
        "nonmember_hourly": "nonmember_rides",
        "member_hourly": "member_rides",
        "total_count_hourly": "total_rides"
    }, inplace=True)

    weekday_data = pd.melt(weekday_data,
                           id_vars=['weekday_daily'],
                           value_vars=['nonmember_rides', 'member_rides'],
                           var_name='type_of_rides',
                           value_name='count_rides')

    # Konversi 'weekday_daily' menjadi kategori dengan urutan yang benar
    weekday_data['weekday_daily'] = pd.Categorical(weekday_data['weekday_daily'],
                                                   categories=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

    weekday_data = weekday_data.sort_values('weekday_daily')

    return weekday_data
# weekday data

# filter date

min_date = bike_sharing["dateday"].min()
max_date = bike_sharing["dateday"].max()

# sidebar
with st.sidebar:
    # add capital bikeshare logo
    st.image("https://raw.githubusercontent.com/anisanwidiaa/Bike-share-dataset/main/image/CapitalBikeshare_Logo.png")
    st.sidebar.header("Sort by:")

    # get start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label="Date ", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.sidebar.header("Explore my LinkedIn:")
st.sidebar.markdown("Anisa Nurwidiastuti")
st.sidebar.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/anisanwidiaa//)")
# sidebar

# connect filter & main_df

main_df = bike_sharing[
    (bike_sharing["dateday"] >= str(start_date)) &
    (bike_sharing["dateday"] <= str(end_date))
]

weather_total = create_weather_total(main_df)
hour_data = create_hour_data(main_df)
weather_data = create_weather_data(main_df)
season_total = create_season_total(main_df)
month_data = create_month_data(main_df)
season_data = create_season_data(main_df)
weekday_data = create_weekday_data(main_df)

# mainpage
st.title("Dashboard of Bike-Sharing:Capital Bikeshare :📈")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['total_count_hourly'].sum() / 1000
    st.metric("Rides's Total", value=f"{total_all_rides:.2f} K")
with col2:
    total_nonmember_hourly_rides = main_df['nonmember_hourly'].sum() /1000
    st.metric("Non Member Rides's Total", value=f"{total_nonmember_hourly_rides:.2f} K")
with col3:
    total_member_hourly_rides = main_df['member_hourly'].sum() /1000
    st.metric("Member Rides's Total", value=f"{total_member_hourly_rides:.2f} K")

st.markdown("---")
# mainpage


# CHART1
fig = px.bar(month_data,
              x='month_daily',
              y='count_rides',
              color='type_of_rides',
              barmode='group',
              color_discrete_sequence=["pink", "blue"],
              title='Accumulated calculation by month for bikeshare').update_layout(xaxis_title='Month', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

# CHART2 
fig1 = px.box(weather_data,
              x='type_of_rides',  
              y='count_rides',
              color_discrete_sequence=["red", "green"],
              title='Total bikeshare rides categorized by customer category',
              labels={'type_of_rides': 'Type of subscription', 'count_rides': 'Total Rides'})

fig2 = px.bar(weather_total,
              x='weather_daily',
              y='total_rides',
              color_discrete_sequence=["orange"],
              title='Total bikeshare rides based on weather conditions').update_layout(xaxis_title='Weather', yaxis_title='Total Rides')
fig1.update_layout(showlegend=True, legend=dict(title='Customer Category'))

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

# CHART 3
fig3 = px.line(hour_data,
              x='hour',
              y='total_count_hourly',
              color='weekday_hourly',
              color_discrete_sequence=["skyblue", "orange", "red"],
              markers=True,
              title="Bikeshare Rides in Weekday of Counts").update_layout(xaxis_title='Hour', yaxis_title='Total Rides')

st.plotly_chart(fig3, use_container_width=True)

# CHART4

st.caption('Copyright ©, created by Anisa Nurwidiastuti')