from scraper_logic import scrape_cib_data
import pandas as pd
import time

import datetime

print("Starting full scrape using verified logic...")
start_time = time.time()

# limit=None means process all pages
df = scrape_cib_data(limit=None)

if df is not None and not df.empty:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"cib_blacklist_data_{timestamp}.xlsx"
    print(f"Saving {len(df)} rows to {output_path}...")
    df.to_excel(output_path, index=False)
    print(f"Success! Time taken: {time.time() - start_time:.2f}s")
else:
    print("Scrape failed or returned empty data.")
