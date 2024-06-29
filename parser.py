import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import logging

logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.main_url = 'https://www.rbc.ru/'
        self.categories_urls = self.get_categories_from_footer()

    def get_categories_from_footer(self):
        self.driver.get(self.main_url)
        time.sleep(1)
        categories_urls = {}
        footer_list = self.driver.find_element(By.CSS_SELECTOR, 'ul.footer__list[data-publisher-nick="main_footer_links"]')
        footer_items = footer_list.find_elements(By.CLASS_NAME, 'footer__item')
        for item in footer_items[:5]:
            link = item.find_element(By.CLASS_NAME, 'footer__link')
            category = link.text
            url = link.get_attribute('href')
            categories_urls[category] = url
        return categories_urls

    def collect_news_data(self, category, url):
        try:
            self.driver.get(url)
            time.sleep(1)

            # Поиск первой новости
            news_element = self.driver.find_element(By.CLASS_NAME, 'item__link')
            title = news_element.text
            link = news_element.get_attribute('href')

            self.driver.get(link)
            time.sleep(1)

            try:
                description_element = self.driver.find_element(By.XPATH, '//head/meta[@name="description"]')
                description = description_element.get_attribute('content')

            except NoSuchElementException:
                description = ''

            return {
                'category': category,
                'title': title,
                'link': link,
                'description': description
            }
        except WebDriverException as e:
            logging.error(f"Ошибка при сборе данных для категории {category}: {e}")
            return None

    def scrape_all_categories(self):
        news_data = []
        for category, url in self.categories_urls.items():
            data = self.collect_news_data(category, url)
            if data:
                news_data.append(data)
        return news_data

    def save_to_csv(self, data, filename='news_selenium.csv'):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')

    def close(self):
        self.driver.quit()

# Использование класса
scraper = NewsScraper()
news_data = scraper.scrape_all_categories()
scraper.save_to_csv(news_data)
scraper.close()