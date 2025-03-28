from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse
from datetime import datetime



def is_after_six_pm(time_str):
    decoded_text = urllib.parse.unquote(time_str)
    time_format = "%m/%d/%Y %I:%M %p"
    start_time = datetime.strptime(decoded_text, time_format)
    six_pm = start_time.replace(hour=18, minute=0, second=0, microsecond=0)
    # Check if hour is 6 PM or later
    return start_time > six_pm


# Set up Selenium WebDriver
def book_ball_machine():
    driver = webdriver.Chrome()  # Ensure chromedriver is installed and in PATH

    try:
        # Open the booking website
        driver.get("https://app.courtreserve.com/")
        time.sleep(3)
       
        # Perform login (Modify element locators as needed)
        driver.find_element(By.ID, "Username").send_keys("xxxx")
        driver.find_element(By.ID, "Password").send_keys("xxx", Keys.RETURN)
        time.sleep(5)
        

        # Navigate and book the ball machine (Modify selectors based on website structure)
        # Example: Clicking book button
        book_button = driver.find_element(By.XPATH, "//a[contains(text(),'BOOK A BALL MACHINE')]")
        book_button.click()
        time.sleep(2) 
        
        daycount = 0
        wait = WebDriverWait(driver, 10)
        booked_session = False
        while daycount < 7 and not booked_session :
            reserve_buttons = driver.find_elements(By.XPATH, "//a[contains(@class, 'btn slot-btn') and contains(text(), 'Reserve')]")
            available_after_six = False 

            for button in reserve_buttons:
                # Extract the start time from the data-href attribute
                data_href = button.get_attribute("data-href")
                # Extract the start time from the data-href (time is in the query string as start=4/1/2025 8:30 AM)
                start_time_str = data_href.split("start=")[1].split("&")[0]
                # Convert to a 24-hour format and check if it's after 6:00 PM
                if is_after_six_pm(start_time_str):
                    available_after_six = True
                    button.click()  # Click the reserve button for this slot
                    
                    # Step 2: Agree to the disclosure
                    checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='DisclosureAgree']")))
                    checkbox.click()
                    time.sleep(5)
                    # Step 3: Click the "Save" button to confirm
                    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary btn-submit']")))
                    save_button.click()
                    booked_session= True 
                    time.sleep(5)
                    print("Booking Succesful")
                    break 
            if not available_after_six:
                print("No available evening slots after 6:00 PM. Moving to the next day.")
            
                # Click the "Next" button to move to the next date (navigate to next page)
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='k-button k-button-md k-rounded-md k-button-solid k-button-solid-base k-icon-button k-nav-next']")))
                next_button.click()

                # Wait for the page to load before checking again
                time.sleep(2)  # Adjust sleep time if needed
            daycount += 1
    finally:
        driver.quit()



count = 0 
while True  and count <100:
    book_ball_machine()
    current_time = datetime.now() 
    if current_time.minute >30:
        target_time =  current_time.replace(hour=current_time.hour+1, minute=0, second=0, microsecond=0,day=current_time.day+1)
    else:
        target_time = current_time.replace(hour=current_time.hour, minute=30, second=0, microsecond=0,day=current_time.day)
    time_diff = target_time - current_time
    print(f"Sleeping for {time_diff.total_seconds()} seconds until next hour")
    time.sleep(time_diff.total_seconds())
    # book_ball_machine()
    count += 1
