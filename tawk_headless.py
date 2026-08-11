from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import tempfile
import shutil
import os
"""
python tawk_headless.py
"""

"""
sudo apt update
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
sudo apt install -y python3-pip
sudo pip3 install requests selenium
python3 tawk.py

pip install requests selenium
python main.py
python tawk.py
"""

# -----------------------------
# Configuration
# -----------------------------
URL = "https://iptvforall2026.blogspot.com/"
URL = "https://free-iptv-2026.netlify.app/"

SUBJECT = "Win 1000$ Amazon Gift Card"
MESSAGE = " "


def find_tawk_badge(driver, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        driver.switch_to.default_content()

        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        #print("IFRAMES:", len(iframes))

        for i, iframe in enumerate(iframes):
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame(iframe)

                badges = driver.find_elements(
                    By.CSS_SELECTOR,
                    "span.tawk-badge.tawk-min-badge"
                )

                #print(f"iframe {i}: badges found = {len(badges)}")

                for badge in badges:
                    """
                    print("BADGE TEXT:", repr(badge.text))
                    print("BADGE HTML:", badge.get_attribute("outerHTML"))
                    """
                    if badge.is_displayed():
                        print("BADGE IS DISPLAYED")

                        if badge.text.strip() == "1":
                            driver.switch_to.default_content()
                            return True

            except Exception as e:
                print(f"iframe {i} error:", type(e).__name__, str(e))

    driver.switch_to.default_content()
    return False
    
# -----------------------------
# Start browser
# -----------------------------
GAS_URL = "https://script.google.com/macros/s/AKfycbywZwu_IQws8T01Jit2-ijsNHxsEKdrtUV0kd24VAGxz9YEbm8oHSDpD87eRdzYBuz-/exec"
while True:
    profile_dir = tempfile.mkdtemp(prefix="chrome-profile-")
    response = None
    while True:
        try:
            response = requests.get(GAS_URL, params={
                "action": "get"
            })
            print(response.status_code)
            print(response.headers.get("Content-Type"))
            print(response.text)
            break
        except:
            pass
    data = response.json()
    EMAIL = None
    if data["success"]:
        EMAIL = data["email"]
        print('Email: ', EMAIL)
      
        
        options = webdriver.ChromeOptions()
      
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--proxy-server=http://127.0.0.1:8118")
        options.add_argument(
            f"--user-data-dir={profile_dir}"
        )
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/143.0.0.0 Safari/537.36"
        )
        
        driver = webdriver.Chrome(options=options)
        driver.get(URL)

        wait = WebDriverWait(driver, 10)
        #time.sleep(50000)
        if find_tawk_badge(driver):
            print("Badge is 1")
        else:
            print("Badge not found or text isn't 1")
            
        driver.switch_to.default_content()
        chat_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.chat-button"))
        )
        driver.execute_script("arguments[0].click();", chat_button)
        time.sleep(1)

        # Wait a few seconds for Tawk to load
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )

        # -------------------------------------------------------
        # Find the Tawk iframe
        # -------------------------------------------------------
        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        found = False

        for iframe in iframes:
            driver.switch_to.default_content()

            try:
                driver.switch_to.frame(iframe)

                # Check if the offline form exists
                if driver.find_element(By.XPATH, "//input[@aria-placeholder='Subject']"):
                    found = True
                    break

            except:
                pass

        if not found:
            print("Offline form not found. iframe length: ", len(iframes))
            driver.quit()
            exit()

        # -------------------------------------------------------
        # Fill the form
        # -------------------------------------------------------

        driver.find_element(By.XPATH, "//input[@aria-placeholder='Name']").send_keys(EMAIL)
        driver.find_element(By.XPATH, "//input[@aria-placeholder='Email']").send_keys(EMAIL)

        driver.find_element(By.XPATH, "//input[@aria-placeholder='Subject']").send_keys(SUBJECT)

        txt = driver.find_element(By.XPATH, "//textarea")

        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        # Create a dedicated directory if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        
        # Build an absolute, explicit path for the file
        screenshot_path = os.path.join(os.getcwd(), "screenshots", f"screenshot_{EMAIL}.png")
        
        # Force a window size extension to ensure the page renders 
        driver.set_window_size(1920, 1080)
        driver.save_screenshot(screenshot_path)
        print(f"Captured screen successfully at: {screenshot_path}")

        print(f"Found {len(textareas)} textarea(s)")
        for ta in driver.find_elements(By.TAG_NAME, "textarea"):
            if ta.is_displayed() and ta.is_enabled():
                ta.click()
                ta.send_keys(MESSAGE)
                parent = ta.find_element(By.XPATH, "..")
                next_sibling = parent.find_element(By.XPATH, "following-sibling::*[1]")
                next_sibling.click()
                break

        # Click submit
        #driver.find_element(By.CSS_SELECTOR, "button[type='button']").click()

        print("Form submitted successfully.")
