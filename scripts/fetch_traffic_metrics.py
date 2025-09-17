#!/usr/bin/env python3
"""
GitHub Traffic Metrics Fetcher

This script fetches GitHub repository traffic metrics (views and clones)
and saves them to CSV files for tracking over time.
"""

import os
import requests
import csv
import datetime
import sys


def fetch_traffic_metrics():
    """Fetch GitHub traffic metrics and save to CSV files."""
    
    # Get environment variables
    token = os.environ.get('TOKEN')
    repo = os.environ.get('REPO')
    
    if not token:
        print("Error: TOKEN environment variable not set")
        sys.exit(1)
    
    if not repo:
        print("Error: REPO environment variable not set")
        sys.exit(1)
    
    headers = {"Authorization": f"token {token}"}
    
    urls = {
        "views": f"https://api.github.com/repos/{repo}/traffic/views",
        "clones": f"https://api.github.com/repos/{repo}/traffic/clones",
    }
    
    today = datetime.date.today().isoformat()
    os.makedirs("metrics", exist_ok=True)
    
    for metric, url in urls.items():
        print(f"Fetching {metric} data...")
        
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            data = r.json()
            
            filename = f"metrics/{metric}.csv"
            file_exists = os.path.exists(filename)
            
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["date", "count", "uniques"])
                
                # API returns last 14 days → find today's data
                key = "views" if metric == "views" else "clones"
                today_data = next(
                    (d for d in data[key] if d["timestamp"].startswith(today)),
                    None
                )
                
                if today_data:
                    writer.writerow([
                        today,
                        today_data["count"],
                        today_data["uniques"]
                    ])
                    print(f"Added {metric} data for {today}: {today_data['count']} total, {today_data['uniques']} unique")
                else:
                    print(f"No {metric} data found for {today}")
                    
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {metric} data: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error processing {metric} data: {e}")
            sys.exit(1)


if __name__ == "__main__":
    fetch_traffic_metrics()
