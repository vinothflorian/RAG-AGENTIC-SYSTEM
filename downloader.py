import aiohttp
import asyncio
import os
import json
from datetime import datetime, timedelta

RAW_DATA_DIR = "JSON_FILE"
os.makedirs(RAW_DATA_DIR, exist_ok=True)
BASE_URL = "https://www.federalregister.gov/api/v1/documents.json"

async def fetch_documents_for_date(session, date_str):
    params = {
        "per_page": 1000,
        "order": "newest",
        "conditions[publication_date]": date_str
    }
    print(f"Requesting data for {date_str}...")
    async with session.get(BASE_URL, params=params) as response:
        if response.status != 200:
            print(f"Failed to fetch data for {date_str}: {response.status}")
            print(await response.text())
            return
        data = await response.json()
        if not data.get("results"):
            print(f"No documents found for {date_str}")
        file_path = os.path.join(RAW_DATA_DIR, f"documents_{date_str}.json")
        with open(file_path, "w", encoding="utf-8") as fl:
            json.dump(data, fl, indent=2)
        print(f"Saved data for {date_str} to {file_path}")

async def fetch_last_7_days():
    today = datetime.utcnow()
    print(f"Saving files to: {os.path.abspath(RAW_DATA_DIR)}")
    async with aiohttp.ClientSession() as session:
        for i in range(7):
            day = today - timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            await fetch_documents_for_date(session, date_str)
            await asyncio.sleep(1)  # avoid rate limits

if __name__ == "__main__":
    asyncio.run(fetch_last_7_days())
    print("Data fetching completed for the last 7 days.")