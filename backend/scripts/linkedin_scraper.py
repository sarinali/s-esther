from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def navigate_to_linkedin_feed():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.linkedin.com/feed/")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys("donuts5.2022@gmail.com")

        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys("scrape123")

        sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn__primary--large.from__button--floating")))
        sign_in_button.click()

        sleep(2)

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])

        search_url = "https://www.linkedin.com/search/results/people/?keywords=daniel%20caesar&origin=CLUSTER_EXPANSION&sid=mDN"
        driver.get(search_url)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        print("Waiting for page to fully load...")
        sleep(5)

        print("Checking for iframes...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(iframes)} iframes")

        for i, iframe in enumerate(iframes):
            print(f"Iframe {i}: id={iframe.get_attribute('id')}, src={iframe.get_attribute('src')}")

        print("Searching for any artdeco-card elements...")
        all_cards = driver.find_elements(By.CSS_SELECTOR, "[class*='artdeco-card']")
        print(f"Found {len(all_cards)} elements with 'artdeco-card' in class")

        print("Searching for any pv0 elements...")
        pv0_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='pv0']")
        print(f"Found {len(pv0_elements)} elements with 'pv0' in class")

        print("Searching in each iframe...")
        for i, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"Switched to iframe {i}")

                iframe_cards = driver.find_elements(By.CSS_SELECTOR, "div.pv0.ph0.mb2.artdeco-card")
                print(f"Found {len(iframe_cards)} target divs in iframe {i}")

                iframe_all_cards = driver.find_elements(By.CSS_SELECTOR, "[class*='artdeco-card']")
                print(f"Found {len(iframe_all_cards)} artdeco-card elements in iframe {i}")

                if iframe_cards:
                    print(f"SUCCESS: Found target divs in iframe {i}!")
                    for j, div in enumerate(iframe_cards):
                        print(f"Iframe {i} - Result div {j}: {div.get_attribute('class')}")

                driver.switch_to.default_content()

            except Exception as iframe_error:
                print(f"Error checking iframe {i}: {iframe_error}")
                driver.switch_to.default_content()

        try:
            result_lis = driver.find_elements(By.CSS_SELECTOR, "li.vdwXPaZqjnOSVBOJRaUGXoYwopOhpiBiuQ")
            print(f"Found {len(result_lis)} target result li elements in main content")

            for index, li in enumerate(result_lis):
                print(f"\n--- Person {index + 1} ---")

                try:
                    name_element = li.find_element(By.CSS_SELECTOR, "a[data-test-app-aware-link] span[dir='ltr'] span[aria-hidden='true']")
                    name = name_element.text.strip()
                    print(f"Name: {name}")
                except:
                    print("Name: Not found")

                try:
                    profile_link_element = li.find_element(By.CSS_SELECTOR, "a[data-test-app-aware-link]")
                    profile_link = profile_link_element.get_attribute("href")
                    print(f"Profile Link: {profile_link}")
                except:
                    print("Profile Link: Not found")

                try:
                    job_title_element = li.find_element(By.CSS_SELECTOR, "div.xRJOgrQuFzciyRxKOIOwvaYwLREkZzCCxtQk")
                    job_title = job_title_element.text.strip()
                    print(f"Job Title: {job_title}")
                except:
                    print("Job Title: Not found")

                try:
                    location_element = li.find_element(By.CSS_SELECTOR, "div.JcoRZcgVWQelOtLJFmykrzjWASePpwDbmoyVM")
                    location = location_element.text.strip()
                    print(f"Location: {location}")
                except:
                    print("Location: Not found")

                try:
                    img_element = li.find_element(By.CSS_SELECTOR, "img.presence-entity__image")
                    img_src = img_element.get_attribute("src")
                    img_alt = img_element.get_attribute("alt")
                    print(f"Profile Image: {img_src}")
                    print(f"Image Alt Text: {img_alt}")
                except:
                    print("Profile Image: Not found")

        except Exception as li_error:
            print(f"Could not find result li elements: {li_error}")


        print(f"Successfully navigated to: {driver.current_url}")
        print(f"Page title: {driver.title}")

    except Exception as e:
        print(f"Error navigating to LinkedIn feed: {e}")

    finally:
        sleep(1000)
        # driver.quit()

if __name__ == "__main__":
    navigate_to_linkedin_feed()