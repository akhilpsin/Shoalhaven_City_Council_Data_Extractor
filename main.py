# main.py
from Data_scraper_helper.url_collector import collect_urls
from Data_scraper_helper.page_scraper_parallel import scrape_urls_parallel

if __name__ == "__main__":
    # Step 1: Collect URLs (optional if already done)
    collect_urls()

    # Step 2: Read URLs from file
    with open("output_files/shoalhaven_urls.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"⚡ Total URLs to scrape: {len(urls)}")

    # Step 3: Scrape URLs in parallel with live CSV writing
    failed_urls = scrape_urls_parallel(urls, max_workers=5, csv_file="output_files/shoalhaven_data.csv")

    # Step 4: Summary
    if failed_urls:
        print("\n❌ Some URLs failed:")
        for u in failed_urls:
            print(u)
    else:
        print("\n✅ All URLs scraped successfully!")
