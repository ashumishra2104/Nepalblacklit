from scraper_logic import scrape_cib_data
import time
import datetime
import sys

def progress_reporter(current, total, message):
    # Print progress to stdout so it can be captured
    # Using \r to overwrite line might be tricky in captured output, so just print every 100 pages or so
    if current % 100 == 0 or current == total:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Progress: {current}/{total} - {message}")
        sys.stdout.flush()

if __name__ == "__main__":
    print("Starting FULL scrape (ALL pages)...")
    print("This may take 30-60+ minutes.")
    start_time = time.time()
    
    # max_pages=None means process ALL pages
    # limit=None means process ALL rows
    try:
        df, pdf_url = scrape_cib_data(limit=None, max_pages=None, return_url=True, progress_callback=progress_reporter)
        
        if df is not None and not df.empty:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"cib_blacklist_full_refreshed_{timestamp}.xlsx"
            print(f"Scraping complete. Saving {len(df)} rows to {output_path}...")
            df.to_excel(output_path, index=False)
            print(f"SUCCESS! File saved: {output_path}")
            print(f"Total time taken: {time.time() - start_time:.2f}s")
            if pdf_url:
                print(f"Source PDF URL: {pdf_url}")
        else:
            print("Scrape failed or returned empty data.")
            exit(1)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
