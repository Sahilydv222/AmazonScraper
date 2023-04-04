
#======================================================================================================================================================================
#                                            >>>>>>>>>>>>>>>>Importing required modules<<<<<<<<<<<<<<<<<<<<<<<<
#=======================================================================================================================================================================
from selenium import webdriver     # for driver
from time import sleep              # for sleep
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import csv     # for writing csv file


count = 1
#======================================================================================================================================================================
#                                            >>>>>>>>>>>>>>>>Intializing browser<<<<<<<<<<<<<<<<<<<<<<<<
#=======================================================================================================================================================================
browser = webdriver.Chrome()
for i in range(1,2):
    browser.get(f'https://www.amazon.in/s?i=electronics&rh=n%3A6612025031&fs=true&page={i}&ref=sr_pg_{i}')
    sleep(5)
    source = browser.page_source        # getting the Source of page 
    
    soup = bs(source , "html.parser")


    all_deal = soup.find_all("div",{"class":"a-section a-spacing-base"})   # grtting list of products on page 
    
    length = len(all_deal)
    for item in all_deal:
#======================================================================================================================================================================
#                                            >>>>>>>>>>>>>>>>Scraping products details<<<<<<<<<<<<<<<<<<<<<<<<
#=======================================================================================================================================================================
        title = item.find("span",{"class":"a-size-base-plus a-color-base a-text-normal"}).text
        price = item.find("span",{"class":"a-price-whole"}).text
        Rating = item.find("span",{"class":"a-icon-alt"}).text
        
#======================================================================================================================================================================
#                                            >>>>>>>>>>>>>>>> Going to detail page for getting seller and stock of product <<<<<<<<<<<<<<<<<<<<<<<<
#======================================================================================================================================================================= 

        browser.find_element(By.XPATH,f'(//span[@class="a-size-base s-underline-text"])[{count}]').click()
        count+=1
        sleep(5)

        browser.switch_to.window( browser.window_handles[1])                    # Switching to  The Detail page Tab 
        sleep(5)
        new_page_source = browser.page_source
        soup2 = bs(new_page_source , "html.parser")
        seller = soup2.find("div",{"id":"merchant-info"}).find("a").find("span").text
        stock = soup2.find("span",{"class":"a-size-medium a-color-success"})
        if stock != None:
            stock=stock.text
        else:
            stock = "out of stock"
        
        browser.close()
        sleep(3)
        browser.switch_to.window(browser.window_handles[0])             # Switching Back to The all deals Tab 
        
        
#======================================================================================================================================================================
#                                            >>>>>>>>>>>>>>>>Writing into csv file<<<<<<<<<<<<<<<<<<<<<<<<
#=======================================================================================================================================================================     

        with open(f'amazon_products.csv', "w+" ) as file:
            writer = csv.writer(file)
            writer.writerow(["Product Name", "Price", "Rating", "Seller Name" , "stock"])
            writer.writerow([title, price, Rating, seller , stock])

        if count == length:
            count = 1