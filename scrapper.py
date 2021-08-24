from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import csv

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("C:/Users/admin/Downloads/Code_Projects/PRO-127/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
star_data=[]
def scrape():
    headers = ["name","distance","mass","radius"]
    for i in range(0,428):
        soup=BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find.all("ul", attrs={"class","star"}):
            li_tags=ul_tag.find_all("li")
            temp_list=[]
            for index, li_tag in enumerate(li_tags):
                if index ==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.find_all("a")[0].contents[0])
                    except:
                           temp_list.append("")
            star_data.append(temp_list)
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table')

        with open("scrapper2.csv","w") as f:
            csvwriter= csv.writer(f)
            csvwriter.writerrow(headers)
            csvwriter.writerows(star.data)     

scrape()