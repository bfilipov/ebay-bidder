import logging
from urllib.request import urlopen

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


class EbayBidder:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = logging.getLogger(__name__)
        self.driver.implicitly_wait(0)
        # use explicit waits for each element that must be clicked on.

    def sign_in(self, email, password):
        self.driver.get('https://www.ebay.com/')
        self.driver.find_element_by_css_selector("span[id=gh-ug] > a").click()
        self.send_input_to_id_when_ready(email, 'userid')
        self.send_input_to_id_when_ready(password, 'pass')
        action2.move_to_element(
            self.driver.find_element_by_id('sgnBt')).click()
        action2.perform()

    def send_input_to_id_when_ready(self, input, id, waittime=5):
        try:
            WebDriverWait(self.driver, waittime).until(
                ec.presence_of_element_located((By.ID, id))
            )
        except TimeoutException as e:
            self.logger.error(e)

        element = self.driver.find_element_by_css_selector(f'input[id="{id}"]')

        enter_password_action = webdriver.ActionChains(self.driver)
        enter_password_action.move_to_element(element).click()
        enter_password_action.send_keys(input)
        enter_password_action.perform()

    def find_items_from_list_with_value_less_than(self, urls, limit_amount=0.05):
        items_in_query = []
        for item in urls:
            html = urlopen(item)
            bs_obj = BeautifulSoup(html, "html.parser")
            name_list = bs_obj.findAll("li", {"class": "sresult lvresult clearfix li"})
            self.logger.info(item)

            for name in name_list:
                self.logger.info(name.li.span.get_text()[:1])
                if float(name.li.span.get_text().replace('$', '')) <= limit_amount:
                    self.logger.info('Match ->' + name.h3.a['href'])
                    items_in_query.append(name.h3.a['href'])
        self.logger.info("Found " + str(len(items_in_query)) + " items")
        return items_in_query

    def bid_on_items(self, search_items, bid_amount=0.06):
        if len(search_items) > 0:
            for each in search_items:
                driver.get(each)
                try:
                    # if not(driver.find_elements_by_xpath("//*[contains(text(), 're the highest bidder.')]")):
                    self.driver.get(driver.find_element_by_xpath("//*[@id='bidBtn_btn']").get_attribute("href"))
                    # if not(driver.find_elements_by_xpath("//*[contains(text(), 'Your max bid:')]")):
                    self.driver.implicitly_wait(2)
                    act = webdriver.ActionChains(self.driver)
                    self.logger.info(str(bid_amount))
                    act.move_to_element(self.driver.find_element_by_xpath("//*[@id='maxbid']")).click().send_keys(str(bid_amount))
                    act.perform()

                    self.driver.implicitly_wait(2)
                    act.move_to_element(self.driver.find_element_by_xpath("//*[@id='but_v4-1']")).click()
                    act.perform()
                    # driver.find_element_by_id("but_v4-1").click()

                    self.driver.implicitly_wait(2)
                    act.move_to_element(self.driver.find_element_by_xpath("//*[@id='but_v4-2']")).click()
                    act.perform()
                    # driver.find_element_by_id("but_v4-2").click()

                    self.driver.implicitly_wait(2)
                    act.move_to_element(self.driver.find_element_by_xpath("//*[@id='bidBtn_btn']")).click()
                    act.perform()

                except Exception as e:
                    self.logger.error(e)

                if self.driver.find_elements_by_xpath("//*[contains(@id, 'but_v4-0')]"):
                    try:
                        self.driver.find_element_by_id("but_v4-0").click()
                    except Exception as e:
                        self.logger.error(e)
