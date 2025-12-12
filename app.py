import streamlit as st
import pandas as pd
from scraper_logic import scrape_cib_data
import io
import time

st.set_page_config(page_title="Nepal CIB Blacklist Scraper", layout="wide")

st.title("Nepal CIB Blacklist Scraper")

st.markdown("""
This app scrapes data from the Credit Information Bureau of Nepal (CIB) blacklist report.
You can either fetch a sample (first 10 pages) or download the entire dataset.
""")

# Progress callback function
def update_progress(current, total, message):
    progress_bar.progress(current / total)
    status_text.text(f"{message} ({current}/{total})")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Option 1: Get Sample (First 10 Pages)")
    if st.button("Get Sample"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("Fetching sample data..."):
            # Use max_pages=10 for 10 pages as per user request
            df_sample, pdf_url = scrape_cib_data(max_pages=10, progress_callback=update_progress, return_url=True)
            
            if df_sample is not None:
                st.success(f"Successfully fetched {len(df_sample)} rows!")
                if pdf_url:
                    st.markdown(f"**Source PDF:** [{pdf_url}]({pdf_url})")
                
                st.dataframe(df_sample)
                
                # Convert to Excel for download
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_sample.to_excel(writer, index=False)
                
                st.download_button(
                    label="Download Sample Excel",
                    data=buffer.getvalue(),
                    file_name="cib_blacklist_sample.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Failed to fetch data.")
        
        # Clear progress after completion
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()

with col2:
    st.subheader("Option 2: Download All Data")
    st.info("Note: The full scrape processes 3500+ pages and may take a significant amount of time.")
    
    if st.button("Download All Data"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        st.warning("⚠️ CRITICAL: Do not close this tab. The process takes 30-60+ minutes.")
        
        with st.spinner("Fetching ALL data... (This WILL take a long time, please verify terminal for detailed logs if needed)"):
            # Explicitly using max_pages=None to ensure ALL pages are fetched
            # Previous limit was 'None' which also meant all pages, but being explicit is safer
            df_full, pdf_url = scrape_cib_data(limit=None, max_pages=None, progress_callback=update_progress, return_url=True)
            
            if df_full is not None:
                st.success(f"Successfully fetched {len(df_full)} rows!")
                if pdf_url:
                    st.markdown(f"**Source PDF:** [{pdf_url}]({pdf_url})")
                
                # Convert to Excel for download
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_full.to_excel(writer, index=False)
                
                st.download_button(
                    label="Download Full Excel",
                    data=buffer.getvalue(),
                    file_name=f"cib_blacklist_full_{int(time.time())}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Failed to fetch data.")
        
        # Clear progress after completion
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
