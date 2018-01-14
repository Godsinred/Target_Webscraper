from bs4 import BeautifulSoup
import requests
from selenium import webdriver

def main():

    # r = requests.get("https://www.target.com")
    # soup = BeautifulSoup(r.content, "lxml")
    #
    # soup = soup.find("div", id="nav")
    # print(soup)
    #/ Users // godsinred // Desktop // TestrApplication - master // ApplicationFiles // Resources // Star1.png

    driver_location = "//Applications//Python 3.6//chromedriver.exe"

    driver = webdriver.Chrome()  # replace with .Firefox(), or with the browser of your choice
    url = "http://google.com"
    driver.get(url)  # navigate to the page
    print(driver)

    driver.quit()

    # for items in categories.find_all("li", class_="navigation--link"):
    #     item = items.find('a')
    #     print(item.text + ": https://www.target.com" + item.get("href"))


    # to make a Post request
    # r = requests.post('http://httpbin.org/post', data = {'key':'value'})
    

if __name__ == "__main__":
    main()
