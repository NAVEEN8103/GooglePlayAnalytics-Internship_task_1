import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import numpy as np

# Function to check if current time is between 5 PM and 7 PM IST
def is_time_between_5pm_7pm_ist():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    current_hour = now.hour
    return 17 <= current_hour < 19  # 17:00 to 18:59 (5 PM to 7 PM IST)

# Load dataset
try:
    df = pd.read_csv('./data/Play Store Data.csv')
except FileNotFoundError:
    print("Error: 'Play Store Data.csv' not found in './data/' directory.")
    exit()

# Data Cleaning and Preprocessing
# Clean Installs: Remove '+' and ',' and convert to integer, handle invalid entries
def clean_installs(install):
    try:
        return int(install.replace('+', '').replace(',', ''))
    except (ValueError, AttributeError):
        return None

df['Installs'] = df['Installs'].apply(clean_installs)
df = df.dropna(subset=['Installs'])

# Clean Reviews: Convert to integer, handle invalid entries
def clean_reviews(review):
    try:
        return int(review)
    except (ValueError, TypeError):
        return None

df['Reviews'] = df['Reviews'].apply(clean_reviews)
df = df.dropna(subset=['Reviews'])

# Clean Size: Convert 'M' to float, exclude 'Varies with device'
df['Size'] = df['Size'].str.replace('M', '', regex=False)
df = df[df['Size'] != 'Varies with device']
df['Size'] = pd.to_numeric(df['Size'], errors='coerce')

# Clean Rating: Ensure numeric, drop NaN
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Generate synthetic Sentiment_Subjectivity (replace with actual data if available)
np.random.seed(42)  # For reproducibility
df['Sentiment_Subjectivity'] = np.random.uniform(0, 1, len(df))

# Apply Filters
categories = ['GAME', 'BEAUTY', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'ENTERTAINMENT', 'SOCIAL', 'EVENTS']
df = df[
    (df['Rating'] > 3.5) &
    (df['Category'].isin(categories)) &
    (df['Reviews'] > 500) &
    (~df['App'].str.contains('s|S', case=False, na=False)) &
    (df['Sentiment_Subjectivity'] > 0.5) &
    (df['Installs'] > 50000)
].dropna()

# Category translations
category_translations = {
    'BEAUTY': 'सौंदर्य',  # Hindi
    'BUSINESS': 'வணிகம்',  # Tamil
    'DATING': 'Partnersuche',  # German
    'GAME': 'GAME',
    'COMICS': 'COMICS',
    'COMMUNICATION': 'COMMUNICATION',
    'ENTERTAINMENT': 'ENTERTAINMENT',
    'SOCIAL': 'SOCIAL',
    'EVENTS': 'EVENTS'
}

# Map categories to translated names
df['Category_Display'] = df['Category'].map(category_translations)

# Print filtered DataFrame for debugging
print(f"Filtered DataFrame ({len(df)} apps):")
if len(df) > 0:
    print(df[['App', 'Category', 'Category_Display', 'Rating', 'Size', 'Installs', 'Reviews', 'Sentiment_Subjectivity']])
else:
    print("Empty DataFrame")
    print("Columns: [App, Category, Category_Display, Rating, Size, Installs, Reviews, Sentiment_Subjectivity]")
    print("Index: []")

# Check if current time is between 5 PM and 7 PM IST
if is_time_between_5pm_7pm_ist():
    # Create bubble chart
    plt.figure(figsize=(12, 8))

    # Plot bubbles for each category
    for category in df['Category_Display'].unique():
        cat_data = df[df['Category_Display'] == category]
        color = 'pink' if category == 'GAME' else 'skyblue'
        plt.scatter(
            cat_data['Size'],
            cat_data['Rating'],
            s=cat_data['Installs'] / 1000,  # Scale installs for bubble size
            c=color,
            alpha=0.5,
            label=category
        )

    # Customize plot
    plt.xlabel('App Size (MB)')
    plt.ylabel('Average Rating')
    plt.title('Bubble Chart: App Size vs. Average Rating (Bubble Size = Installs)')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show plot
    plt.show()
else:
    print("Chart is only available between 5 PM and 7 PM IST.")