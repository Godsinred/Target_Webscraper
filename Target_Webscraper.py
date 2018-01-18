"""
Jonathan Ishii

Projecct - Target_Webscraper

The purpose of this project is to learn how to webscrape using selenium,
as well as learning how to gather and store data.
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# how to install chromedriver
# https://www.youtube.com/watch?v=dz59GsdvUF8

def get_sub_categories(hyperlink):
    """
    The purpose of this is to get all the sub categories and its corresponding links
    :param hyperlink: the hyperlink of the main category
    :return: a dictionary of sub category names and its hyperlinks as its value
    """

    # initiates the webdriver
    driver = webdriver.Chrome()
    # opens the browser
    driver.get(hyperlink)

    # setting up the waits
    DELAY = 10
    driver.implicitly_wait(DELAY)
    wait = WebDriverWait(driver, DELAY)

    wait.until(EC.visibility_of_all_elements_located((By.XPATH, """//*[@id="js-plp-page-title"]""")))
    wait.until(EC.visibility_of_all_elements_located((By.XPATH, """// *[ @ id = "main"]""")))
    wait.until(EC.visibility_of_all_elements_located((By.XPATH, """// *[ @ id = "home"]""")))

    # gets all the sub categories and its hyperlinks
    try:
        try:
            title = driver.find_element_by_xpath("""//*[@id="js-plp-page-title"]""")
            print(title.text)

            category_list = driver.find_elements_by_class_name("categories")

        except:
            print("Error: Unable to find categories.")
            category_list = {}

        sub_categories = {}
        for category in category_list:
            cats = category.find_elements_by_tag_name('a')

            for c in cats:
                link = c.get_attribute("href")
                name = c.text
                sub_categories[name] = link

    except:
        print("Error: Unable to get sub categories.")

    finally:
        driver.quit()

    return sub_categories

def main():

    # created selenium object
    driver = webdriver.Chrome()  # replace with .Firefox(), or with the browser of your choice
    url = "https://www.target.com/"

    # tells the driver to wait up to 10 seconds before timing out
    # for data that will be loaded on the screen
    DELAY = 10
    driver.implicitly_wait(DELAY)
    wait = WebDriverWait(driver, DELAY)

    # navigate to the page
    driver.get(url)

    try:
        # opens up the side bar javascript
        wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="js-toggleLeftNav"]""")))
        button = driver.find_element_by_xpath("""//*[@id="js-toggleLeftNav"]""")
        button.click()

        # clicks on browse by category
        wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="5"]""")))
        button = driver.find_element_by_xpath("""//*[@id="5"]""")
        button.click()

        # gets all the category elements
        wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="leftNavigation"]/ul[2]""")))
        items = driver.find_element_by_xpath("""//*[@id="leftNavigation"]/ul[2]""").find_elements_by_tag_name("li")


        # gets the hyperlink and category name but the first and the last,
        # since the first is back to main menu and the last is exit
        category_links = {}
        for i in range(1, len(items) - 1):
            hyperlink = items[i].find_element_by_tag_name('a').get_attribute('href')
            category_name = items[i].text
            sub_categories = get_sub_categories(hyperlink)
            # makes a dictionary of dictionary
            # main category being the first key and the second dictionary will have a key of sub category name
            #  with the hyperlink to it
            category_links[category_name] = sub_categories

        print(category_links)

    except TimeoutException:
        print("Loading took too long.")

    time.sleep(30)

if __name__ == "__main__":
    main()
