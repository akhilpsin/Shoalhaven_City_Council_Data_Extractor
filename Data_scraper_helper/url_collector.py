# url_collector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def collect_urls():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # headless
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)

    try:
        driver.get("https://www3.shoalhaven.nsw.gov.au/masterviewUI/modules/ApplicationMaster/Default.aspx")

        try:
            agree_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Agree']"))
            )
            agree_button.click()
            time.sleep(2)
        except:
            pass

        # Navigate to DA Tracking > Advanced Search
        da_tracking_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='DA Tracking']/ancestor::a"))
        )
        da_tracking_link.click()

        advanced_search_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Advanced Search']/ancestor::a"))
        )
        advanced_search_link.click()

        # Set date range
        from_date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_cphContent_ctl00_ctl03_dateInput_text"))
        )
        to_date_input = driver.find_element(By.ID, "ctl00_cphContent_ctl00_ctl05_dateInput_text")
        from_date_input.clear()
        from_date_input.send_keys("01/09/2025")
        to_date_input.clear()
        to_date_input.send_keys("30/09/2025")

        search_button = driver.find_element(By.ID, "ctl00_cphContent_ctl00_btnSearch")
        search_button.click()

        base_url = "https://www3.shoalhaven.nsw.gov.au/masterviewUI/modules/ApplicationMaster/"
        all_urls = []
        prev_page_urls = set()
        page_count = 0

        while True:
            page_count += 1
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class,'rgRow') or contains(@class,'rgAltRow')]"))
            )

            current_page_urls = set()
            for row in rows:
                link = row.find_element(By.XPATH, ".//a[contains(@href, 'default.aspx?page=wrapper')]").get_attribute("href")
                if not link.startswith("http"):
                    link = base_url + link.lstrip("./")
                current_page_urls.add(link)

            if current_page_urls == prev_page_urls:
                break

            all_urls.extend(current_page_urls)
            prev_page_urls = current_page_urls.copy()

            try:
                next_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.rgPageNext[title='Next Page']"))
                )
                if "disabled" in next_button.get_attribute("class").lower():
                    break
                next_button.click()
                time.sleep(1)
            except:
                break

        # Save to file
        with open("output_files/shoalhaven_urls.txt", "w", encoding="utf-8") as f:
            for u in all_urls:
                f.write(u + "\n")

        print(f"✅ Total URLs collected: {len(all_urls)}")
        return all_urls

    finally:
        driver.quit()

if __name__ == "__main__":
    collect_urls()
