# page_scraper_parallel.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

# --------------------------
# Worker function to scrape a single URL
# --------------------------
def scrape_single_url(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(2)

        # Step 1: Click Agree once
        base_url = "https://www3.shoalhaven.nsw.gov.au/masterviewUI/modules/ApplicationMaster/Default.aspx"
        driver.get(base_url)
        try:
            agree_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Agree']"))
            )
            agree_button.click()
            time.sleep(0.5)
        except TimeoutException:
            pass

        driver.get(url)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "ctl00_cphContent_ctl00_lblApplicationHeader"))
        )

        # Click "Expand All"
        try:
            expand_all = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@href,'javascript:expandCollapse(\"expand\")')]")
                )
            )
            expand_all.click()
            time.sleep(0.3)
        except TimeoutException:
            pass

        # --------------------------
        # Extract data
        # --------------------------
        data = {}
        data["DA_Number"] = driver.find_element(By.ID, "ctl00_cphContent_ctl00_lblApplicationHeader").text.strip()
        data["Detail_URL"] = url

        details_text = driver.find_element(By.ID, "lblDetails").text.strip()
        if "Submitted:" in details_text:
            des, sub_date = details_text.split("Submitted:", 1)
            data["Description"] = des.replace("Description:", "").strip()
            data["Submitted_Date"] = sub_date.strip()
        else:
            data["Description"] = details_text.replace("Description:", "").strip()
            data["Submitted_Date"] = ""

        data["Decision"] = driver.find_element(By.ID, "lblDecision").text.strip()
        data["Categories"] = driver.find_element(By.ID, "lblCat").text.strip()
        data["Property_Address"] = driver.find_element(By.ID, "lblProp").text.strip()
        data["Applicant"] = driver.find_element(By.ID, "lblPeople").text.replace("Applicant: ", "").strip()
        data["Progress"] = driver.find_element(By.ID, "lblProg").text.strip()

        fees_text = driver.find_element(By.ID, "lblFees").text.strip()
        data["Fees"] = "Not required" if fees_text == "No fees recorded against this application." else fees_text

        data["Documents"] = driver.find_element(By.ID, "lblDocs").text.strip()

        contact_text = driver.find_element(By.ID, "lbl91").text.strip()
        data["Contact_Council"] = (
            "Not required"
            if contact_text
            == "Application Is Not on exhibition, please call Council on 1300 293 111 if you require assistance."
            else contact_text
        )

        driver.quit()
        return (url, data, None)

    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return (url, None, str(e))


# --------------------------
# Main function to scrape all URLs in parallel and write CSV
# --------------------------
def scrape_urls_parallel(urls, max_workers=5, csv_file="output_files/shoalhaven_data.csv"):
    fieldnames = [
        "DA_Number", "Detail_URL", "Description", "Submitted_Date", "Decision",
        "Categories", "Property_Address", "Applicant", "Progress",
        "Fees", "Documents", "Contact_Council"
    ]

    # Create CSV with header if not exists
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writeheader()

        failed_urls = []

        # Use ProcessPoolExecutor for parallel scraping
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(scrape_single_url, url): url for url in urls}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    _, data, error = future.result()
                    if data:
                        writer.writerow(data)  # write immediately to CSV
                        print(f"✅ Success: {url}")
                    else:
                        failed_urls.append(url)
                        print(f"❌ Failed: {url} - {error}")
                except Exception as e:
                    failed_urls.append(url)
                    print(f"❌ Failed (exception): {url} - {e}")

    print(f"\n✅ Scraping complete. Success: {len(urls) - len(failed_urls)}, Failed: {len(failed_urls)}")
    if failed_urls:
        print("Failed URLs:")
        for u in failed_urls:
            print(u)

    return failed_urls


# --------------------------
# Standalone run
# --------------------------
if __name__ == "__main__":
    with open("output_files/shoalhaven_urls.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    scrape_urls_parallel(urls, max_workers=5)
