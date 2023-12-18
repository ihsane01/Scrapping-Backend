import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lib2to3.pgen2 import driver
from time import sleep
from selenium.webdriver.common.by import By
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
current_link = 1
turn_it = True
all_journals = list()
while (turn_it):
    dico_journal = {}
    with open('urls_sc_data-blockchain.json') as data_file:
        data = json.load(data_file)
    for v in data:
        driver = webdriver.Chrome() 
        try:
            driver.get(v)
        except WebDriverException:
            print("page down")
        sleep(4)
        authors = []
        locations = []
        try:
            fullpage = driver.find_element(
                By.CLASS_NAME, 'article-wrapper.u-padding-s-top.grid.row')
        except:
            pass
        try:
            underFullPage = fullpage.find_element(
                By.XPATH, '//article')
        except:
            pass
        try:
            JournalDateSection = underFullPage.find_element(By.XPATH, './div[1]')
        except:
            pass
        try:
            TypeTitleSection = underFullPage.find_element(By.XPATH, './h1[1]')
        except:
            pass
        try:
            AuthorsSection = underFullPage.find_element(By.XPATH, './div[2]')
        except:
            pass
        try:
            DOISection = underFullPage.find_element(By.XPATH, './div[3]')
        except:
            pass
        try:
            AccessSection = underFullPage.find_element(By.CLASS_NAME, 'LicenseInfo')
        except:
            pass
        try:
            AbstractSection = underFullPage.find_element(By.CLASS_NAME, 'Abstracts')
        except:
            pass
        try:
            Publisher = JournalDateSection.find_element(By.XPATH, './div[2]/h2[1]/a[1]').text
        except:
            Publisher = ""
        try:
            Date = JournalDateSection.find_element(By.XPATH, './div[2]/div[1]').text
        except:
            Date = ""
        try:
            Title = TypeTitleSection.find_element(By.XPATH, './span[1]').text
        except:
            Title = ""
        try:
            Type = TypeTitleSection.find_element(By.XPATH, './div[1]').text
        except:
            Type = ""
        Authors = []
        Locations = []
        try:
            AuthorPart = AuthorsSection.find_element(By.XPATH, './div[1]/div[1]/div[1]')
        except:
            pass
        try:
            listauthors = AuthorPart.find_elements(By.XPATH, "./button")
        except:
            listauthors = []
        try:
            for auth in listauthors:
                author = auth.find_element(
                    By.XPATH, './span[1]').text
                Authors.append(author)
        except:
            pass
        try:
            DOI = DOISection.find_element(By.XPATH, "./a[1]").get_attribute('href')
        except:
            DOI = ""
        try:
            Access = AccessSection.find_element(By.XPATH, "./div[2]").text
        except:
            Access = ""
        try:
            Abstract = AbstractSection.find_element(By.XPATH, "./div[1]/div[1]/p[1]").text
        except:
            Abstract = ""
        try:
            for auth in listauthors:
                auth.click()
                sleep(4)
                Location = driver.find_element(By.CLASS_NAME, "affiliation").text
                Locations.append(Location)
                TypeTitleSection.find_element(By.XPATH, './span[1]').click()
        except:
            pass
        dico_journal = {"Title":Title, "Abstract": Abstract, "Type": Type, "Access": Access
                        , "Date": Date, "DOI": DOI, "Publisher": Publisher, "Authors": Authors,"Universities": locations}      
        all_journals.append(dico_journal)
        with open("sciencesDirectes.json", "w") as write_file:  
            json.dump(all_journals, write_file, indent=4)
        print(current_link)
        current_link += 1
    driver.close
    turn_it = False
driver.close()