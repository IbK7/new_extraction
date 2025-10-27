from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import pandas as pd

# List of URL objects with their corresponding selectors
urls_with_selectors = [
    {
        'url': 'https://urdu.geo.tv/',
        'selectors': ['h2[data-vr-headline]']
    },
    {
        'url': 'https://urdu.dunyanews.tv/',
        'selectors': ['h3']
    },
    {
        'url': 'https://urdu.arynews.tv/',
        'selectors': ['h2.entry-title', 'h1.entry-title', 'h3.entry-title']
    },
    {
        'url': 'https://www.dawnnews.tv/',
        'selectors': ['h2.story__title',]
    },
    {
        'url': 'https://www.siasat.pk/forums/%D8%AE%D8%A8%D8%B1%DB%8C%DA%BA.69/',
        'selectors': ['h2.articlePreview-title']
    },
    {
        'url': 'https://www.independenturdu.com/',
        'selectors': ['h4[data-vr-headline] a']
    },
    {
        'url': 'https://www.bbc.com/urdu',
        'selectors': ['h3.bbc-ghpu9f']
    },
    {
        'url': 'https://loksujag.com/',
        'selectors': ['h4.card-title']
    }
]

headlines = []


# Load existing headlines if file exists
file_path = 'headlines.csv'
if os.path.exists(file_path):
    existing_df = pd.read_csv(file_path)
    existing_headlines = set(existing_df['headline'].tolist())  # Fast lookup for duplicates
    start_index = len(existing_df)  # Continue ID from the last value
else:
    existing_headlines = set()
    start_index = 0  # Start from 0 if file does not exist


# Initialize the WebDriver
driver = webdriver.Chrome()

driver = webdriver.Chrome()

try:
    print("bjadbvdasdasdasdasd")
    for url_obj in urls_with_selectors:
        url = url_obj['url']
        selectors = url_obj['selectors']
        
        driver.get(url)
        print(f"Scraping headlines from {url}...")
        time.sleep(5)  # Delay for page loading
        
        for selector in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                for element in elements:
                    headline_text = element.text.strip()
                    if 'bbc' in url:
                        spans = element.find_elements(By.CSS_SELECTOR, "span:not([data-testid='visually-hidden-text'])")
                
                        extracted_texts = [span.text.strip() for span in spans if span.text.strip()]
                        if not extracted_texts:
                            headline_text = element.text.strip()  # Fallback if no valid spans
                        else:
                            headline_text = " ".join(extracted_texts)  # Join extracted parts

                        # Remove commas in text3 (assumed last element)
                        headline_text = headline_text.rsplit(" ", 1)[0] if "," in headline_text.split()[-1] else headline_text
                    
                    
                    if not headline_text:  # If no text, check child <a> tags
                        a_tags = element.find_elements(By.CSS_SELECTOR, 'a')
                        for a_tag in a_tags:
                            headline_text = a_tag.text.strip()
                            if headline_text and headline_text not in existing_headlines:
                                headlines.append({'source': url, 'headline': headline_text})
                                existing_headlines.add(headline_text)  # Add to set to avoid rechecking
                    elif headline_text not in existing_headlines:
                        headlines.append({'source': url, 'headline': headline_text})
                        existing_headlines.add(headline_text)  # Add to set to avoid rechecking
            # print(f"Found {len(headlines)} new headlines from {url}.")
    # Save new headlines to CSV if any new ones exist
    if headlines:
        df = pd.DataFrame(headlines)
        df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
        print(f"Added {len(headlines)} new headlines.")
    else:
        print("No new headlines found.")
        
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()


