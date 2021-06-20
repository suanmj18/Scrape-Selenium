from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode

def getdata(driver,bhk):

    #loading azax dynamic pages
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height: break
            last_height = new_height
    except:
        print("Can't load the dynamic page")
        return driver
    time.sleep(5)
    #another way to load azax dynamic pages
    # c=10
    # while(c):
    #     html = driver.find_element_by_tag_name('html')
    #     html.send_keys(Keys.END)
    #     time.sleep(10)
    #     c-=1

    #extracting data from the page
    try: all=driver.find_elements_by_xpath("//div[@class='filter-property-list detailurl']")
    except: all=[]

    data=[] #to store all the data
    for element in all:
        item={} #contains all the data which are scraped
        
        try:
            location=element.find_element_by_xpath(".//div[@class='col-8']/h1[@class='filter-pro-heading']").text.split("\n")
            item['BHK'],item['Address']=unidecode(location[0][:location[0].index("Apartment")+10]),unidecode(location[1])
        except: item['BHK'], item['Address']="",""

        try: item['Price']=unidecode(element.find_element_by_xpath(".//div[@class='property-price']").text)
        except: item['Price']=""

        try: item['Area']=unidecode(element.find_element_by_xpath(".//div[@class='row filter-pro-details']/div[@class='col-4']").text.split("\n")[1])
        except: item['Area']=""

        try: item['Facing']=unidecode(element.find_element_by_xpath(".//div[@class='row filter-pro-details']/div[@class='col-3']").text.split("\n")[1])
        except: item['Facing']=""

        try: item['Status']=unidecode(element.find_element_by_xpath(".//div[@class='row filter-pro-details']/div[@class='col-5']").text.split("\n")[1])
        except: item['Status']=""

        try: item['Details']=unidecode(element.find_element_by_xpath(".//ul[@class='pro-list']").text.replace("\n",", "))
        except: item['Details']=""
        # details=details.replace("\n",", ")
        try: item['Owner_Name']=unidecode(element.find_element_by_xpath(".//div[@class='filter-property-owner']/div[@class='contact-details']/span[@class='owner-name']").text)
        except: item['Owner_Name']=""

        try: item['Posted']=unidecode(element.find_element_by_xpath(".//div[@class='filter-property-owner']/div[@class='contact-details']/span[@class='owner-post']").text.split(":")[1])
        except: item['Posted']=""

        data.append(item)
        # print(item)

    #exporting scraped data to csv file through pandas module
    csv_data = pd.DataFrame(data)
    csv_data.to_csv('data_{}.csv'.format(bhk), index=False)

    return driver

if __name__=='__main__':
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 1}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

        driver = webdriver.Chrome(executable_path="C:\drivers\chromedriver_win32\chromedriver.exe")
        try:
            driver.get('https://www.propertiesguru.com/residential-search/2bhk-residential_apartment_flat-for-sale-in-new_delhi')
            time.sleep(2)
        except:
            print("Unable to load the page")
            exit(1)

        driver=getdata(driver,"2-bhk") #calling the function to get the data of all the 2-bhk
        time.sleep(2)

        try:
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME) #going on top of the page
            driver.refresh() #refresh the page
            time.sleep(2)

            driver.find_element_by_xpath("//a[@class='nav-link dropdown-toggle bd']").click() #checking the check-boxes
            button=driver.find_element_by_xpath("//ul[@class='property-type room-no pull-right']/li[3]/input")
            driver.implicitly_wait(5) #waiting for the path to load
            ActionChains(driver).move_to_element(button).click(button).perform()

            button=driver.find_element_by_xpath("//ul[@class='property-type room-no pull-right']/li[4]/input")
            driver.implicitly_wait(5)
            ActionChains(driver).move_to_element(button).click(button).perform()
            button=driver.find_element_by_xpath("//a[@class='nav-link dropdown-toggle bd']")
            driver.implicitly_wait(5)
            ActionChains(driver).move_to_element(button).click(button).perform()
        except Exception as e:
            print("Exception Occured:",e)

        time.sleep(5)
        driver=getdata(driver,"2-3-4-bhk")#calling the function to get the data of all the 2,3,4 bhk

        driver.close()
    except Exception as e:
        print("Exception Occured:", e)
        driver.close()
