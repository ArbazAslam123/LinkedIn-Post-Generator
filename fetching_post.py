from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import json
import re

def extract_linkedin_posts(profile_url, li_at_cookie, scroll_attempts=5):
    # 1. Configure browser for the extraction pipeline
    chrome_options = Options()
    # chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-notifications")
    chrome_options.page_load_strategy = 'eager'
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(20)
    
    # 2. Establish session context via the domain before injecting cookies
    print("Connecting to LinkedIn to establish domain context...")
    try:
        driver.get("https://www.linkedin.com")
    except TimeoutException:
        print("Initial page load reached threshold, domain context established. Proceeding...")
        
    driver.add_cookie({
        "name": "li_at",
        "value": li_at_cookie,
        "domain": ".linkedin.com"
    })
    
    # 3. Navigate directly to the target's recent activity feed
    feed_url = f"{profile_url.rstrip('/')}/recent-activity/shares/"
    print(f"Navigating to feed: {feed_url}")
    
    try:
        driver.get(feed_url)
    except TimeoutException:
        print("Feed page load reached timeout threshold. Moving to data extraction...")

    time.sleep(5) 
    
    # MULTIPLE SCROLLS TO FETCH MORE POSTS
    print(f"Scrolling {scroll_attempts} times to load more posts...")
    for i in range(scroll_attempts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3) # Wait for the new posts to render
        print(f"Scroll {i + 1}/{scroll_attempts} complete.")
    
    # 4. Parse the raw HTML structure
    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts_data = []
    
    post_containers = soup.find_all("div", attrs={"data-urn": True})
    
    if not post_containers:
        post_containers = soup.find_all("div", class_="feed-shared-update-v2")
    
    for container in post_containers:
        text_box = container.find("span", class_="break-words")
        if not text_box:
            text_box = container.find("div", class_="update-components-text")
            
        # --- THE FIX: MANUALLY REPLACE HTML BREAKS WITH \n ---
        if text_box:
            # Swap <br> tags for \n
            for br in text_box.find_all("br"):
                br.replace_with("\n")
            # Insert a \n after paragraph tags
            for p in text_box.find_all("p"):
                p.insert_after("\n")
                
            post_text = text_box.get_text(separator="\n").strip()
            # Clean up excessive newlines (normalizing gaps)
            post_text = re.sub(r'\n\s*\n', '\n\n', post_text)
        else:
            post_text = ""
        # -----------------------------------------------------
        
        if not post_text or post_text == "No text found":
            continue
            
        likes_box = container.find("span", class_="social-details-social-counts__reactions-count")
        if not likes_box:
            likes_box = container.find("button", class_="social-details-social-counts__count-value")
            
        likes_raw = likes_box.text.strip() if likes_box else "0"
        
        likes_cleaned = re.sub(r'\D', '', likes_raw)
        engagement_metric = int(likes_cleaned) if likes_cleaned else 0
        
        if not any(p['text'] == post_text for p in posts_data):
            posts_data.append({
                "text": post_text,
                "engagement": engagement_metric
            })
        
    driver.quit()
    return posts_data

# Execution Block
if __name__ == "__main__":
    my_cookie = ""
    target_profile = "https://www.linkedin.com/in/alliekmiller"
    
    print("Starting extraction...")
    # You can change the number '10' below to scroll more or fewer times
    extracted_data = extract_linkedin_posts(target_profile, my_cookie, scroll_attempts=10)
    
    # Dump the data into a JSON file
    with open("linkedin_feed_data.json", "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)
        
    print(f"Successfully extracted {len(extracted_data)} unique posts and saved to linkedin_feed_data.json!")