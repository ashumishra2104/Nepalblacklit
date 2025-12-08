from scraper_logic import scrape_cib_data
import time
import datetime

print("Starting sample scrape (first 10 pages)...")
start_time = time.time()

# max_pages=10 means process first 10 pages
df, pdf_url = scrape_cib_data(max_pages=10, return_url=True)

if df is not None and not df.empty:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"cib_blacklist_sample_10pages_{timestamp}.xlsx"
    print(f"Saving {len(df)} rows to {output_path}...")
    df.to_excel(output_path, index=False)
    print(f"Success! Time taken: {time.time() - start_time:.2f}s")
else:
    print("Scrape failed or returned empty data.")
