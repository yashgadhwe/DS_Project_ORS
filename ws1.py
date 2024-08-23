from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

def extract_urls():
    try:
        product_links = driver.find_elements(By.CSS_SELECTOR, "a.rPDeLR")
        urls = [link.get_attribute("href") for link in product_links if link.get_attribute("href")]
        return urls
    except Exception as e:
        print(f"Error extracting URLs: {e}")
        return []

def extract_product_details():
    try:
        shop_name = driver.find_element(By.CSS_SELECTOR, "h1._6EBuvT span.mEh187").text
        product_name = driver.find_element(By.CSS_SELECTOR, "h1._6EBuvT span.VU-ZEz").text
        product_image = driver.find_element(By.CSS_SELECTOR, "div.gqcSqV img._53J4C-").get_attribute("src")
        present_rate = driver.find_element(By.CSS_SELECTOR, "div.Nx9bqj").text
        actual_rate = driver.find_element(By.CSS_SELECTOR, "div.yRaY8j").text
        deal = driver.find_element(By.CSS_SELECTOR, "div.UkUFwK span").text
        sizes_elements = driver.find_elements(By.CSS_SELECTOR, "div.hSEbzK ul.hSEbzK li.aJWdJI a.CDDksN")
        sizes = [size.text for size in sizes_elements]

        return {
            "shop_name": shop_name,
            "product_name": product_name,
            "product_image": product_image,
            "present_rate": present_rate,
            "actual_rate": actual_rate,
            "deal": deal,
            "sizes": ", ".join(sizes)
        }
    except Exception as e:
        print(f"Error extracting details: {e}")
        return {}

# Open the first page
url = "https://www.flipkart.com/clothing-and-accessories/winter-wear/jackets/men-jackets/pr?sid=clo,qvw,z0g,jbm&otracker=categorytree&otracker=nmenu_sub_Men_0_Jackets"
driver.get(url)

all_urls = []

for page in range(1, 6):
    time.sleep(10)
    urls = extract_urls()
    all_urls.extend(urls)
    print(f"Page {page} URLs:")
    for url in urls:
        print(url)
    
    if page < 5:
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a._9QVEpD span')
            next_button.click()
        except Exception as e:
            print(f"Could not navigate to page {page + 1}: {e}")
            break

all_products = []

for product_url in all_urls:
    try:
        driver.get(product_url)
        time.sleep(5)
        product_details = extract_product_details()
        if product_details:
            all_products.append(product_details)
            print(product_details)
    except Exception as e:
        print(f"Error processing URL {product_url}: {e}")

driver.quit()

# Export to Excel using pandas
if all_products:
    df = pd.DataFrame(all_products)
    df.to_excel("flipkart_products1.xlsx", index=False)
    print(f"\nTotal products processed: {len(all_products)}")
    print("Data has been exported to 'flipkart_products1.xlsx'.")
else:
    print("No products were found.")
