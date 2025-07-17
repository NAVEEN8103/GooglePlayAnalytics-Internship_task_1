# File: internship_tasks/task1_wordcloud.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
import re

# Download NLTK stopwords
nltk.download('stopwords')

# Load datasets directly
apps_df = pd.read_csv(r'C:\Users\navee\Desktop\INTERNSHIP\GooglePlayAnalytics-Internship\data\Play Store Data.csv')
reviews_df = pd.read_csv(r'C:\Users\navee\Desktop\INTERNSHIP\GooglePlayAnalytics-Internship\data\User Reviews.csv')

# Convert ratings to numeric
apps_df['Rating'] = pd.to_numeric(apps_df['Rating'], errors='coerce')

# Filter Health & Fitness apps with 5-star ratings
hf_apps = apps_df[(apps_df['Category'] == 'HEALTH_AND_FITNESS') & (apps_df['Rating'] == 5.0)]
hf_app_names = hf_apps['App'].dropna().unique()

# Filter positive reviews for these apps
filtered_reviews = reviews_df[
    (reviews_df['App'].isin(hf_app_names)) &
    (reviews_df['Sentiment'] == 'Positive') &
    (~reviews_df['Translated_Review'].isna())
]

# Define stopwords and app name words
stop_words = set(stopwords.words('english'))
app_name_words = set(word.lower() for app in hf_app_names for word in str(app).split())

# Clean text function
def clean_text(text):
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    return [word for word in words if word not in stop_words and word not in app_name_words]

# Extract all cleaned words
all_words = []
for review in filtered_reviews['Translated_Review']:
    cleaned = clean_text(review)
    all_words.extend(cleaned)

# Check if there are any words to plot
if not all_words:
    print("No words found after filtering! Please check your filters and input data.")
else:
    text_for_wc = ' '.join(all_words)

    # Generate Word Cloud
    wordcloud = WordCloud(width=1000, height=500, background_color='white', colormap='viridis').generate(text_for_wc)

    # Show Plot
    plt.figure(figsize=(15, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud: 5-Star Reviews in Health & Fitness Category', fontsize=16)
    plt.tight_layout()
    plt.show()
