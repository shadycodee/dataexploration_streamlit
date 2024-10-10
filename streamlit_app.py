import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from streamlit_option_menu import option_menu

# Title of the app
st.title('Mental Health and Technology Usage Data Exploration')

# Load the dataset
try:
    df = pd.read_csv('mental_health_and_technology_usage_2024.csv')
except FileNotFoundError:
    st.error('Dataset not found. Please upload the "mental_health_and_technology_usage_2024.csv" file.')
    st.stop()

# Navigation menu
selected = option_menu(
    menu_title=None,
    options=['Introduction', 'Dataset Overview', 'Visual Representation', 'Conclusion'],
    icons=['info-circle', 'table', 'bar-chart', 'check-circle'],
    orientation='horizontal'
)

# Introduction Section
if selected == 'Introduction':
    st.header('📖 Introduction')
    st.write(''' 
    This dataset explores the relationship between mental health and technology usage.
    It provides insights into how various factors related to technology influence mental health in individuals.
    The purpose of this exploration is to uncover patterns and trends that can help in understanding this relationship better.
    ''')
    

# Dataset Overview Section
elif selected == 'Dataset Overview':
    
    st.header('📊 Dataset Overview')
    # Add an image from your local file
    st.image('dataset.png', use_column_width=True)

    # Get a random sample of 3 rows from the DataFrame
    random_sample = df.sample(n=5)
    # Display the random sample
    st.write("Sample from Dataset:")
    st.dataframe(random_sample)
    
    st.subheader('Basic Information')

    # Capture df.info() output in a buffer and display it
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    # Display basic statistics
    st.subheader('Descriptive Statistics')
    st.write(df.describe())

    # Handle missing values
    numerical_cols = df.select_dtypes(include=['number'])
    non_numerical_cols = df.select_dtypes(exclude=['number'])
    df[numerical_cols.columns] = numerical_cols.fillna(numerical_cols.mean())
    df[non_numerical_cols.columns] = non_numerical_cols.fillna(non_numerical_cols.mode().iloc[0])

    # st.subheader('Cleaned Data')
    # st.write(df.head())
    

# Visual Representation Section
elif selected == 'Visual Representation':
    st.header('📈 Visual Representation')

    # General Distribution using Histograms
    st.subheader('General Distribution using Histograms')
    fig, ax = plt.subplots(figsize=(10, 8))
    df.hist(ax=ax)
    st.pyplot(fig)

    # Age Distribution
    st.subheader('Age Distribution')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['Age'], kde=True, color='red', ax=ax)
    ax.set_title('Age Distribution')
    ax.set_xlabel('Age')
    ax.set_ylabel('Count')
    st.pyplot(fig)

    # Mental Health Status Distribution
    st.subheader('Mental Health Status Distribution')
    fig, ax = plt.subplots(figsize=(6, 6))
    df['Mental_Health_Status'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'], startangle=90, ax=ax)
    ax.set_title('Mental Health Status Distribution')
    ax.set_ylabel('')
    st.pyplot(fig)

    # Gender Distribution
    st.subheader('Gender Distribution')
    fig, ax = plt.subplots(figsize=(6, 6))
    df['Gender'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'], startangle=90, ax=ax)
    ax.set_title('Gender Distribution')
    ax.set_ylabel('')
    st.pyplot(fig)

    # Stress Level Distribution
    st.subheader('Stress Level Distribution')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['Stress_Level'], kde=True, color='green', ax=ax)
    ax.set_title('Stress Level Distribution')
    ax.set_xlabel('Stress Level')
    ax.set_ylabel('Count')
    st.pyplot(fig)

    # Assign numerical values to stress levels
    stress_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
    df['Stress_Level_Num'] = df['Stress_Level'].map(stress_mapping)

    # Calculate the average stress level
    average_stress_level = df['Stress_Level_Num'].mean()
    st.write(f"**The average stress level is: {average_stress_level:.2f}**")

    # Technology Usage vs Mental Health Status
    st.subheader('Technology Usage Hours vs Mental Health Status')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='Mental_Health_Status', y='Technology_Usage_Hours', data=df, palette='Set2', ax=ax)
    ax.set_title('Technology Usage Hours vs Mental Health Status')
    ax.set_xlabel('Mental Health Status')
    ax.set_ylabel('Technology Usage Hours')
    st.pyplot(fig)

    # Screen Time vs Mental Health Status
    st.subheader('Screen Time Hours vs Mental Health Status')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='Screen_Time_Hours', y='Mental_Health_Status', data=df, palette='Set2', ax=ax)
    ax.set_title('Screen Time Hours vs Mental Health Status')
    ax.set_xlabel('Screen Time Hours')
    ax.set_ylabel('Mental Health Status')
    st.pyplot(fig)

    # Work Environment Impact by Mental Health Status
    st.subheader('Work Environment Impact by Mental Health Status')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x='Work_Environment_Impact', hue='Mental_Health_Status', data=df, palette='Set3', ax=ax)
    ax.set_title('Work Environment Impact by Mental Health Status')
    ax.set_xlabel('Work Environment Impact')
    ax.set_ylabel('Count')
    st.pyplot(fig)

    # Correlation Matrix and Heatmap
    st.subheader('Correlation Matrix and Heatmap')
    numerical_df = df.select_dtypes(include=['float64', 'int64'])  # Numeric columns only for correlation
    corr_matrix = numerical_df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# Conclusion Section
elif selected == 'Conclusion':
    st.header('📝 Conclusion')

    st.subheader('Summary Statistics by Mental Health Status')
    summary_stats = df.groupby('Mental_Health_Status').describe()
    st.write(summary_stats)

    # General Insights and Conclusion
    st.subheader('General Insights')

    insights = """
    - **Demographics and User Base**: The dataset comprises 10,000 users with an average age of 42 years.
    - **Technology Usage**: Users engage in 6.4 hours of technology usage daily, indicating significant reliance on digital tools.
    - **Stress Levels**: The average stress level is 2 (on a scale of 1 to 3), suggesting generally manageable stress.
    - **Sleep Patterns**: Users average 6.5 hours of sleep per night, which is slightly lower than recommended.
    - **Physical Activity**: An average of 5.0 hours of physical activity suggests users maintain a reasonable level of fitness.
    """

    st.write(insights)
    st.subheader('Final Conclusion')
    st.write(""" 
    Overall, users maintain a balanced lifestyle regarding technology usage, social media, and physical activity. However, potential areas for concern include sleep and high screen time, which might impact mental health and stress levels over time.
    """)