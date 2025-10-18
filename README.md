# Shoalhaven City Council DA Data Extractor

A **web scraper** that extracts all **Development Application (DA)** details from the **Shoalhaven City Council's DA Tracking portal** for a given date range.

---

## Features

- Collects **all DA URLs** from the Shoalhaven City Council DA Tracking portal.  
- Scrapes detailed information for each DA, including:
  - DA Number
  - Detail URL
  - Description
  - Submitted Date
  - Decision
  - Categories
  - Property Address
  - Applicant
  - Progress
  - Fees
  - Documents
  - Council Contact Info
- Supports **parallel scraping** using Python’s `concurrent.futures` for faster extraction.  
- Writes data **directly to CSV** with multi-line fields preserved.  

---

## Project Structure

```

Shoalhaven_City_Council_Data_Extractor/
│
├─ main.py                  # Entry point to collect URLs and scrape DA details
├─ url_collector.py         # Collects all DA URLs from the portal
├─ page_scraper_parallel.py # Scrapes DA details in parallel and writes to CSV
├─ shoalhaven_urls.txt      # Stores collected DA URLs (generated)
├─ requirements.txt         # contains all external packages and libraries
└─ shoalhaven_data.csv      # Scraped DA data (generated)

````

---

## Usage

1. Clone the repository:

   ```bash
   git clone "https://github.com/akhilpsin/Shoalhaven_City_Council_Data_Extractor"
   cd Shoalhaven_City_Council_Data_Extractor
   ```

2. Make sure to install all the external packages and libraries in **requirements.txt**

3. Run the scraper:

   ```bash
   python main.py
   ```

4. The script will:

   * Collect DA URLs .
   * Scrape DA details in parallel.
   * Save the results in `shoalhaven_data.csv` with proper formatting.

---

## Notes

* The CSV preserves **newlines** in multi-line text fields.
* Each cell is **wrapped in quotes** for safe Excel/Google Sheets import.
* You can adjust the **date range** in `url_collector.py`.
