from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
START_URL="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser=webdriver.Chrome("/Users/ramhp/chromedriver")
browser.get(START_URL)
time.sleep(10)
headers=["Name","Distance","Mass","Radius"]
sun_data=[]
new_sun_data=[]
def scrape():
     for i in range(0,1):
         while True:
             time.sleep(2)
             soup = BeautifulSoup(browser.page_source,"html.parser")
             current_page_num=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
             if current_page_num<i:
                 browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
             elif current_page_num>i:
                 browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
             else:
                 break
         for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
             li_tags=ul_tag.find_all("li")
             temp_list=[]
             for index,li_tag in enumerate(li_tags):
                 if index == 0:
                     temp_list.append(li_tag.find_all("a")[0].contents[0])
                 else:
                     try:
                         temp_list.append(li_tag.contents[0])
                     except:
                         temp_list.append("")
             hyperlink_li_tag = li_tags[0]
             temp_list.append("https://en.wikipedia.org/"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])     
             sun_data.append(temp_list)
         browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
def scrape_more_data(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.path0")
        temp_list=[]
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
             th_tags=tr_tag.find_all("th")
             for th_tag in th_tags:
                 try:
                     temp_list.append(th_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                 except:
                     temp_list.append("")
        new_sun_data.append(temp_list)
    except:
        time.sleep(1)
        sleep_more_data(hyperlink)
scrape()
for index,data in enumerate(sun_data):
    scrape_more_data(data[5])
final_sun_data=[]
for index,data in enumerate(sun_data):
    new_sun_data_element=new_sun_data[index]
    new_sun_data_element=[elem.replace("\n","")for elem in new_sun_data_element]
    new_sun_data_element=new_sun_data_element[:7]
    final_sun_data.append(data+new_sun_data_element)
with open("final.csv","w")as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_sun_data)