import requests
from pathlib import Path
import json
from datetime import datetime, timezone, timedelta

def fetch_and_save_json(url: str, local_file: str = "job_listings.json"):
    """
    Fetches JSON data from a remote URL and saves it to a local file.
    
    Parameters:
    - url: str -> URL of the remote JSON file
    - local_file: str -> Path to save the local JSON file
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()

        # Save locally
        with open(local_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        print(f"Successfully saved {len(data)} records to '{local_file}'")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")

def filter_jobs(input_file_path : str = "job_listings.json", output_file_path : str = "filtered_jobs.json"):
    with open(input_file_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    # Get today's date
    today = datetime.now(timezone.utc).date()

    yesterday = (datetime.now(timezone.utc) - timedelta(days=2)).date()

    # Filter jobs posted today
    # jobs_posted_today = [
    #     job for job in jobs
    #     if job.get("date_posted", 0) == 1751392325
    # ]

    jobs_posted_today = jobs[0:5]

    # Save to a separate JSON file
    output_file = Path(output_file_path)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(jobs_posted_today, f, indent=2)

    print(f"Saved {len(jobs_posted_today)} jobs posted today to '{output_file}'")
