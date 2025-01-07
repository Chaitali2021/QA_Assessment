from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import random
import re
import pandas as pd

# Initialize the Chrome driver with options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open the target URL
driver.get("https://global.viaje.ai/blablacar/home/")
driver.maximize_window()

# WebDriverWait instance
wait = WebDriverWait(driver, 40)

# Login function with valid credentials
def login():
    try:
        # Click on login button
        login_btn = driver.find_element(By.XPATH, '(//button[@type="submit"])[3]').click()

        # Enter username
        wait.until(EC.visibility_of_element_located((By.ID, 'username')))
        driver.find_element(By.ID, 'username').send_keys('chaithali.dube240613@sciative.in')

        # Enter password
        wait.until(EC.visibility_of_element_located((By.ID, 'password')))
        driver.find_element(By.ID, 'password').send_keys('#Mumbai21')

        # Submit the login form
        wait.until(EC.element_to_be_clickable((By.ID, 'submit-login-form'))).click()
        print("Login successful.")
    except Exception as e:
        print(f"An error occurred during login: {e}")

# LCH Dashboard availability
def lch_dashboard():
    try:
        # Navigate to LCH Dashboard
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//span[@class="side_bar_text"])[3]'))).click()

        # Check refresh date
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="refresh_value"]//span')))
        refresh_date = driver.find_element(By.XPATH, '//div[@id="refresh_value"]')

        ref_date = refresh_date.text.strip()
        current_date = datetime.utcnow().strftime('%Y-%m-%d')

        if ref_date != current_date:
            print(f"Refresh date and current date do not match: {ref_date} != {current_date}")
        else:
            print("Refresh date matches the current date.")
    except Exception as e:
        print(f"An error occurred in LCH Dashboard: {e}")

# LCH Fields availability
def LCH_fields_avail():
    try:
        # Check Country dropdown availability
        wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[@id="country_dd"]'))).click()
        countries = driver.find_elements(By.XPATH, "//select[@id='nav_country']//option")
        print(f"Total countries found: {len(countries)}")
        for country in countries:
            print(country.text)

        # Check Calendar availability
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//button[@class='btn dropdown-toggle btn-light'])[1]")))
        print("Calendar is available with the current date.")

        # Check Source and Destination availability
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[8]//div[1]//button[1]//div[1]//div[1]//div[1]")))
        print("All Sources is available.")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fixed-header"]/div[2]/div/div[9]/div[1]/button/div/div/div')))
        print("All Destination is available.")

        # Check Competition availability
        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="competition-dropdown"]'))).click()
        competitions = driver.find_elements(By.XPATH, '//div[@id="competition"]//label//input')
        print(f"Total competitions: {len(competitions)}")
        for competition in competitions:
            print(competition.get_attribute('value'))

        # Check Competition Type availability
        comp_types = driver.find_elements(By.XPATH, '//select[@id="select_level"]//option')
        print("Available competition types:")
        for comp_type in comp_types:
            print(comp_type.text)

        # Check Highchart availability
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='highcharts-series-group']")))
        print("Highchart is available for default selection.")

        # Validate counts from highcharts
        # Add your count validation code here

    except Exception as e:
        print(f"An error occurred in LCH Fields: {e}")

# Card Availability
def card_availability():
   high = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="pie-insight-line high"][1]')))
   high.click()
   print("High filter applied.")
   cards = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="shadow p-2 bg-white rounded main_row"]')))
   print(f"Total Number of cards: {len(cards)}")
   driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)   
   time.sleep(1)
   
def collect_data(driver):
    products_list = []

    cards = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="shadow p-2 bg-white rounded main_row"]')))
    print(f"Total Number of cards: {len(cards)}")
    # take any 2 random cards and print data
    random_cards = random.sample(cards, 2)
    print(f"Random cards: {len(random_cards)}")
    for card_index, card in enumerate(random_cards, start=1):

        left_card = card.find_element(By.XPATH, '//div[@class="shadow p-2 bg-white rounded main_row"]//div')
        driver.execute_script("arguments[0].scrollIntoView();", left_card)
        try:

            axis = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@title="Source - Destination"])[{card_index}]')))
            axis_text = axis.text
            print(f"Axis Name: {axis_text}")
        
        except :
            print("ID not found")   
        
        carrier = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@title="Carrier"])[{card_index}]'))).get_attribute('textContent')
        print(f"Carrier Name: {carrier}")

        seat_class = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f"(//*[@title='Seat Class'])[{card_index}]"))).get_attribute('textContent')
        print(f"Seat Class: {seat_class}")

        Dapt_arv_time = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@title="Departure Time | Arrival Time "])[{card_index}]'))).get_attribute('textContent')
        print(f"DA|AT: {Dapt_arv_time}")

        time.sleep(1)

        journy_type = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@title="Journey Type"])[{card_index}]'))).get_attribute('textContent')   
        print(f"Journy Type: {journy_type}")

        depature_date = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@title="Date of Departure"])[{card_index}]'))).get_attribute('textContent')
        print(f"Depature Date: {depature_date}")


        for OTA_index, OTA in enumerate(random_cards, start=1):

                rigth_card = OTA.find_element(By.XPATH, '//div[@class="shadow p-2 bg-white rounded main_row"]//div')
                driver.execute_script("arguments[0].scrollIntoView();", rigth_card)
                try:
                    BBC = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"(//a[@href='https://www.blablacar.com.br/search?fn=Itapeva&tn=São Paulo&db=2025-01-06&seats=1&transport_type=bus'])[{OTA_index}]")))
                    BBC.click()
                    # print("BBC link is clicked")
                    driver.switch_to.window(driver.window_handles[0])
                    # Switch to the latest window
                except :
                    print("Hyper Link not found")

                current_prc_and_dis = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@class="odd"])[{OTA_index}]//td[2]/div')))
                current_prc_and_dis_text = current_prc_and_dis.text
                print(f"Current price and discount: {current_prc_and_dis_text}")
                    
                last_dow_range = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@class="odd"])[{OTA_index}]//td[3]/div')))
                last_dow_range_text = last_dow_range.text
                print(f"Last DOW Price range: {last_dow_range_text}")


                last_dow_dic_range = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@class="odd"])[{OTA_index}]//td[4]/div')))
                last_dow_dic_range_text = last_dow_dic_range.text
                print(f"Last DOW Discount range: {last_dow_dic_range_text}")

                available_seats = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@class="odd"])[{OTA_index}]//td[5]/div')))
                available_seats_text = available_seats.text
                print(f"Available Seats are: {available_seats_text}")

                seat_count_match = re.search(r'\d+', available_seats_text)
                if seat_count_match:
                    seat_count = int(seat_count_match.group())  # Convert extracted number to an integer
                    print(f"Available Seats (numeric): {seat_count}")
                else:
                    raise ValueError(f"No numeric value found in seat count text: '{available_seats_text}'")

                try:
                    bus_available = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f'(//*[@class="odd"])[{OTA_index}]//td[6]/div')))

                    if seat_count > 0:
                     bus_available = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '(//*[@class="fa-solid fa-circle-check text-success"])')))

                     print(f"Bus is available with {seat_count} seat(s). Status: is Active")
                    else:
                        bus_available = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@class="fa-solid fa-circle-xmark text-danger"]')))
                        print(f"Bus is not available. Status is Inactive")

                except Exception as e:
                        print(f"An error occurred while checking bus availability: {e}")


        
     
            





# Execute the functions
try:
    login()
    lch_dashboard()
    LCH_fields_avail()
    card_availability()
    collect_data(driver)
finally:
    driver.quit()
