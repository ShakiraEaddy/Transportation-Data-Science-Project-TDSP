# -*- coding: utf-8 -*-
"""Explorer TDSP - Shakira Eaddy"""
"""Code and information was developed in Google Colab"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium


"""
**Accessing data using the [NYC OpenData Motor Vehicle Collisions - Crashes dataset](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95).  Each row represents a crash event. The Motor Vehicle Collisions data tables contain information from all police-reported motor vehicle collisions in NYC.**
"""

# Uploading my data by mounting my Google Drive.
from google.colab import drive
drive.mount('/content/drive')

# Reads the data using pandas read_csv function
data = pd.read_csv('/content/drive/MyDrive/Motor_Vehicle_Collisions_-_Crashes_20241007.csv')

# Prints the first 5 rows of the data using the 'head' function of pandas
data.head()

# Describes the data using the describe function of pandas
desc_stats = data.describe()
desc_stats

# Data described from table
"""
> 1. Latitude & Longitude: The latitude and longitude indicate where the crashes occur. However, there are some data points with latitude and longitude values of 0, which is likely due to missing or inaccurate data.
> 2. Number of Persons Injured: On average, each crash has around 0.305 injuries. The maximum number of injuries in a single crash is 43.
> 3. Number of Persons Killed: Fatalities are rare, with an average of 0.00146 deaths per crash. The maximum number of deaths in one crash is 8.
> 4. Number of Pedestrians, Cyclists, and Motorists Injured/Killed: These columns provide a breakdown of the injuries and fatalities by type of individual involved.
> 5. Collision ID: This is a unique identifier for each crash.
---

**Based on the resources above and outside knowledge, there are some potential bias issues related to the availability of data from well-resourced communities as compared to under-resourced communities. How might bias show up in my dataset?**
> Answer: **Bias issues related to data from well-resourced and under-resourced communities can greatly affect the accuracy and usefulness of datasets. Under-resourced communities often do not have the means to collect and report data properly, leading to a lack of representation of their needs and incidents. In contrast, well-resourced areas usually have better data collection methods, which can result in over-reporting. This creates sampling bias, where the data mainly reflects the experiences of well-resourced communities and skews the understanding of issues like safety and health. Additionally, the people gathering and analyzing data may have unconscious biases that influence which data is prioritized and how it is interpreted. This can lead to overgeneralization, where conclusions drawn from the data do not apply to under-resourced communities, furthering existing inequalities. Data quality may vary, and issues related to privacy and consent can occur, especially if individuals from under-resourced backgrounds are less aware of their rights. To reduce these biases, it is essential to encourage inclusive data collection, practice ethical methods, promote careful analysis of data, and build trust within communities. By raising awareness of these issues, we can create a more fair approach to data that accurately represents the needs of all communities, especially those that are underserved.**
"""

# Checks the dataset for missing values.

# Imports the pandas library
import pandas as pd
data = pd.read_csv('/content/drive/MyDrive/Motor_Vehicle_Collisions_-_Crashes_20241007.csv')

# Leverages the isnull() and sum() functions to find the number of missing values in each column
missing_values = pd.isnull(data).sum()

# Turns the missing value counts into percentages
missing_values_percentage = (missing_values / len(data)) * 100

# Returns counts and percentages of missing values in each column
missing_data = pd.DataFrame({'Missing Values': missing_values, 'Percentage (%)': missing_values_percentage})
missing_data.sort_values(by='Percentage (%)', ascending=False)

"""
***Here's an overview of the missing values in the dataset:***
> Columns like VEHICLE TYPE CODE 5, CONTRIBUTING FACTOR VEHICLE 5, VEHICLE TYPE CODE 4, and so on have a high percentage of missing values. This is expected since not all crashes involve multiple vehicles or factors. OFF STREET NAME and CROSS STREET NAME have significant missing values. This could be due to crashes occurring in locations where these details aren't applicable or weren't recorded. ZIP CODE, BOROUGH, and ON STREET NAME also have missing values. This might be due to incomplete data entry or crashes occurring in areas where these specifics aren't easily determinable. LOCATION, LATITUDE, and LONGITUDE have the same count of missing values, indicating that when one is missing, the others are likely missing as well.
"""

# Creates a bar chart to display the top 10 contributing factors (e.g. backing up unsafely, unsafe lane changing, etc.) to crashes within the dataset.

# Plots a Bar Chart
top_factors = data['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().head(10)
plt.figure(figsize=(12, 7))

# Plotting the top contributing factors. Filling in x as the index field of the variable 'top_factors'
sns.barplot(x=top_factors.index, y=top_factors.values, palette="magma")
plt.title('Top 10 Contributing Factors to crashes', fontsize=16)
plt.xlabel('index field', fontsize=14)
plt.ylabel('values', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""
**The top 3 contributing factors that cause the most crashes other than "Unspecified":**
> The first contributing factor that causes the most crashes are "Driver/Inattention/Distraction".
> The second contributing factor that causes the most crashes are "Failure to Yield Right-of-Way".
> The third contributing factor that causes the most crashes are "Following Too Closely".

**Recommendations I would make to new and current drivers after assessing the above data:**
> Due to the top three contributing factors that cause the most crashes, other than them being unspecified are Driver/Inattention/Distraction, Failure to Yield Right-of-Way, and Following Too Closely, I would encourage new and current drivers to not only follow traffic laws but to also pay close attention to traffic and others on the road. Be attentive towards drivers and others around them.
"""

