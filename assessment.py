
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome driver with options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open the target URL
driver.get("https://gor-pathology.web.app/")
driver.maximize_window()

wait = WebDriverWait(driver, 40)

def login():
    try:
        # Check the Username field availability
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@name="email"]')))
        driver.find_element(By.XPATH, '//*[@name="email"]').send_keys('test@kennect.io')

        # Check the Password field availability
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@name="password"]')))
        driver.find_element(By.XPATH, '//*[@name="password"]').send_keys('Qwerty@1234')

        # Submit the login form
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]'))).click()
        print("Login successful.")
           

    except Exception as e:
        print(f"An error occurred during login: {e}")    

def invalid_login():

    #Check Login Functionality with Invalid Credentials
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@name="email"]')))

        #Clear the email and password fields
        driver.find_element(By.XPATH, '//*[@name="email"]').clear()
        driver.find_element(By.XPATH, '//*[@name="email"]').send_keys('chaitalidube21@gmail.com')

        driver.find_element(By.XPATH, '//*[@name="password"]').clear()
        driver.find_element(By.XPATH, '//*[@name="password"]').send_keys('Qw678erty@1234')

        driver.find_element(By.XPATH, '//*[@type="submit"]').click()
        time.sleep(10)
        
        # Check for the error message
        error_msg = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@class="MuiAlert-message"]'))
        )
        
        # Check if the error message is displayed for invalid credentials
        if error_msg.is_displayed():
            print("Test Passed: Error message displayed for invalid credentials.", {error_msg.text})
        else:
            print("Test Failed: User successfully logged in with invalid credentials.")


login()
invalid_login()
driver.close()