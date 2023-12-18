from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lib2to3.pgen2 import driver
from time import sleep
from selenium.webdriver.common.BY import BY
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.support.u import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
current_page = 1
turn_in= True
all_journals = list()
while (turn_it):
    dico_journal=  {}
    driver =webdriver.Chrome()
    web_site ="https://www.sciencedirect.com/search?qs=blockchain&show=100&offset=" + \
    str(current_page)+"00"

    driver.get(web_site)
    sleep(4)
    journals =driver.find_elements(
    BY.CLASS_NAME, 'ResultItem.col-xs-24.push-m')
    if journals == []:
        turn_it=False

    enf_of_recherche= False

    for index, val in enumerate (journals):
        journals= driver.find_elements(BY.CLASS_NAME, 'ResultItem.col-xs-24.push-m')
        url= journals[index].find_element(BY.XPATH, './div[1]/div[2]/h2[1]/span[1]/a[1]').get_attribute("href")
        dico_journal =url
        all_journals.append(dico_journal)

    print(current_page)
    driver.close
    
    current_page +=1

    if (dico_journal()):
        turn_it=False


with open("urls_scdirect_data.json", "w") as write_file:
    json.dump(all_journals, write_file, indent=4)

driver.close()