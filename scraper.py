import pandas as pd
from google_play_scraper import Sort, reviews
import os

# 1. Setup - Define the apps from your Interim Report
apps = {
    'UMANG': 'in.gov.umang.negd.g2c',
    'DigiLocker': 'com.digilocker.android',
    'AarogyaSetu': 'nic.goi.aarogyasetu'
}

# Create a data directory if it doesn't exist
output_dir = 'data/raw'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def scrape_app_reviews(app_name, app_id, count=1000):
    print(f"Starting scrape for {app_name}...")
    
    # Scrape reviews
    result, continuation_token = reviews(
        app_id,
        lang='en', # Focusing on English as per your report limitations
        country='in',
        sort=Sort.NEWEST, # Get the most recent feedback
        count=count
    )
    
    # Convert to DataFrame
    df = pd.DataFrame(result)
    
    # Add the App Name for identification
    df['App_Name'] = app_name
    
    # Select and rename columns to match your Data Dictionary[cite: 1]
    # Mapping: content -> Review_Text, score -> Star_Rating, at -> Timestamp
    df_filtered = df[['App_Name', 'content', 'score', 'at']].copy()
    df_filtered.columns = ['App_Name', 'Review_Text', 'Star_Rating', 'Timestamp']
    
    # Save to CSV[cite: 2]
    file_path = os.path.join(output_dir, f"{app_name}_reviews.csv")
    df_filtered.to_csv(file_path, index=False)
    print(f"Saved {len(df_filtered)} reviews to {file_path}")

# Execute scraping for all apps
for name, id in apps.items():
    # Scraping 500 per app to start hitting your 1,000+ target[cite: 1, 2]
    scrape_app_reviews(name, id, count=500)

print("\nScraping complete! You can now find the files in the 'data/raw' folder.")