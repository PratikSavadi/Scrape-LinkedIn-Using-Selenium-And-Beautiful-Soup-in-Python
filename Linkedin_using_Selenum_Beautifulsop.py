import os.path
import pandas as pd
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

"""
        *************************MANDATORY ARGUMENTS REQUIRED*********************************
        Chrome Driver Path
        Linkedin Username and Password
        Name to search in linkedIn search bar   
"""

LINKEDIN_URL="https://linkedin.com/uas/login"
USERNAME= "username"
PASSWORD= "password"

def open_linkedIn_page(driver):
    """
    In this method  instance will be used to log into LinkedIn
    """

    # Opening linkedIn's login page
    response = requests.get(LINKEDIN_URL)
    # checks the status code of URL
    if response.status_code == 200:
        return driver.get(LINKEDIN_URL)
        # waiting for the page to load
        time.sleep(5)
        driver.maximize_window() # For maximizing window
        # driver.implicitly_wait(10) # gives an implicit wait for 20 seconds
    else:
        print("URL Could not open.Please check the URL.")
        return None

def login_to_linkedIn(driver,EMAIL_ID_KEY,PASSWORD_KEY):
    """
    This method is used to sign in the linkedin by using username and password
    """
    try:
        # find the username key from html page
        username = driver.find_element(By.ID,USERNAME )
        # enters the email address
        username.send_keys(EMAIL_ID_KEY)
        # find the password key from html page
        pword = driver.find_element(By.ID,PASSWORD )
        # eneters the password
        pword.send_keys(PASSWORD_KEY)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
    except Exception as e:
        print('Please Enter the valid credentials :')
    return

start = time.time()

def  search_name_in_searchbar(driver,Name):
    """
    In this method the cursor goes to search bar and place name in search bar and finds the
     10 names
    """
    # find key search from html page and goes to the search bar
    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))).click()
    # enters the name in search bar
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))).send_keys(Name)
    # after entring the name presses the enter or click then finds the names
    WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH,"//span[@class='search-global-typeahead-hit__text t-16 t-black']"))).click()
    # this will go to the people tab on linkedin page where all the 10 names will be there
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='People']"))).click()

def get_detailed_info(driver):
    """
    In this method all the detailes of specific person will be taken and written to the csv
    """
    # we will stop the script for 3 seconds so that
    # the data can load
    time.sleep(5)
    # reads details of the page
    src = driver.page_source
    driver.implicitly_wait(150)
    # Now using beautiful soup to convert to readable format
    soup = BeautifulSoup(src, 'lxml')
    driver.implicitly_wait(150)
    time.sleep(2)
    # Extracting the HTML of the complete introduction box
    # that contains the name,work/student, and the location
    location =soup.find_all('div',{'class':'entity-result__secondary-subtitle t-14 t-normal'})
    works_student =soup.find_all('div',{'class':'entity-result__primary-subtitle t-14 t-black t-normal'})
    people_name=soup.find_all("span", dir="ltr")

    all_people_name,all_works_student,all_location_list=([],[],[])

    # looping
    for loc,wok,name in zip(location,works_student,people_name):
        all_location_list.append(loc.get_text(strip=True))
        all_works_student.append(wok.get_text(strip=True))
        all_people_name.append(name.find_next("span").text)

    # converting to the data frame
    detailed_data = pd.DataFrame(
        {'Name': all_people_name,
         'Work/Student': all_works_student,
         'Location': all_location_list
        })
    path_to_csv='C:/Users/LAPPY HUB/Downloads'
    if os.path.exists(path_to_csv):
        print('The Detailed_Data.csv file is written in the path'+str(path_to_csv) )
        print ('Total Rows in data :'+str(len(detailed_data)))
        detailed_data.to_csv(path_to_csv+'/'+'Detailed_Data.csv',index=False)

def execute(CHROME_DRIVER_PATH,EMAIL_ID_KEY,PASSWORD_KEY,Name):
    """
        *************************MANDATORY ARGUMENTS REQUIRED*********************************
        Chrome Driver Path
        Linkedin Username and Password
        Name to search in linkedIn search bar
    """
       
    # checks if the chrome driver path exists
    if not os.path.exists(CHROME_DRIVER_PATH):
        print('Executable file could not found in specified path')

    # from webdriver_manager.chrome import ChromeDriverManager
    # Creating a webdriver instance
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)

    # this method opens the linkedIn page
    open_linkedIn_page(driver)
    # this method enters the username and password on  linkedIn page and sign in to the  linkedIn
    login_to_linkedIn(driver,EMAIL_ID_KEY,PASSWORD_KEY)
    # this method find the name in search bar
    search_name_in_searchbar(driver,Name)
    # this method gets the detailed of first 10 people from the page
    get_detailed_info(driver)

    return

CHROME_DRIVER_PATH=input('Please Enter the chrome driver path : ')
EMAIL_ID_KEY=input('Please Enter Username/Email_Id :')
PASSWORD_KEY=input('Please Enter Password :')
Name = input('Please Enter Name to search :')
execute(CHROME_DRIVER_PATH,EMAIL_ID_KEY,PASSWORD_KEY,Name)
