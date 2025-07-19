import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import numpy as np
import os

# Function to check if current time is between 5 PM and 7 PM IST
def is_time_between_5pm_7pm_ist():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    current_hour = now.hour
    return 17 <= current_hour < 19  # 17:00 to 18:59

# Load dataset
try:
    df = pd.read_csv('./data/Play Store Data.csv')
except FileNotFoundError:
    print("❌ Error: 'Play Store Data.csv' not found in './data/' directory.")
    exit()

# Clean Installs
def clean_installs(install):
    try:
        return int(install.replace('+', '').replace(',', ''))
    except (ValueError, AttributeError):
        return None

df['Installs'] = df['Installs'].apply(clean_installs)
df = df.dropna(subset=['Installs'])

# Clean Reviews
def clean_reviews(review):
    try:
        return int(review)
    except (ValueError, TypeError):
        return None

df['Reviews'] = df['Reviews'].apply(clean_reviews)
df = df.dropna(subset=['Reviews'])

# Clean Size
df['Size'] = df['Size'].str.replace('M', '', regex=False)
df = df[df['Size'] != 'Varies with device']
df['Size'] = pd.to_numeric(df['Size'], errors='coerce')

# Clean Rating
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Generate synthetic Sentiment_Subjectivity
np.random.seed(42)
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

# Translate Category Display Names
category_translations = {
    'BEAUTY': 'सौंदर्य',           # Hindi
    'BUSINESS': 'वाणिक',         # Tamil
    'DATING': 'Partnersuche',      # German
    'GAME': 'GAME',
    'COMICS': 'COMICS',
    'COMMUNICATION': 'COMMUNICATION',
    'ENTERTAINMENT': 'ENTERTAINMENT',
    'SOCIAL': 'SOCIAL',
    'EVENTS': 'EVENTS'
}

df['Category_Display'] = df['Category'].map(category_translations)

# Debug print
print(f"Filtered DataFrame ({len(df)} apps):")
if len(df) > 0:
    print(df[['App', 'Category', 'Category_Display', 'Rating', 'Size', 'Installs', 'Reviews', 'Sentiment_Subjectivity']])
else:
    print("⚠️ Empty DataFrame")

# ✅ Run chart generation
if is_time_between_5pm_7pm_ist():
    # Create output folder if not exists
    os.makedirs('web_dashboard/assets', exist_ok=True)

    # Create Bubble Chart
    plt.figure(figsize=(14, 10))

    # Define a color palette
    colors = {'GAME': 'lightcoral', 'सौंदर्य': 'skyblue', 'वाणिक': 'lightgreen', 
              'COMICS': 'plum', 'COMMUNICATION': 'lightcyan', 'Partnersuche': 'lightyellow',
              'ENTERTAINMENT': 'lightpink', 'SOCIAL': 'lightblue', 'EVENTS': 'lavender'}

    for category in df['Category_Display'].unique():
        cat_data = df[df['Category_Display'] == category]
        plt.scatter(
            cat_data['Size'],
            cat_data['Rating'],
            s=cat_data['Installs'] / 1000,
            c=colors.get(category, 'gray'),
            alpha=0.6,
            edgecolors='white',
            linewidth=0.5,
            label=category
        )

    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)

    # Labels and title
    plt.xlabel('App Size (MB)', fontsize=12)
    plt.ylabel('Average Rating', fontsize=12)
    plt.title('Bubble Chart: App Size vs. Average Rating (Bubble Size = Installs)', fontsize=14, pad=15)

    # Enhance legend visibility
    plt.legend(title='Category', bbox_to_anchor=(1.15, 1), loc='upper left', 
               fontsize=10, framealpha=1.0, edgecolor='black', facecolor='white', 
               ncol=1, title_fontsize=12, frameon=True)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save image
    plt.savefig('web_dashboard/assets/bubble_chart.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("✅ Bubble chart saved as web_dashboard/assets/bubble_chart.png")
else:
    print("🕒 Chart will generate only between 5 PM and 7 PM IST.")