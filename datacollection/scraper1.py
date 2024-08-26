import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define the base URL for pagination
base_url = 'https://www.flipkart.com/clothing-and-accessories/winter-wear/sweater/men-sweater/pr?sid=clo%2Cqvw%2Cvkb%2Cieq&otracker=categorytree&otracker=nmenu_sub_Men_0_Sweater&page='

def extract_urls_from_page(url):
    response = requests.get(url)
    urls = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.select('a.rPDeLR') if 'href' in a.attrs]  # Correct selector
        urls = [f"https://www.flipkart.com{link}" for link in links]
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    return urls


def extract_product_details(product_url):
    response = requests.get(product_url)
    details = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract brand name and product name
        try:
            h1_tag = soup.select_one('h1._6EBuvT')
            brand_name = h1_tag.select_one('span.mEh187').text if h1_tag else "N/A"
            product_name = h1_tag.select_one('span.VU-ZEz').text if h1_tag else "N/A"
        except AttributeError:
            brand_name = "N/A"
            product_name = "N/A"
        
        # Extract product image
        try:
            product_image = soup.select_one('img._53J4C-')['src']
        except (AttributeError, TypeError):
            product_image = "N/A"
        
        # Extract offer price, original price, and deal percentage
        try:
            offer_price = soup.select_one('div.Nx9bqj.CxhGGd').text
        except AttributeError:
            offer_price = "N/A"
        
        try:
            original_price = soup.select_one('div.yRaY8j').text
        except AttributeError:
            original_price = "N/A"
        
        try:
            deal_percentage = soup.select_one('div.UkUFwK.WW8yVX.dB67CR span').text
        except AttributeError:
            deal_percentage = "N/A"
        
        # Extract available colors
        #try:
        #    color_elements = soup.select('div.V3Zflw.QX54-Q.E1E-3Z.dpZEpc')
        #    colors = [color.text.strip() for color in color_elements]
        #except AttributeError:
        #    colors = []

        # Extract available sizes
        try:
            size_elements = soup.select('ul.hSEbzK li a.CDDksN.zmLe5G.dpZEpc')
            sizes = [size.text for size in size_elements]
        except AttributeError:
            sizes = []

        # Extract rating
        try:
            rating = soup.select_one('div.XQDdHH._1Quie7').text
        except AttributeError:
            rating = "N/A"
        
        details = {
            "brand_name": brand_name,
            "product_name": product_name,
            "product_image": product_image,
            "offer_price": offer_price,
            "original_price": original_price,
            "deal_percentage": deal_percentage,
            #"colors": ", ".join(colors),
            "sizes": ", ".join(sizes),
            "rating": rating
        }
    else:
        print(f"Failed to retrieve the product details. Status code: {response.status_code}")
    
    return details


all_urls = []
for page in range(1, 100):
    if len(all_urls) < 400:
        url = f"{base_url}{page}"
        print(f"Fetching URLs from: {url}")
        urls_from_page = extract_urls_from_page(url)
        all_urls.extend(urls_from_page)
        time.sleep(2)
    else:
        pass

print(f"Total URLs extracted: {len(all_urls)}")

all_products = []
for product_url in all_urls:
    if len(all_products) < 200:
        product_details = extract_product_details(product_url)
        if product_details:
            all_products.append(product_details)
            print(product_details)
        time.sleep(2)  # Sleep to avoid hitting the server too hard
    else:
        pass

# Export to Excel using pandas
df = pd.DataFrame(all_products)
df.to_excel("flipkart_products_sweater.xlsx", index=False)

print(f"\nTotal products processed: {len(all_products)}")
print("Data has been exported to 'flipkart_products_sweater.xlsx'.")
