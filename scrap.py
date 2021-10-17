from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import pandas as pd


chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome('./chromedriver') #Setting Chrome driver PATH

driver.get("https://www.edmunds.com/cars-for-sale-by-owner") #URL to Scrape

zip_field = driver.find_element_by_name("zip") #Input field to Enter Zip Code
time.sleep(5) #Wait for 5 seconds to get the page fully loaded
zip_field.clear() #Clear the zip code field for auto entered data based on geolocation

#zip_field.send_keys('55012') #Entering Zip Code in Zip field
#zip_field.send_keys(Keys.RETURN) #Pressing the Enter Button

en =  driver.find_element_by_xpath('//*[@id="search-radius-range-min"]') #Finding the Radius Slider
time.sleep(5)

move = ActionChains(driver)
#Moving the radius slider to reduce radius area
#Can increase it by changing offset value according to needs
move.click_and_hold(en).move_by_offset(-70, 0).release().perform() 

#Getting List of all items on the page
CarInfoList = driver.find_elements_by_class_name("visible-vehicle-info")

#Getting URLS of each product scraped from page
listOflinks=[]
for el in CarInfoList:
    ppp1=el.find_elements_by_tag_name('h2')[-1]
    pp2=ppp1.find_element_by_tag_name('a')
    listOflinks.append(pp2.get_property('href'))

#For Pagination to get data from all pages
#driver.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/div[1]/div[1]/div/div[2]/div[1]/a').click
#driver.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/div[1]/div[1]/div/div[2]/div[1]/a').click
#driver.find_elements_by_class_name('num-link mx-0_5 px-0_25 text-gray-darker').click()

len(listOflinks) #Checking for Number of Items in List

#Opening URLS of each item
#Collecting data as required i.e a=Name, b=Price, c=VIN, d=Summary, e=Specs
FinalData=[]
for i in listOflinks:
    driver.get(i)
    a=driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[2]/section/h1').text
    b=driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div[1]/div/span').text
    c=driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[2]/section/div[2]/div/span[1]').text
    d=driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[3]/div/div/section[1]/div').text
    #Using try Except method because some items have specs and some have not
    try:
      e=driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[3]/div/div/section[4]/div[1]').text
    except Exception:
      pass
 #Getting data in Dictionary     
    Final={'name':a,
      'price':b,
      'VIN':c,
      'Summary':d,
      'Specs':e,}
    FinalData.append(Final)

#Saving Data into Excel File

df1=pd.DataFrame(FinalData)
df1.to_excel("output.xlsx") 