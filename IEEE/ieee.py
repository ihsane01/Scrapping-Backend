from lib2to3.pgen2 import driver
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import json
import re
from dateutil.parser import parse
from time import strptime


def filter_journals():
    try:
        journal_input_div_object = driver.find_element(
            By.ID, "refinement-ContentType:Journals")
        driver.execute_script(
            "arguments[0].click();", journal_input_div_object)
        sleep(1)
    except:
        print("canot filter journals")

# getting authors


def get_author():
    try:
        authors = journal.find_element(
            By.CSS_SELECTOR, 'xpl-authors-name-list').text
        list_auths = authors.split(';\n')
    except:
        list_auths = ""
        print("Authors not found")
    return list_auths

# getting title


def get_title():
    try:
        tile_object = journal.find_element(By.CSS_SELECTOR, 'h3')
        title = tile_object.text
    except:
        title = ""
        print("title not found")
    return title

# getting publication info (year type publisher)


def get_journal_info():
    try:
        pub_info = journal.find_element(
            By.CSS_SELECTOR, 'div.publisher-info-container')
        year = pub_info.find_element(By.XPATH, './span[1]').text
        year = year.replace('Year: ', '')

        type = pub_info.find_element(By.XPATH, './span[2]').text
        type = type.lstrip("|")

        publisher = pub_info.find_element(By.XPATH, './span[3]').text
        # formating publisher
        publisher = publisher.lstrip('|')
        publisher = publisher.replace(' Publisher: ', '')
    except:
        print("info not nound")
        publisher = ""
        type = ""
        year = ""

    return publisher, type, year


# getting journal link
def get_journal_link():
    try:
        tile_object = journal.find_element(By.CSS_SELECTOR, 'h3')
        titleToclick = tile_object.find_element(By.CSS_SELECTOR, 'a')
        journal_link = titleToclick.get_attribute("href")
    except:
        print("journal link not found")
        journal_link = ""
    return journal_link

# click event on the journal


def click_journal():
    # Cliking the link
    try:
        tile_object = journal.find_element(By.CSS_SELECTOR, 'h3')
        titleToclick = tile_object.find_element(By.CSS_SELECTOR, 'a')
        ActionChains(driver).move_to_element(titleToclick).perform()
        titleToclick.click()
        sleep(1)
    except:
        print("Nothing to clik")

# getting abstract


def get_abstract():
    try:
        absract_div = driver.find_element(
            By.CLASS_NAME, "row.document-main-body")
        abstract_div2 = absract_div.find_element(By.CLASS_NAME, "u-mb-1")
        abstract_text = abstract_div2.find_element(By.XPATH, "./div[1]").text
    except:
        abstract_text = ""
        print("abstract not found")

    return abstract_text

# getting date from publication


def get_date():
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    try:
        global date, day, month, num_month
        date_txt = driver.find_element(
            By.CLASS_NAME, "u-pb-1.doc-abstract-confdate").text
        formated_date = date_txt.split("-")[1]
        global date
        date = formated_date.split(" ")
        global day, month, year
        day = date[0]
        month = date[1]
        year = date[2]
        # convert month of the year to number
        num_month = months.index(month) + 1
    except:
        print("No Date found")
        formated_date = ""
        day = ""
        month = ""
        year = ""
    return date, day, month, num_month

# getting the conference location


def get_locations():
    sleep(0.5)
    all_univ = list()
    all_countries = list()
    all_locations = list()
    try:
        authors_div = driver.find_element(
            By.ID, "authors")
        ActionChains(driver).move_to_element(authors_div).perform()
        authors_div.click()
        authors = driver.find_elements(
            By.CLASS_NAME, "authors-accordion-container")
        for auth in authors:
            all_locations.append(auth.text.split('\n')[1])
            all_countries.append(auth.text.split('\n')[1].split(',').pop())

        driver.back()

    except:
        all_countries = ""
        all_locations = ""
        print("elements not found")
    return all_countries, all_locations

# getting the references from the dropdown


def write_scraped_data_json(file_location: str):
    with open(file_location, "w") as write_file:
        # convert the list into a json file
        json.dump(all_journals, write_file, indent=4)

# event to click coockies
# accepting cookies to destroy the overlay


def get_published_in():
    try:
        # deleting elm between ()
        pb_in = driver.find_element(
            By.CLASS_NAME, "u-pb-1.stats-document-abstract-publishedIn")
        pbi = pb_in.find_element(By.XPATH, "./a[1]").text
        text = re.sub(r'\([^\)]*\)', '', pbi)
    except:
        print("no pub found")
        text = ""
    return text


def accept_cookies():
    cookies_btn = driver.find_element(By.CLASS_NAME, "cc-btn.cc-dismiss")
    driver.execute_script("arguments[0].click();", cookies_btn)


current_page = 1
PATH = "C:\Program Files (x86)\chromedriver.exe"
turn_it = True
all_journals = list()
while(turn_it):
    dico_journal = {}
    driver = webdriver.Chrome(PATH)
    web_site = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=blockchains&pageNumber=" + \
        str(current_page)
    driver.get(web_site)
    sleep(1)
    filter_journals()
    journals = driver.find_elements(By.CLASS_NAME, "List-results-items")

    enf_of_recherche = False
    next_page = 2

    accept_cookies()

    for journal in journals:

        authors_tmp = get_author()
        title_tmp = get_title()
        publisher_tmp, type_tmp, year_tmp = get_journal_info()
        journal_link_tmp = get_journal_link()
        # click journal
        click_journal()
        pub_tmp = get_published_in()
        all_countries_tmp, all_locations_tmp = get_locations()
        abstract_tmp = get_abstract()
        date_tmp, day_tmp, month_name_tmp, num_month_tmp = get_date()

        # go back to the privious page
        driver.back()

        dico_journal = {"Title": title_tmp, "Abstract": abstract_tmp, "Type": type_tmp,
                        "Date": date_tmp, "Year": year_tmp, "Month": num_month_tmp, "MonthName": month_name_tmp, "Day": day_tmp, "DOI": journal_link_tmp, "Publisher": pub_tmp, "Authors": authors_tmp, "Universities": all_locations_tmp, "Countries": all_countries_tmp}

        # debuging purposes
        print(dico_journal)

        # this list contains all our data
        all_journals.append(dico_journal)

    print("current page", current_page)

    driver.close()

    current_page += 1

    if(dico_journal == {} or current_page == 15):
        turn_it = False

write_scraped_data_json("ieee_data.json")

# driver.close()
