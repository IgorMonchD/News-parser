import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsScraper:
    def __init__(self):
        self.main_url = 'https://www.rbc.ru/'
        self.categories_urls = self.get_categories_from_footer()

    def get_categories_from_footer(self):
        response = requests.get(self.main_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        categories_urls = {}
        footer_list = soup.select_one('ul.footer__list[data-publisher-nick="main_footer_links"]')
        if footer_list:
            footer_items = footer_list.select('.footer__item')[:5]
            for item in footer_items:
                link = item.select_one('.footer__link')
                if link:
                    category = link.text.strip()
                    url = link.get('href')
                    categories_urls[category] = url
        return categories_urls

    def collect_news_data(self, category, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Поиск первой новости
            news_element = soup.select_one('.item__link')
            if news_element:
                title = news_element.text.strip()
                link = news_element.get('href')

                # Переход по ссылке для получения описания
                news_response = requests.get(link)
                news_soup = BeautifulSoup(news_response.text, 'html.parser')

                description_element = news_soup.select_one('head meta[name="description"]')
                description = description_element.get('content') if description_element else ''

                return {
                    'category': category,
                    'title': title,
                    'link': link,
                    'description': description
                }
            else:
                logging.error(f"Элемент новости не найден для категории {category}")
                return None
        except Exception as e:
            logging.error(f"Ошибка при сборе данных для категории {category}: {e}")
            return None

    def scrape_all_categories(self):
        news_data = []
        for category, url in self.categories_urls.items():
            data = self.collect_news_data(category, url)
            if data:
                news_data.append(data)
        return news_data

    def save_to_csv(self, data, filename='news_requests.csv'):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')

# Использование класса
scraper = NewsScraper()
news_data = scraper.scrape_all_categories()
scraper.save_to_csv(news_data)