# Creating another bar chart to determine which vehicle types were involved in the most crashes
# Determines the top vehicle types involved in crashes
top_vehicle_types = data['VEHICLE TYPE CODE 1'].value_counts().head(10)

# Plots the top vehicle types
plt.figure(figsize=(12, 7))
sns.barplot(x=top_vehicle_types.index, y=top_vehicle_types.values, palette="cividis")
plt.title('Top 10 Vehicle Types Involved in crashes', fontsize=16)
plt.xlabel('Vehicle Type', fontsize=14)
plt.ylabel('Number of crashes', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""
**The top 3 vehicles that were most involved in crashes:**
> Sedans
> Station Wagon/Sport Utility Vehicles
> Passenger Vehicles

**Why I think that "Sedan(s)," "Station Wagon(s)," and "Passenger Vehicle(s)" are involved in a larger number of crashes, injuries, and deaths when compared to the rest of the vehicles:**
> One of the reasons that "Sedan(s)," "Station Wagon(s)," and "Passenger Vehicle(s)" are involved in a larger number of crashes, injuries, and deaths when compared to the rest of the vehicles is because of how much of those specific types of vehicles there are on the roads in comparison to the other vehicles in the chart. Sedans and passenger cars are some of the most commonly driven vehicles. Because there are so many of them on the roads, they are more likely to be involved in accidents just due to more chances to interact with other vehicles.

**Reviewing the x-axis of the bar chart you created above:**
**What I noticed when reviewing the x-axis of the bar chart**
> I noticed that "Station Wagon/Sport Utility Vehicle" and "Taxi" are listed twice within the bar chart as separate categories. This causes incorrect data due to those specific vehicle types being *split*. If the two "Station Wagon/Sport Utility Vehicle" categories were together, it would be considered the number one "vehicle type crash" because the two adding up would cause a higher data value than the "Sedan" category. Also, the two "Taxi" categories need to be added together as well within their same category since they represent the same data and vehicle types.

**What I would recommend to improve the bar chart, based on the x-axis (horizontal axis)**
> I would recommend making the two "Station Wagon/Sport Utility Vehicle" categories be within the same category as well as the two "Taxi" categories be within the same category. Adding the two "Station Wagon/Sport Utility Vehicle" categories together would not only cause a higher data value, but it will also create a more accurate analysis. The same with reason regarding the "Taxi" category.

> To improve the accuracy of the dataset and ensure clear data representation, I would recommend the following:
> Consolidate Categories: Combine the "Station Wagon" and "Sport Utility Vehicle" categories into one category. This will provide a clearer picture of the total incidents involving these types of vehicles, reflecting their combined impact on crash statistics.
> Merge Taxi Categories: Similarly, merge the two "Taxi" categories into a single entry. Since they represent the same type of vehicle, combining them will lead to more accurate data and a better understanding of taxi-related crashes.
> Standardize Definitions: Ensure that there is a clear and consistent definition for each vehicle category. This helps prevent confusion and ensures that similar types of vehicles are grouped together correctly.
> Regular Audits: Conduct regular audits of the data to identify any duplicates or inconsistencies. This can help maintain the integrity of the dataset over time.
> Data Visualization: Use visual representations of the data that highlight the importance of merging these categories. Charts or graphs that show combined totals can help stakeholders understand the real impact of these vehicle types.
"""

# Graphing the *types* of crashes within this dataset and their frequencies.

import matplotlib.pyplot as plt
import seaborn as sns

# Aggregating data - Complete for Cyclist and Motorist
types_of_crashes = {
    'Pedestrian Injuries': data['NUMBER OF PEDESTRIANS INJURED'].sum(),
    'Cyclist Injuries': data['NUMBER OF CYCLIST INJURED'].sum(),
    'Motorist Injuries': data['NUMBER OF MOTORIST INJURED'].sum(),
    'Pedestrian Deaths': data['NUMBER OF PEDESTRIANS KILLED'].sum(),
    'Cyclist Deaths': data['NUMBER OF CYCLIST KILLED'].sum(),
    'Motorist Deaths': data['NUMBER OF MOTORIST KILLED'].sum()
}

# Converting to DataFrame for easier plotting
crash_types_df = pd.DataFrame(list(types_of_crashes.items()), columns=['crash Type', 'Count'])

# Ploting
plt.figure(figsize=(12, 7))
sns.barplot(x='Count', y='crash Type', data=crash_types_df, palette="mako")
plt.title('Types of crashes and Their Frequencies')
plt.xlabel('Count')
plt.ylabel('Type of crash')
plt.tight_layout()
plt.show()

"""
**After analyzing the chart above, a recommendation to the Department of Transportation based on this data:**
> To reduce the high rate of motorist injuries, the Department of Transportation could focus on enhancing road design, enforcing speed limits, and promoting safe driving practices. Improved lane markings, roundabouts, and protected turn lanes could make high-risk areas safer. Speed control measures, like increased enforcement and public awareness campaigns, would encourage safer driving, while programs addressing fatigue and distracted driving could improve focus.
"""

# Creating a chart that displays the average number of crashes per hour of the day.

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Loads the dataset
file_path = '/content/drive/MyDrive/Motor_Vehicle_Collisions_-_Crashes_20241007.csv'
data = pd.read_csv(file_path)

# Converts 'CRASH DATE' and 'CRASH TIME' to datetime
data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'])
data['CRASH TIME'] = pd.to_datetime(data['CRASH TIME'], format='%H:%M')

# Time of Day Analysis
data['Hour of Day'] = data['CRASH TIME'].dt.hour

# Groups by 'Hour of Day' and calculates the average number of crashes per hour
average_crashes_per_hour = data.groupby('Hour of Day').size() / data['Hour of Day'].nunique()

# Plots the average number of crashes
plt.figure(figsize=(12, 6))
sns.barplot(x=data['Hour of Day'], y=average_crashes_per_hour)
plt.title('Average Number of crashes per Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Average Number of crashes')
plt.xticks(range(0, 24))
plt.show()

"""
**Information from the table regarding the time of the day most crashes occur and why.**
> Most crashes happen around 8:00 p.m. for several reasons. As it gets darker, visibility decreases, making it harder for drivers to adjust from daylight to night driving. There’s also more traffic, with people heading home or going out, increasing the chance of collisions. Additionally, drivers may feel more fatigued around this time after a long day, which reduces alertness and reaction times.
"""

# Ploting a graph to determine how COVID-19 impacted the number of crashes per month, if at all.

# Converts 'CRASH DATE' to datetime format
data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'])

# Groups by month and year to get the number of crashes per month
monthly_crashes = data.groupby(data['CRASH DATE'].dt.to_period("M")).size()

# Plots the trend over time
plt.figure(figsize=(15, 7))
monthly_crashes.plot()
plt.title('Number of Crashes per Month', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Crashes', fontsize=14)
plt.tight_layout()
plt.show()

"""
** What does the graph tell me about the impact of COVID-19 on the number of crashes per month, and why do I think this occurred:**
> Between 2013 and early 2019, crash numbers showed clear seasonality each year along with noticeable cyclic patterns. Toward the end of 2019, crashes dropped significantly, reaching an all-time low in 2020 due to COVID-19. With fewer people driving during quarantines, crash rates naturally decreased. In late 2020, crashes began to rise again, resuming a seasonal trend that continued through mid-2024.
"""

# Applies time series decomposition to review trends, seasonality, and residuals.

import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

# Counts the number of crashes per day, group by CRASH DATE
daily_crashes = data.groupby(data['CRASH DATE']).size()

# Sets the plot style
sns.set(style="darkgrid")

# Plots the daily crashes time series
plt.figure(figsize=(15, 6))
plt.plot(daily_crashes, label='Daily crashes')
plt.title('Daily Motor Vehicle Collisions in NYC')
plt.xlabel('Date')
plt.ylabel('Number of Crashes')
plt.legend()
plt.show()

# Decomposes the time series
decomposition = seasonal_decompose(daily_crashes, model='additive', period=365)

# Plots the decomposed components
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
decomposition.trend.plot(ax=ax1)
ax1.set_title('Trend')
decomposition.seasonal.plot(ax=ax2)
ax2.set_title('Seasonal')
decomposition.resid.plot(ax=ax3)
ax3.set_title('Residuals')
plt.tight_layout()
plt.show()

"""
> The Time Series Plot shows the number of daily crashes over time, long-term trends, seasonal patterns, or significant outliers.

> Decomposed Components:
     > Trend: This graph shows the long-term trend in the data, which can indicate whether crashes are increasing, decreasing, or stable over time.
     > Seasonality: This reveals any regular patterns that repeat over a specific period, such as yearly. It helps identify times of the year with higher or lower crash frequencies.
     > Residuals: These are the irregular components that cannot be attributed to the trend or seasonality. They might include random or unpredictable fluctuations.

> Based on the 'trend graph', it shows a steady increase in crashes from 2014 to early 2019, followed by a gradual decline starting in 2019. Toward the end of 2019 and throughout most of 2020, crash numbers dropped sharply. From late 2020 through the end of 2021, crashes rose slightly but then began to decrease again from late 2021 through the first quarter of 2024.

> Based on the 'residual graph', there was a clear unexpected change at the start of 2014 and an even bigger change at the beginning of 2020. The change in 2014 might point to an unusual event that briefly affected crash numbers, while the change in 2020 likely connects to the start of COVID-19. Due to quarantines and fewer cars on the road, crash numbers dropped more than expected, causing these differences from the trend.
"""

# Builds a bar chart to compare and analyze the number of crashes across the five boroughs: Brooklyn (also known as Kings County), Queens, Manhattan, Bronx, and Staten Island.
# Plots a bar chart to compare the number of crashes that occurred in each of the five boroughs.

# Sets style
sns.set_style("whitegrid")

# Plots the distribution of crashes by borough
plt.figure(figsize=(12, 7))

# Finds the count of unique values of BOROUGHS.
borough_count = data['BOROUGH'].value_counts()
sns.barplot(x=borough_count.index, y=borough_count.values, palette="viridis")
plt.title('Distribution of Crashes by Borough', fontsize=16)
plt.xlabel('Borough', fontsize=14)
plt.ylabel('Number of Crashes', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""
> Based on the chart, Brooklyn has the highest number of crashes, and Staten Island has the lowest number of crashes. 

> Reasons as to why certain boroughs can have a higher or lower number of crashes can be due to factors such as population. For example, if there is a higher population in Brooklyn than in Staten Island, then the number of crashes can play a big role in why there are more crashes in Brooklyn than in Staten Island.
"""

# Creates a heatmap to determine the most dangerous intersections in the dataset.

# Creates a heatmap leveraging the latitude and longitude variables to determine where the most crashes are occurring
from folium.plugins import HeatMap

# Drops rows with missing latitude and longitude values
data_geo = data.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Creates a base map
m = folium.Map(location=[40.730610, -73.935242], zoom_start=10)  # Centered around NYC

# Creates a heatmap
heat_data = [[row['LATITUDE'], row['LONGITUDE']] for index, row in data_geo.iterrows()]
HeatMap(heat_data, radius=8, max_zoom=13).add_to(m)
m.save("Heatmap.html")

"""
> After looking at my created heatmap, I noticed a concentration of crashes in the areas of intersections.
"""

# Creating severity mapping to plot crashes on the map and code them based on severity, distinguishing between crashes that resulted in injuries and those that led to fatalities.

# Sample a subset of the data for visualization
sample_data_severity = data_geo.sample(n=1000, random_state=42)

# Creates a base map
m_severity = folium.Map(location=[40.730610, -73.935242], zoom_start=10)

# Adds crashes to the map with color coding and shape coding based on severity
for index, row in sample_data_severity.iterrows():
    if row['NUMBER OF PERSONS KILLED'] > 0:
        color = "Red"  # Fatalities

        folium.features.RegularPolygonMarker(
          location=[row['LATITUDE'], row['LONGITUDE']],
          number_of_sides=3,
          radius=5,
          gradient = False,
          color=color,
          fill=True,
          fill_color=color
        ).add_to(m_severity)


    elif row['NUMBER OF PERSONS INJURED'] > 0:
        color = "Yellow"  # Injuries
        folium.CircleMarker(
          location=[row['LATITUDE'], row['LONGITUDE']],
          radius=5,
          color=color,
          fill=True,
          fill_color=color
       ).add_to(m_severity)
    else:
        color = "Green"  # No injuries or fatalities
        folium.features.RegularPolygonMarker(
          location=[row['LATITUDE'], row['LONGITUDE']],
          number_of_sides=4,
          radius=5,
          gradient = False,
          color=color,
          fill=True,
          fill_color=color
        ).add_to(m_severity)


m_severity.save("severity.html")

"""
> After looking at the severity map, the intersections that seem to be the most dangerous are FDR Drive under East 25th Street Pedestrian Bridge, West 90th Street connects with West End Avenue, and where 103rd Avenue connects with 99th Street.
"""

"""
**Research question:***
> Research Question: At what times of day are crashes, injuries, and fatalities most likely to occur in New York City, and what trends can be observed across different boroughs?
> Reason: This research question was chosen to help identify specific time periods with higher crash rates, injuries, and fatalities, which can provide valuable insights for targeted safety interventions. Understanding when crashes are most likely to occur allows transportation departments to provide resources more effectively, such as scheduling enforcement during peak risk hours or adjusting traffic management strategies to reduce accidents. Additionally, identifying these high-risk times can aid in public awareness campaigns, helping to promote safer driving behaviors at critical times, and contributing to improved road safety. This question also emphasizes identifying peak times for crashes and associated injuries or fatalities, while allowing for an analysis of patterns across various times of day.
"""

# Builds a visualization, a model, and other statistical methods to gain insights into my data and to support my research question.

#Creating a chart that displays the average number of crashes per hour of the day.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Loads the dataset
file_path = '/content/drive/MyDrive/Motor_Vehicle_Collisions_-_Crashes_20241007.csv'
data = pd.read_csv(file_path)

# Converts 'CRASH DATE' and 'CRASH TIME' to datetime
data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'])
data['CRASH TIME'] = pd.to_datetime(data['CRASH TIME'], format='%H:%M')

# Time of Day Analysis
data['Hour of Day'] = data['CRASH TIME'].dt.hour

# Groups by 'Hour of Day' and calculates the average number of crashes per hour
average_crashes_per_hour = data.groupby('Hour of Day').size() / data['Hour of Day'].nunique()

# Plots the average number of crashes
plt.figure(figsize=(12, 6))
sns.barplot(x=data['Hour of Day'], y=average_crashes_per_hour)
plt.title('Average Number of crashes per Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Average Number of crashes')
plt.xticks(range(0, 24))
plt.show()


# Bar chart to compare and analyze the number of crashes across the five boroughs: Brooklyn (also known as Kings County), Queens, Manhattan, Bronx, and Staten Island.
# Plots a bar chart to compare the number of crashes that occurred in each of the five boroughs.

# Sets style
sns.set_style("whitegrid")

# Plots the distribution of crashes by borough
plt.figure(figsize=(12, 7))

# Finds the count of unique values of BOROUGHS. Hint: Use value_count function.
borough_count = data['BOROUGH'].value_counts()
sns.barplot(x=borough_count.index, y=borough_count.values, palette="viridis")
plt.title('Distribution of Crashes by Borough', fontsize=16)
plt.xlabel('Borough', fontsize=14)
plt.ylabel('Number of Crashes', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Heatmap
# Samples a subset of the data for visualization
sample_data_severity = data_geo.sample(n=1000, random_state=42)

# Creats a base map
m_severity = folium.Map(location=[40.730610, -73.935242], zoom_start=10)

# Adds crashes to the map with color coding and shape coding based on severity
for index, row in sample_data_severity.iterrows():
    if row['NUMBER OF PERSONS KILLED'] > 0:
        color = "Red"  # Fatalities

        folium.features.RegularPolygonMarker(
          location=[row['LATITUDE'], row['LONGITUDE']],
          number_of_sides=3,
          radius=5,
          gradient = False,
          color=color,
          fill=True,
          fill_color=color
        ).add_to(m_severity)


    elif row['NUMBER OF PERSONS INJURED'] > 0:
        color = "Yellow"  # Injuries
        folium.CircleMarker(
          location=[row['LATITUDE'], row['LONGITUDE']],
          radius=5,
          color=color,
          fill=True,
          fill_color=color
       ).add_to(m_severity)
    else:
        color = "Green"  # No injuries or fatalities
        folium.features.RegularPolygonMarker(
          location=[row['LATITUDE'], row['LONGITUDE']],
          number_of_sides=4,
          radius=5,
          gradient = False,
          color=color,
          fill=True,
          fill_color=color
        ).add_to(m_severity)


m_severity.save("severity.html")


#Creates a heatmap leveraging the latitude and longitude variables to determine where the most crashes are occurring
from folium.plugins import HeatMap

# Drops rows with missing latitude and longitude values
data_geo = data.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Creates a base map
m = folium.Map(location=[40.730610, -73.935242], zoom_start=10)  # Centered around NYC

# Creates a heatmap
heat_data = [[row['LATITUDE'], row['LONGITUDE']] for index, row in data_geo.iterrows()]
HeatMap(heat_data, radius=8, max_zoom=13).add_to(m)

m.save("Heatmap.html")



"""
My one-page virtual poster board to portray my research findings and recommendations: 
> https://drive.google.com/file/d/1OcTrx8CUxz9Ar8dD_LDsHNNyizILoheK/view?usp=sharing 
"""
