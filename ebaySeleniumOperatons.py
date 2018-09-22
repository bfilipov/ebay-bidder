from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup


def sign_in(driver, email_used, password_used):
    driver.get('https://www.ebay.com/')
    driver.find_element_by_css_selector("span[id=gh-ug] > a").click()

    action1 = webdriver.ActionChains(driver)
    action1.move_to_element(
        driver.find_element_by_css_selector('input[id="userid"]')
    ).click().send_keys(email_used)
    action1.perform()

    action2 = webdriver.ActionChains(driver)
    action2.move_to_element(
        driver.find_element_by_css_selector('input[id="pass"]')
    ).click().send_keys(password_used)
    action2.move_to_element(
        driver.find_element_by_id('sgnBt')
    ).click()
    action2.perform()


def find_items_from_list_with_value_less_than(urls, limit_amount=0.05):
    items_in_query = []
    for item in urls:
        html = urlopen(item)
        bs_obj = BeautifulSoup(html, "html.parser")
        name_list = bs_obj.findAll("li", {"class":"sresult lvresult clearfix li"})
        # driver.get(item) commented on 10.2017 to speed things up
        print(item)

        for name in name_list:
            print(name.li.span.get_text()[:1])

            # print('evaluating if' + name.li.span.get_text() + ' <= ' + str(limit_amount))
            if float(name.li.span.get_text().replace('$','')) <= limit_amount:
                print('Match ->' + name.h3.a['href'])
                items_in_query.append(name.h3.a['href'])
    print("Found " + str(len(items_in_query)) + " items")
    return items_in_query


def bid_on_items(driver, search_items, bid_amount=0.06):
    if len(search_items) > 0:
        for each in search_items:
            driver.get(each)
            try:
                # if not(driver.find_elements_by_xpath("//*[contains(text(), 're the highest bidder.')]")):
                driver.get(driver.find_element_by_xpath("//*[@id='bidBtn_btn']").get_attribute("href"))
                # if not(driver.find_elements_by_xpath("//*[contains(text(), 'Your max bid:')]")):
                driver.implicitly_wait(2)
                act = webdriver.ActionChains(driver)
                print(str(bid_amount))
                act.move_to_element(driver.find_element_by_xpath("//*[@id='maxbid']")).click().send_keys(str(bid_amount))
                act.perform()
                 
                driver.implicitly_wait(2)
                act.move_to_element(driver.find_element_by_xpath("//*[@id='but_v4-1']")).click()
                act.perform()                
                # driver.find_element_by_id("but_v4-1").click()

                driver.implicitly_wait(2)
                act.move_to_element(driver.find_element_by_xpath("//*[@id='but_v4-2']")).click()
                act.perform()
                # driver.find_element_by_id("but_v4-2").click()
                
                driver.implicitly_wait(2)
                act.move_to_element(driver.find_element_by_xpath("//*[@id='bidBtn_btn']")).click()
                act.perform() 
                
            except Exception as e:
                print(e)                
                
            if driver.find_elements_by_xpath("//*[contains(@id, 'but_v4-0')]"):
                try:
                    driver.find_element_by_id("but_v4-0").click()
                except Exception as e:
                    print(e)
