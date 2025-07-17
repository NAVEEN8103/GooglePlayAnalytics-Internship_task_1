import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import numpy as np

# Function to check if current time is between 1 PM and 2 PM IST
def is_time_between_1pm_2pm_ist():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    current_hour = now.hour
    return 13 <= current_hour < 14  # 13:00 to 13:59 (1 PM to 2 PM IST)

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
        # Remove '+' and ',' and convert to integer
        return int(install.replace('+', '').replace(',', ''))
    except (ValueError, AttributeError):
        # Return None for invalid entries like 'Free'
        return None

df['Installs'] = df['Installs'].apply(clean_installs)
# Drop rows with invalid Installs
df = df.dropna(subset=['Installs'])

# Clean Price: Remove '$' and convert to float
df['Price'] = df['Price'].str.replace('$', '', regex=False).astype(float)

# Calculate Revenue: Price * Installs
df['Revenue'] = df['Price'] * df['Installs']

# Clean Size: Convert 'M' to float, exclude 'Varies with device'
df['Size'] = df['Size'].str.replace('M', '', regex=False)
df = df[df['Size'] != 'Varies with device']
df['Size'] = pd.to_numeric(df['Size'], errors='coerce')

# Clean Android Version: Extract numeric part (e.g., '4.0.3 and up' -> 4.0)
def extract_android_version(ver):
    try:
        # Take the first number or numbers before ' and'
        return float(ver.split(' and')[0].split()[0])
    except:
        return np.nan

df['Android Ver'] = df['Android Ver'].apply(extract_android_version)

# Apply Filters
df = df[
    (df['Installs'] >= 10000) &
    (df['Revenue'] >= 10000) &
    (df['Android Ver'] > 4.0) &
    (df['Size'] > 15) &
    (df['Content Rating'] == 'Everyone') &
    (df['App'].str.len() <= 30)
].dropna()

# Print filtered DataFrame for debugging
print(f"Filtered DataFrame ({len(df)} apps):")
print(df[['App', 'Category', 'Type', 'Installs', 'Revenue', 'Size', 'Android Ver', 'Content Rating']])

# Get top 3 categories by number of apps
top_categories = df['Category'].value_counts().head(3).index.tolist()
print(f"Top 3 categories: {top_categories}")

# Filter for top 3 categories
df_top = df[df['Category'].isin(top_categories)]

# Calculate average installs and revenue for Free vs Paid apps
grouped = df_top.groupby(['Category', 'Type']).agg({
    'Installs': 'mean',
    'Revenue': 'mean'
}).reset_index()

# Check if current time is between 1 PM and 2 PM IST
if is_time_between_1pm_2pm_ist():
    # Prepare data for plotting
    categories = top_categories
    free_installs = grouped[grouped['Type'] == 'Free']['Installs'].values
    paid_installs = grouped[grouped['Type'] == 'Paid']['Installs'].values
    free_revenue = grouped[grouped['Type'] == 'Free']['Revenue'].values
    paid_revenue = grouped[grouped['Type'] == 'Paid']['Revenue'].values

    # Ensure arrays are of equal length
    if len(free_installs) < len(categories):
        free_installs = list(free_installs) + [0] * (len(categories) - len(free_installs))
    if len(paid_installs) < len(categories):
        paid_installs = list(paid_installs) + [0] * (len(categories) - len(paid_installs))
    if len(free_revenue) < len(categories):
        free_revenue = list(free_revenue) + [0] * (len(categories) - len(free_revenue))
    if len(paid_revenue) < len(categories):
        paid_revenue = list(paid_revenue) + [0] * (len(categories) - len(paid_revenue))

    # Create dual-axis chart
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Bar positions
    bar_width = 0.35
    x = range(len(categories))

    # Plot installs on primary y-axis
    ax1.bar([i - bar_width/2 for i in x], free_installs, bar_width, label='Free Installs', color='#1f77b4')
    ax1.bar([i + bar_width/2 for i in x], paid_installs, bar_width, label='Paid Installs', color='#ff7f0e')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Average Installs', color='#1f77b4')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, rotation=45)

    # Create secondary y-axis for revenue
    ax2 = ax1.twinx()
    ax2.plot(x, free_revenue, 'o-', label='Free Revenue', color='#2ca02c', linewidth=2, markersize=8)
    ax2.plot(x, paid_revenue, 's-', label='Paid Revenue', color='#d62728', linewidth=2, markersize=8)
    ax2.set_ylabel('Average Revenue ($)', color='#d62728')
    ax2.tick_params(axis='y', labelcolor='#d62728')

    # Title and legend
    plt.title('Average Installs and Revenue for Free vs. Paid Apps in Top 3 Categories')
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=4)

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show plot
    plt.show()
else:
    print("Chart is only available between 1 PM and 2 PM IST.")