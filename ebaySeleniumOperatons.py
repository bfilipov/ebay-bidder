# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 16:16:56 2018

@author: bFilipov
"""
from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup

def signin(driver,emailUsed,passswordUsed):
    driver.get('https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&ru=http%3A%2F%2Fwww.ebay.com%2F')
    
    action1 = webdriver.ActionChains(driver)
    #action1.move_to_element(driver.find_element_by_css_selector('div #pri_signin div span input')).send_keys(emailUsed)''Stopped woringg 02.2017
    #action1.move_to_element(driver.find_element_by_css_selector('div #pri_signin input')).send_keys(emailUsed) stopped working 10.2017
    action1.move_to_element(driver.find_element_by_css_selector('input[placeholder="Email or username"]')).click().send_keys(emailUsed)
    action1.perform()
    action2 = webdriver.ActionChains(driver)
    #action2.move_to_element(driver.find_element_by_css_selector('div #pri_signin :nth-child(6) span input')).click().send_keys(passswordUsed) stopped worlomg 10.2017
    action2.move_to_element(driver.find_element_by_css_selector('input[type="Password"]')).click().send_keys(passswordUsed)
    action2.perform()
    driver.find_element_by_id('sgnBt').click()

def findSearchItems(urls=[],limitAmount=0.05):
    itemsInQuery = []
    for item in urls:
        html=urlopen(item)
        bsObj = BeautifulSoup(html, "html.parser")
        nameList = bsObj.findAll("li", {"class":"sresult lvresult clearfix li"})
        #driver.get(item) commented on 10.2017 to speed things up
        print(item)

        for name in nameList:
            print(name.li.span.get_text()[:1])

            #print('evaluationg if' + name.li.span.get_text() + ' <= ' + str(limitAmount))
            if float(name.li.span.get_text().replace('$','')) <= limitAmount:
                print('Match ->' + name.h3.a['href'])
                itemsInQuery.append(name.h3.a['href'])
    print("Found " + str(len(itemsInQuery)) + " items")
    return itemsInQuery



def bidOnItems(driver,searchItems,bidAmmount=0.06):
    if len(searchItems) > 0:
        for each in searchItems:        
            driver.get(each)
            try:
                #if not(driver.find_elements_by_xpath("//*[contains(text(), 're the highest bidder.')]")):
                driver.get(driver.find_element_by_xpath("//*[@id='bidBtn_btn']").get_attribute("href"))
                #if not(driver.find_elements_by_xpath("//*[contains(text(), 'Your max bid:')]")):
                driver.implicitly_wait(2)
                act = webdriver.ActionChains(driver)
                print(str(bidAmmount))
                act.move_to_element(driver.find_element_by_xpath("//*[@id='maxbid']")).click().send_keys(str(bidAmmount))
                act.perform()
                 
                driver.implicitly_wait(2)
                act.move_to_element(driver.find_element_by_xpath("//*[@id='but_v4-1']")).click()
                act.perform()                
                #driver.find_element_by_id("but_v4-1").click()

                driver.implicitly_wait(2)
                act.move_to_element(driver.find_element_by_xpath("//*[@id='but_v4-2']")).click()
                act.perform()
                #driver.find_element_by_id("but_v4-2").click()
                
                driver.implicitly_wait(2)
                act.move_to_element(driver.find_element_by_xpath("//*[@id='bidBtn_btn']")).click()
                act.perform() 
                
            except Exception as e:
                print(e)
                pass
                
            if driver.find_elements_by_xpath("//*[contains(@id, 'but_v4-0')]"):
                try:
                    driver.find_element_by_id("but_v4-0").click()
                except Exception as e:
                    print(e)
                    pass
