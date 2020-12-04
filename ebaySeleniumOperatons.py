import logging
import time
import os
import zipfile
from urllib.request import urlopen

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import undetected_chromedriver as uc
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()


class EbayBidder:
    def __init__(self, proxy=False, headless=False):
        self.options = uc.ChromeOptions()
        if headless:
            self.options.headless = True
            self.options.add_argument('--headless')

        if proxy:
            self.set_proxy()

        self.driver = uc.Chrome(options=self.options)
        self.logger = logging.getLogger(__name__)
        self.driver.implicitly_wait(0)

    def get(self, url):
        self.driver.get(url)

    def sign_in(self, email, password):
        self.driver.get('https://www.ebay.com/')
        self.driver.find_element_by_css_selector("span[id=gh-ug] > a").click()
        self.send_input_to_id_when_ready(email, 'userid')
        self.click_to_button_with_id_when_ready('signin-continue-btn')
        # time.sleep(1)
        self.send_input_to_id_when_ready(password, 'pass')
        self.click_to_button_with_id_when_ready('sgnBt')
        action = webdriver.ActionChains(self.driver)
        action.move_to_element(
            self.driver.find_element_by_id('sgnBt')).click()
        action.perform()

    def send_input_to_id_when_ready(self, input, id, waittime=5):
        self.wait_for_id(id, waittime)
        element = self.driver.find_element_by_css_selector(f'input[id="{id}"]')
        enter_password_action = webdriver.ActionChains(self.driver)
        enter_password_action.move_to_element(element).click()
        enter_password_action.send_keys(input)
        try:
            enter_password_action.perform()
        except NoSuchElementException as e:
            self.logger.error(e)

    def wait_for_id(self, id, waittime):
        try:
            WebDriverWait(self.driver, waittime).until(
                ec.presence_of_element_located((By.ID, id))
            )
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(e)

    def click_to_button_with_id_when_ready(self, id, waittime=5):
        self.wait_for_id(id, waittime)
        button = self.driver.find_element_by_css_selector(f'button#{id}')
        click_to_button_if_present = webdriver.ActionChains(self.driver)
        click_to_button_if_present.move_to_element(button).click()
        try:
            click_to_button_if_present.perform()
        except NoSuchElementException as e:
            self.logger.error(e)

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
                self.driver.get(each)
                try:
                    # if not(driver.find_elements_by_xpath("//*[contains(text(), 're the highest bidder.')]")):
                    self.driver.get(self.driver.find_element_by_xpath("//*[@id='bidBtn_btn']").get_attribute("href"))
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

    def set_proxy(self):
        PROXY_HOST = os.getenv('PROXY_HOST')
        PROXY_PORT = os.getenv('PROXY_PORT')
        PROXY_USER = os.getenv('PROXY_USER')
        PROXY_PASS = os.getenv('PROXY_PASS')

        manifest_json = """
                {
                    "version": "1.0.0",
                    "manifest_version": 2,
                    "name": "Chrome Proxy",
                    "permissions": [
                        "proxy",
                        "tabs",
                        "unlimitedStorage",
                        "storage",
                        "<all_urls>",
                        "webRequest",
                        "webRequestBlocking"
                    ],
                    "background": {
                        "scripts": ["background.js"]
                    },
                    "minimum_chrome_version":"22.0.0"
                }
                """

        background_js = """
                var config = {
                        mode: "fixed_servers",
                        rules: {
                        singleProxy: {
                            scheme: "http",
                            host: "%s",
                            port: parseInt(%s)
                        },
                        bypassList: ["localhost"]
                        }
                    };

                chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                }

                chrome.webRequest.onAuthRequired.addListener(
                            callbackFn,
                            {urls: ["<all_urls>"]},
                            ['blocking']
                );
                """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        self.options.add_extension(pluginfile)
        # use explicit waits for each element that must be clicked on.
