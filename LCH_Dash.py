from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from datetime import datetime
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("https://global.viaje.ai/blablacar/home/")
driver.maximize_window()


wait = WebDriverWait(driver, 40)

#Login with valid credential

def login():
    login_btn = driver.find_element(By.XPATH, '(//button[@type="submit"])[3]').click()

    wait.until(EC.visibility_of_element_located((By.ID,'username')))
    wait.until(EC.element_to_be_clickable((By.ID,'username')))
    driver.find_element(By.ID,'username').send_keys('chaithali.dube240613@sciative.in')

    wait.until(EC.visibility_of_element_located((By.ID,'password')))
    wait.until(EC.element_to_be_clickable((By.ID,'password')))
    driver.find_element(By.ID,'password').send_keys('#Mumbai21')

    time.sleep(10)
    wait.until(EC.visibility_of_element_located((By.ID,'submit-login-form')))
    wait.until(EC.element_to_be_clickable((By.ID,'submit-login-form'))).click()


#LCH Dashboard avaibility

def lch_dashboard():
    wait.until(EC.visibility_of_element_located((By.XPATH,'(//span[@class="side_bar_text"])[3]')))
    wait.until(EC.element_to_be_clickable((By.XPATH,'(//span[@class="side_bar_text"])[3]'))).click()

    #Check for Default filters and Refresh date and time

    wait.until(EC.visibility_of_element_located((By.XPATH,'//div[@id="refresh_value"]//span')))
    refresh_date = driver.find_element(By.XPATH,'//div[@id="refresh_value"]')

    ref_date =refresh_date.text
    print(f"Full refresh text using JS: {ref_date}")

    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    print(current_date)

    if ref_date == current_date:
        print(f"Ref_date and current date not matched:{current_date}")

    else:
        print("Current date and last refresh date are simillar")


# #Country Avaibility

def LCH_fields_avail():
    wait.until(EC.visibility_of_element_located((By.XPATH,'//ul[@id="country_dd"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH,'//ul[@id="country_dd"]'))).click()
    country = driver.find_elements(By.XPATH,"//select[@id='nav_country']//option")
    print(f"total countries found: {len(country)}\n")
    for option in country:
        print(option.text)


    #Check Calander avaibility
    calendar = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH,"(//button[@class='btn dropdown-toggle btn-light'])[1]")))
    print("By Default Current Date is present")

    # #Check SDK avaibility
    wait.until(EC.visibility_of_element_located((By.XPATH,"//div[8]//div[1]//button[1]//div[1]//div[1]//div[1]")))
    print("By Default All Sources is present")

    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="fixed-header"]/div[2]/div/div[9]/div[1]/button/div/div/div')))
    print("By Default All Destination is present")

    # #Cherck Competitions ava
    wait.until(EC.visibility_of_element_located((By.XPATH,'//div[@id="competition-dropdown"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@id="competition-dropdown"]'))).click()
    competitions = driver.find_elements(By.XPATH,'//div[@id="competition"]//label//input')

    compe = [competition.get_attribute('value') for competition in competitions]
    print(f"Total competition are:{len(compe)}")

    for comp in compe:
        print(comp)

    #Check the competition Type avaibility
    wait.until(EC.visibility_of_element_located((By.XPATH,'//select[@id="select_level"]')))
    comp_type= driver.find_elements(By.XPATH,'//select[@id="select_level"]//option')

    for option in comp_type:
        print("available competition type is :"+ option.text)


    #Check the Highchart avaibility for by default selection

    wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@class='highcharts-series-group']")))
    print("Highchart is available for default selection")

    high = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='current_position_container']/div[2]/div[2]/div[1]/div")))
    high_count = high.text
    high_count_int = int(high_count)
    print("For by default selection, BBC prices higher than Comp: "+ high_count_int)

    competitively = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='current_position_container']/div[2]/div[2]/div[2]/div")))
    comp_count = competitively.text
    comp_count_int = int(comp_count)
    print("For by default selection, BBC prices and Comp price are same: "+str(comp_count_int ))

    low = wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='current_position_container']/div[2]/div[2]/div[3]/div")))
    low_count = low.text
    low_count_int = int(low_count)
    print(type(low_count_int))
    print("For by default selection, BBC prices lower than Comp: "+ str(low_count_int))

    # Check the pichart avaibility

    pichart = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@class="highcharts-series-group"]')))
    print("Pichart is available for default selection")

    #Check the pichart and available count are same or not

    pichart_low = wait.until(EC.visibility_of_element_located((By.XPATH,"(//*[@class='highcharts-text-outline'])[1]")))
    pichart_low_count = pichart_low.text
    pichart_cleaned_count = pichart_low_count.replace('L:','').replace(',','').strip()
    pichart_final_count = int(pichart_cleaned_count)
    print("picart low count is: "+ str(pichart_final_count))

    if pichart_final_count == low_count_int:
        print("Pichart and BBC buses price lower count is same ")
    else:
        print("Pi cahrt and BBC buses count(Low price) not matched to each other")


    pichart_comp = wait.until(EC.visibility_of_element_located((By.XPATH,"(//*[@class='highcharts-text-outline'])[2]")))
    pichart_comp_count = pichart_comp.text
    pichart_comp_cleaned_count = pichart_comp_count.replace('C:','').replace(',','').strip()
    pichart_final_count = int(pichart_comp_cleaned_count)  
    print("pichart comp count is: "+ str(pichart_final_count))

    if pichart_final_count == comp_count_int:
        print("Pichart and BBC buses price competitively count is same ")
    else:
        print("Pi cahrt and BBC buses count(Competitively) not matched to each other")

    pichart_high = wait.until(EC.visibility_of_element_located((By.XPATH,"(//*[@class='highcharts-text-outline'])[3]")))
    pichart_high_count = pichart_high.text
    pichart_high_cleaned_count = pichart_high_count.replace('H:','').replace(',','').strip()
    pichart_Hfinal_count = int(pichart_high_cleaned_count)
    print("pichart High count is: "+ str(pichart_Hfinal_count))

    if pichart_Hfinal_count == high_count_int:
        print("Pichart and BBC buses price higher count is same ")
    else:
        print("Pi cahrt and BBC buses count(High price) not matched to each other")

    high.click()

def card_availability():    
    try:
        while True:
            try:
                download_csv = driver.find_element(By.XPATH,'//button[@id="download-btn-con"]"]')
                
                break
            except:
                driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)   
                time.sleep(1)
                print("Download CSV is available")
        cards = driver.find_elements(By.XPATH, '//div[@id="cards_tbl_tbl"]/div') 
        print("Total Number of cards is: " + str(len(cards))) 

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()




driver.close()

login()
lch_dashboard()
LCH_fields_avail()
card_availability()