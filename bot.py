from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from datetime import datetime
from bs4 import BeautifulSoup
import threading
import requests
import time


class Bot(threading.Thread):
    def __init__(self, product_code, email, password, refresh_interval=2):
        threading.Thread.__init__(self)
        self.email = email
        self.password = password
        self.product_code = product_code
        self.refresh_interval = refresh_interval
        self.driver = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        self.product_url = 'https://www.amazon.co.jp/gp/product/{}?language=en_US'.format(product_code)

    def run(self):
        self.monitor()

    def start_browser(self):
        self.print_log('Starting browser')
        self.driver = webdriver.Chrome()
        self.driver.get(self.product_url)

    def monitor(self):
        self.print_log('Start monitoring')
        seller = None

        while seller != 'Amazon.co.jp':
            resp = requests.get(self.product_url, headers=self.headers)
            soup = BeautifulSoup(resp.text, 'html.parser')
            seller = soup.select_one('#merchant-info a').text if soup.select_one('#merchant-info a') else ''
            time.sleep(self.refresh_interval)
        self.print_log('In stock')
        self.order()

    def order(self):
        self.start_browser()
        try:
            # Buy item
            self.driver.maximize_window()
            self.driver.find_element_by_name('submit.buy-now').click()
            self.driver.implicitly_wait(1.5)

            # Login if necessary
            self.driver.find_element_by_id('ap_email').send_keys(self.email)
            self.driver.find_element_by_id('continue').click()
            self.driver.find_element_by_id('ap_password').send_keys(self.password)
            self.driver.find_element_by_id('signInSubmit').click()
            self.print_log('Logged In')
            self.driver.implicitly_wait(2)

            # Select payment method
            self.driver.find_element_by_name('ppw-widgetEvent:SetPaymentPlanSelectContinueEvent').click()
            self.print_log('Selected payment method')
            self.driver.implicitly_wait(5)

            # Confirm payment
            self.driver.find_element_by_name('placeYourOrder1').click()
            self.print_log('Order has placed successfully')

            self.driver.quit()
        except WebDriverException:
            self.print_log("Error occurred in ordering process")

    def print_log(self, msg):
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' [' + self.product_code + '] - ' + msg)
