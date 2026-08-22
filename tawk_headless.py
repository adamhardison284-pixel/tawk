from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import random
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

python main.py
pip install requests selenium
python tawk_headless_2.py
"""

# -----------------------------
# Configuration
# -----------------------------
URL = "https://iptvforall2026.blogspot.com/"
URL = "https://free-iptv-2026.netlify.app/"

SUBJECT = "Win 1000$ Amazon Gift Card"

titles = [
    "Win a $1,000 Amazon Gift Card!",
    "Enter to Win $1,000 at Amazon!",
    "You Could Win a $1,000 Amazon Gift Card",
    "Get a Chance to Win $1,000 on Amazon",
    "Win $1,000 to Spend on Amazon!",
    "Claim Your Chance at a $1,000 Amazon Gift Card",
    "Enter Now for a Chance to Win $1,000",
    "$1,000 Amazon Gift Card Giveaway!",
    "Could You Be the Winner of $1,000?",
    "Your Chance to Score a $1,000 Amazon Gift Card",
    "Take Your Shot at Winning $1,000 on Amazon",
    "Enter the $1,000 Amazon Gift Card Giveaway",
    "Win Big: $1,000 Amazon Gift Card Up for Grabs!",
    "A $1,000 Amazon Gift Card Could Be Yours!",
    "Want to Win $1,000 on Amazon? Enter Now!",
    "Lucky Winner Could Receive a $1,000 Amazon Gift Card",
    "Don’t Miss Your Chance to Win $1,000",
    "Enter for a Chance at a $1,000 Amazon Gift Card",
    "Score a $1,000 Amazon Gift Card!",
    "$1,000 Amazon Shopping Spree — Enter to Win!"
]

MESSAGE = " "


def find_tawk_badge(driver, timeout=10):
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
GAS_URL = "https://uryfrvpoyhrzfgctupqk.supabase.co/functions/v1/email-api"
global_tour = 0
while True:
    global_tour = global_tour + 1
    
    profile_dir = tempfile.mkdtemp(prefix="chrome-profile-")
    options = webdriver.ChromeOptions()
    options.set_capability("goog:loggingPrefs", {
        "browser": "ALL"
    })
    
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        f"--user-data-dir={profile_dir}"
    )

    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.0.0 Safari/537.36"
    )
    
    driver = webdriver.Chrome(options=options)
    inc = 0
    data = None
    sites = None
    GAS_URL_ = "https://xvdqarulxvrjumqkjmeb.supabase.co/functions/v1/get_ready_emails"
    while True:
        try:
            response = requests.get(GAS_URL_)
            data = response.json()
            if data.get("status_") == "success":
                sites = data.get("emails", [])
                break
        except:
            print("get email tawk error")
        time.sleep(0.5)
    print('sites: ', sites)
    for site in sites:
        print("step: 1")
        URL = "https://" + site.split('@')[0] + ".netlify.app"
        print("URL: ", URL)
        response = None
        while True:
            try:
                response = requests.get(GAS_URL, params={
                    "action": "get"
                })
                break
            except:
                print("get email api error")
            time.sleep(0.5)
        try:
            data = response.json()
            EMAIL = None
            if data["success"]:
                EMAIL = data["email"]
                print('Email: ', EMAIL)
                
                driver.get(URL)

                wait = WebDriverWait(driver, 5)
                bdg_inc = 0
                already = False
                while True:
                    if bdg_inc < 2:
                        if find_tawk_badge(driver):
                            print("Badge is 1")
                            break
                        else:
                            print("Badge not found or text isn't 1")
                            for log in driver.get_log("browser"):
                                if "tawk" in log["message"].lower() or "cors" in log["message"].lower():
                                    print(log["message"])
                            driver.refresh()
                        bdg_inc = bdg_inc + 1
                    else:
                        already = True
                        break
                        
                print('already: ', already)
                if already == False:
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
                    SUBJECT = random.choice(titles)
                    driver.find_element(By.XPATH, "//input[@aria-placeholder='Subject']").send_keys(SUBJECT)

                    txt = driver.find_element(By.XPATH, "//textarea")

                    textareas = driver.find_elements(By.TAG_NAME, "textarea")

                    print(f"Found {len(textareas)} textarea(s)")
                    for ta in driver.find_elements(By.TAG_NAME, "textarea"):
                        if ta.is_displayed() and ta.is_enabled():
                            ta.click()
                            ta.send_keys(MESSAGE)
                            parent = ta.find_element(By.XPATH, "..")
                            next_sibling = parent.find_element(By.XPATH, "following-sibling::*[1]")
                            next_sibling.click()
                            time.sleep(1)
                                
                            break

                    # Click submit
                    #driver.find_element(By.CSS_SELECTOR, "button[type='button']").click()
                    
                    while True:
                        red_texts = driver.find_elements(
                            By.XPATH,
                            "//*[contains(@class, 'tawk-text-red-1')]"
                        )
                        if len(red_texts) > 0:
                            while True:
                                try:
                                    # Mark as pending
                                    r = requests.get("https://xvdqarulxvrjumqkjmeb.supabase.co/functions/v1/email_stop_time", params={
                                        "email": site
                                    })
                                    print(r.json())
                                    break
                                except:
                                    pass
                                    
                            while True:
                                try:
                                    # Mark as pending
                                    r = requests.get(GAS_URL, params={
                                        "action": "pending",
                                        "email": EMAIL
                                    })
                                    print(r.json())
                                    break
                                except:
                                    pass
                            break
                        else:
                            submitteds = driver.find_elements(
                                By.XPATH,
                                "//*[@class='tawk-text-regular-2']"
                            )
                            if len(submitteds) > 0:
                                if submitteds[0].text == "Your ticket has been submitted. Thank you!":
                                    print("Form submitted successfully.")
                                    while True:
                                        try:
                                            # Mark as sent
                                            r = requests.get(GAS_URL, params={
                                                "action": "sent",
                                                "email": EMAIL
                                            })
                                            print(r.json())
                                            break
                                        except:
                                            pass
                                    break
                else:
                    print("get email tawk error")
                    while True:
                        try:
                            # Mark as pending
                            r = requests.get(GAS_URL, params={
                                "action": "pending",
                                "email": EMAIL
                            })
                            print(r.json())
                            break
                        except:
                            pass
                    
                            
        except:
            print("get email tawk error")
            while True:
                try:
                    # Mark as pending
                    r = requests.get(GAS_URL, params={
                        "action": "pending",
                        "email": EMAIL
                    })
                    print(r.json())
                    break
                except:
                    pass
                    
        inc = inc + 1
        
    while True:
        if driver is not None:
            try:
                driver.close()
                driver.quit()
                shutil.rmtree(profile_dir, ignore_errors=True)
                break
            except:
                print("driver close error")
        else:
            break
        time.sleep(0.5)
