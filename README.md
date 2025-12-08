# Nepal CIB Blacklist Scraper

A Streamlit application to scrape and analyze the Credit Information Bureau (CIB) of Nepal's blacklist report.

## Features

- **Fresh Data**: Always downloads the latest PDF report from the CIB website.
- **Sample Data**: Quickly fetch the first 10 pages (~400 rows) to preview the data.
- **Full Download**: Scrape the entire dataset (3500+ pages) and download as Excel.
- **Progress Tracking**: Real-time progress bar and status updates.
- **Source Link**: Direct link to the source PDF.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/ashumishra2104/Nepalblacklit.git
    cd Nepalblacklit
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

## Deployment

This app is ready for deployment on [Streamlit Cloud](https://streamlit.io/cloud).
1.  Push this repository to GitHub.
2.  Log in to Streamlit Cloud.
3.  Connect your GitHub account and select this repository.
4.  Deploy!
