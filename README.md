# Spotify Extended Data Analysis

This repository contains a Python script and some example Spotify JSON files representing **my** personal listening history data. If you'd like to analyze your own data, simply delete the JSON files included here and replace them with your own Spotify extended history files.

## Prerequisites

- Python 3.7+
- [Pip](https://pip.pypa.io/en/stable/) for installing dependencies

## Installation

1. Clone or download this repository to your local machine.
2. Install the required Python libraries:
   ```python
   pip install pandas matplotlib seaborn
   ```

## Usage

1. Make sure your Spotify streaming history JSON files (e.g., StreamingHistory0.json, StreamingHistory1.json, etc.) are in the same directory as the script.
2. Run the analysis script:
```python
python spotify_analysis.py
```

3. The script will:

  - Automatically detect and load all .json files in the folder.
  - Merge them into a single dataset.
  - Clean and prepare the data.
  - Perform various analyses, printing summary results and generating visualizations such as:
    - Daily listening trend
    - Top artists, tracks, and albums
    - Listening by hour and day of week

## Customizing
- Delete or rename the provided JSON files before adding your own data if you don’t want to mix my example data with yours.
