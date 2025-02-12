import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_and_combine_json(file_pattern="*.json"):
    """
    Loads all JSON files and combines them into a one array.
    """
    all_data = []
    for file_name in glob.glob(file_pattern):
        with open(file_name, "r", encoding="utf-8") as f:
            file_data = json.load(f)
            all_data.extend(file_data)
    
    df = pd.DataFrame(all_data)
    return df

def clean_and_prepare(df):
    """
    Cleans and prepares the data for analysis.
    """
    # Convert timestamps
    df['ts'] = pd.to_datetime(df['ts'], errors='coerce')

    # Convert milliseconds played
    df['ms_played'] = pd.to_numeric(df['ms_played'], errors='coerce')

    # Extract date/time components for easier grouping
    df['date'] = df['ts'].dt.date
    df['year'] = df['ts'].dt.year
    df['month'] = df['ts'].dt.month
    df['day'] = df['ts'].dt.day
    df['hour'] = df['ts'].dt.hour
    df['day_of_week'] = df['ts'].dt.day_name()

    # Create minutes played for convenience
    df['minutes_played'] = df['ms_played'] / 1000 / 60

    # Fill missing strings with something more uniform
    df['master_metadata_track_name'] = df['master_metadata_track_name'].fillna("Unknown Track")
    df['master_metadata_album_artist_name'] = df['master_metadata_album_artist_name'].fillna("Unknown Artist")
    df['master_metadata_album_album_name'] = df['master_metadata_album_album_name'].fillna("Unknown Album")
    
    # Drop rows that have a null timestamp or ms_played if desired
    df = df.dropna(subset=['ts', 'ms_played'])
    
    return df

def analyze_listening_over_time(df):
    """
    Shows total minutes listened per day, month, or year.
    """
    daily = df.groupby('date')['minutes_played'].sum().reset_index()
    monthly = df.groupby(['year', 'month'])['minutes_played'].sum().reset_index()
    yearly = df.groupby('year')['minutes_played'].sum().reset_index()

    print("=== Total minutes listened per day (head) ===")
    print(daily.head(), "\n")
    print("=== Total minutes listened per month (head) ===")
    print(monthly.head(), "\n")
    print("=== Total minutes listened per year ===")
    print(yearly, "\n")

    # Example plot: daily listening over time
    plt.figure(figsize=(10,4))
    plt.plot(daily['date'], daily['minutes_played'], marker='o')
    plt.title("Daily Listening Trend")
    plt.xlabel("Date")
    plt.ylabel("Minutes Played")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def analyze_top_artists_tracks_albums(df, top_n=10):
    """
    Prints and plots the top artists, tracks, and albums.
    """
    top_artists = (df.groupby('master_metadata_album_artist_name')['minutes_played']
                     .sum()
                     .sort_values(ascending=False)
                     .head(top_n))
    
    top_tracks = (df.groupby('master_metadata_track_name')['minutes_played']
                    .sum()
                    .sort_values(ascending=False)
                    .head(top_n))
    
    top_albums = (df.groupby('master_metadata_album_album_name')['minutes_played']
                    .sum()
                    .sort_values(ascending=False)
                    .head(top_n))
    
    print(f"=== Top {top_n} Artists (by total minutes played) ===")
    print(top_artists, "\n")
    
    print(f"=== Top {top_n} Tracks (by total minutes played) ===")
    print(top_tracks, "\n")
    
    print(f"=== Top {top_n} Albums (by total minutes played) ===")
    print(top_albums, "\n")
    
    # Plot example: top artists
    plt.figure(figsize=(8,6))
    sns.barplot(x=top_artists.values, y=top_artists.index, palette="viridis")
    plt.title(f"Top {top_n} Artists by Minutes Played")
    plt.xlabel("Minutes Played")
    plt.ylabel("Artist")
    plt.tight_layout()
    plt.show()

def analyze_listening_by_time_of_day(df):
    """
    Shows how listening is distributed by hour of day and by day of week.
    """
    hourly = df.groupby('hour')['minutes_played'].sum().reset_index()
    daily = df.groupby('day_of_week')['minutes_played'].sum().reset_index()
    
    # Sort days of the week in a sensible order
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    daily['day_of_week'] = pd.Categorical(daily['day_of_week'], categories=day_order, ordered=True)
    daily = daily.sort_values('day_of_week')

    plt.figure(figsize=(8,4))
    sns.barplot(x='hour', y='minutes_played', data=hourly, palette="magma")
    plt.title("Listening by Hour of the Day")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Total Minutes Played")
    plt.tight_layout()
    plt.show()
    
    plt.figure(figsize=(8,4))
    sns.barplot(x='day_of_week', y='minutes_played', data=daily, palette="rocket")
    plt.title("Listening by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Total Minutes Played")
    plt.tight_layout()
    plt.show()

def main():
    # 1. Load and combine the data
    df = load_and_combine_json(file_pattern="*.json")
    print(f"Loaded {len(df)} entries from JSON files.")

    # 2. Clean and prepare the data
    df = clean_and_prepare(df)
    print(f"Data after cleaning: {len(df)} entries remain.")

    # 3. Perform analyses
    analyze_listening_over_time(df)
    analyze_top_artists_tracks_albums(df, top_n=10)
    analyze_listening_by_time_of_day(df)

if __name__ == "__main__":
    main()
