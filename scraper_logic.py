import requests
import pdfplumber
import os
import pandas as pd
from bs4 import BeautifulSoup

def get_pdf_url():
    url = "https://cibnepal.org.np/reports?csrt=16497528134041520037"
    try:
        page = requests.get(url)
        page.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page: {e}")
        return None

    soup = BeautifulSoup(page.content, 'html.parser')
    btn_wrapper = soup.find('div', class_='btns-wrapper')
    if btn_wrapper and btn_wrapper.find('a'):
        return btn_wrapper.find('a')['href']
    return None

def download_pdf(pdf_url, path):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open(path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download PDF: {e}")
        return False

def scrape_cib_data(limit=None, max_pages=None, progress_callback=None, return_url=False):
    """
    Scrapes CIB data.
    limit: (Legacy) If set, processes only the first 'limit' pages (approx) AND truncates to 'limit' rows.
    max_pages: If set, processes the first 'max_pages' pages and returns ALL rows from them. Overrides 'limit' for page count.
    progress_callback: Optional function(current, total, message) to report progress.
    return_url: If True, returns (df, pdf_url). If False, returns df (backward compatibility).
    """
    pdf_url = get_pdf_url()
    if not pdf_url:
        return (None, None) if return_url else None

    downloaded_pdf_path = "cib_blacklist_report_temp.pdf"
    
    # Always download to ensure fresh data
    if progress_callback:
        progress_callback(0, 100, "Downloading PDF...")
    print("Downloading PDF...")
    if not download_pdf(pdf_url, downloaded_pdf_path):
        return (None, pdf_url) if return_url else None

    data = []
    header = [
        "S.NO.",
        "BLACKLIST NO.",
        "BLACKLIST DATE",
        "BORROWER NAME",
        "ASSOCIATED PERSON/FM/COMPANIES"
    ]

    try:
        with pdfplumber.open(downloaded_pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            # Determine pages to process
            if max_pages:
                pages_to_process = min(max_pages, total_pages)
            elif limit:
                if limit == 200:
                    pages_to_process = 20 # Approx 10 rows per page usually
                else:
                    pages_to_process = min(limit, total_pages)
            else:
                pages_to_process = total_pages
            
            print(f"Processing {pages_to_process} pages...")
            if progress_callback:
                progress_callback(0, pages_to_process, f"Processing {pages_to_process} pages...")

            for i in range(pages_to_process):
                # Report progress
                if progress_callback:
                    # Update every page or every few pages
                    progress_callback(i + 1, pages_to_process, f"Processing page {i+1}/{pages_to_process}")

                page = pdf.pages[i]
                tables = page.extract_tables()
                
                if not tables:
                    # Try text extraction if no tables found (debug)
                    # print(f"Page {i+1}: No tables found.")
                    pass
                
                for table in tables:
                    if table:
                        for row in table:
                            # Debug print for first few rows
                            if i == 0 and len(data) < 3:
                                print(f"DEBUG ROW: {row}")

                            if row == header:
                                continue
                            if not row or all(cell is None or cell == '' for cell in row):
                                continue
                            
                            # Normalize row length if needed
                            if len(row) < len(header):
                                # Pad with None
                                row += [None] * (len(header) - len(row))
                            elif len(row) > len(header):
                                # Truncate (or handle differently)
                                row = row[:len(header)]
                                
                            data.append(row)
                            
                            # Only break on limit if max_pages is NOT set
                            if limit and not max_pages and len(data) >= limit:
                                break
                
                # Only break on limit if max_pages is NOT set
                if limit and not max_pages and len(data) >= limit:
                    break

        df = pd.DataFrame(data, columns=header)
        df = df.drop_duplicates()
        
        # Only truncate if limit is set AND max_pages is NOT set
        if limit and not max_pages:
            df = df.head(limit)
            
        return (df, pdf_url) if return_url else df

    except Exception as e:
        print(f"Error extracting data: {e}")
        return None
    finally:
        if os.path.exists(downloaded_pdf_path):
            try:
                os.remove(downloaded_pdf_path)
            except:
                pass
