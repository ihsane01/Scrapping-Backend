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
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
while (turn_it):
    dico_journal = {}
    driver = webdriver.Chrome()
    web_site = "https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=Blockchain&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&pageNumber=" + \
        str(current_page)
    driver.get(web_site)
    sleep(4)
    journals = driver.find_elements(By.CLASS_NAME, 'List-results-items')
    if journals == []:
        turn_it = False
    enf_of_recherche = False
    for index, val in enumerate(journals):
        journals = driver.find_elements(By.CLASS_NAME, 'List-results-items')
        Title = journals[index].find_element(
            By.CSS_SELECTOR, 'h3.result-item-title')
        url = Title.find_element(By.XPATH, './a[1]').get_attribute('href')
        dico_journal = url
        all_journals.append(dico_journal)
    print(current_page)
    driver.close
    if (current_page == 50):
        turn_it = False
    current_page += 1
    if (dico_journal == {}):
        turn_it = False
with open("urls_ieee_data.json", "w") as write_file:
    json.dump(all_journals, write_file, indent=4)
driver.close()
