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

def print_category_links(category_links):
    """
    Prints all the category and its links
    :param category_links: a dictionary of dictionary of the categories and the links
    :return: nothing
    """

    for main_cat, sub_cat in category_links.items():
        print(main_cat)
        #sub cat name and hypterlink
        for key, value in sub_cat.items():
            print(key + ": " + value)

def print_item_list(item_list):
    

def get_sub_categories(hyperlink):
    """
    The purpose of this is to get all the sub categories and its corresponding links
    :param hyperlink: the hyperlink of the main category
    :return: a dictionary of sub category names and its hyperlinks as its value
    """

    # configure chrome options
    options = webdriver.ChromeOptions()
    # tells the browser to be headless
    options.add_argument("headless")
    # set the window size
    options.add_argument('window-size=1200x600')

    # initiates the webdriver
    driver = webdriver.Chrome(chrome_options=options)
    # opens the browser
    driver.get(hyperlink)

    # setting up the waits
    DELAY = 10
    driver.implicitly_wait(DELAY)
    wait = WebDriverWait(driver, DELAY)

    #time.sleep(10)

    # try:
    #     wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="header"]/nav[1]/a[1]""")))
    # except:
    #     print("No return home page button.")
    #
    # try:
    #     wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="js-toggleLeftNav"]""")))
    # except:
    #     print("No navigation page button.")
    #
    # try:
    #     wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="js-toggleLeftNav"]""")))
    # except:
    #     print("No browseByCategory.")
    #
    # try:
    #     wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "categories")))
    # except:
    #     print("No categories.")


    # gets all the sub categories and its hyperlinks
    try:
        try:
            # wait.until(EC.text_to_be_present_in_element((By.XPATH, """//*[@id="js-plp-page-title"]""")))
            # title = driver.find_element_by_xpath("""//*[@id="js-plp-page-title"]""")
            # print(title.text)

            wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="header"]/nav[1]/a[1]""")))
            wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="js-toggleLeftNav"]""")))
            wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "js-browseByCategory")))

            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "categories")))
            wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "categories")))

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

def get_items(main_cat, key, hyperlink, item_list):
    '''

    :param main_cat: the main category to be saved
    :param key: the sub category to be saved
    :param hyperlink: the hyperlink of the subcategory to get all the items from
    :param item_list: all the items that target has on their site
    :return:
    '''
    # configure chrome options
    options = webdriver.ChromeOptions()
    # tells the browser to be headless
    options.add_argument("headless")
    # set the window size
    options.add_argument('window-size=1200x600')

    # initiates the webdriver
    driver = webdriver.Chrome(chrome_options=options)
    # opens the browser
    driver.get(hyperlink)

    # setting up the waits
    DELAY = 10
    driver.implicitly_wait(DELAY)
    wait = WebDriverWait(driver, DELAY)

    # CODE HERE <<<<<<<<<<<<<<<<------------------------------------
    wait.until(EC.element_to_be_clickable(By.XPATH, """//*[@id="plp"]/section/div[2]/div/ul"""))
    wait.until(EC.visibility_of_all_elements_located(By.CLASS_NAME, "product"))

    items = driver.find_element_by_xpath("""//*[@id="plp"]/section/div[2]/div/ul""")

    for item in items:
        # data-ids are 8digit numbers
        id = item.get_attribute("data-id")
        # could be a range of prices or on sale
        price = item.find_element_by_class_name("price").text
        # title of the item
        name = item.find_element_by_class_name("truncated-title").text

        # dictionary -> of list of list with float a
        item_list[id] = [[main_cat, key], name, price]


def main():

    # # configure chrome options
    # options = webdriver.ChromeOptions()
    # # tells the browser to be headless
    # options.add_argument("headless")
    # # set the window size
    # options.add_argument("window-size=1200x600")
    # driver = webdriver.Chrome(chrome_options=options)

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

    category_links = {}
    try:
        # driver.save_screenshot("screenshot.png")
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

        for i in range(1, len(items) - 1):
            hyperlink = items[i].find_element_by_tag_name('a').get_attribute('href')
            category_name = items[i].text
            if(category_name != "Target Finds"):
                sub_categories = get_sub_categories(hyperlink)
                # makes a dictionary of dictionary
                # main category being the first key and the second dictionary will have a key of sub category name
                #  with the hyperlink to it
                category_links[category_name] = sub_categories

        # print all the categories with the sub cats and hyperlinks
        print_category_links(category_links)

    except TimeoutException:
        print("Loading took too long.")

    finally:
        driver.quit()

    # gets all the items from targets site
    item_list = {}
    for main_cat, sub_cat in category_links.items():
        for key, value in sub_cat.items():
            get_items(main_cat, key, value, item_list)

    #

if __name__ == "__main__":
    main()
