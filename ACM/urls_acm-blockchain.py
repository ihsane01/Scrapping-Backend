from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lib2to3.pgen2 import driver
from time import sleep
from selenium.webdriver.common.by import By
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions


current_page = 0
turn_it = True
all_journals = list()

chrome_options = Options()
chrome_options.add_argument('--headless')

while (turn_it):
    dico_journal = {}
    driver = webdriver.Chrome()
    
    web_site = "https://dl.acm.org/action/doSearch?AllField=Blockchain&expand=all&ConceptID=118230&startPage=" + \
        str(current_page)+"&pageSize=100"
    
   
    driver.get(web_site)
    sleep(4)

    journals = driver.find_elements(By.CLASS_NAME, 'issue-item__title')

    if journals == []:
        turn_it = False

    enf_of_recherche = False

    for index, val in enumerate(journals):
        journals = driver.find_elements(By.CLASS_NAME, 'issue-item__title')
        Title = journals[index].find_element(
            By.CSS_SELECTOR, 'span.hlFld-Title')
        url = Title.find_element(By.XPATH, './a[1]').get_attribute('href')

        dico_journal = url

        all_journals.append(dico_journal)

    print(current_page)

    driver.close

    current_page += 1

    if (dico_journal == {}):
        turn_it = False


with open("urls_acm_data-blockchain.json", "w") as write_file:
    json.dump(all_journals, write_file, indent=4)

driver.close()
