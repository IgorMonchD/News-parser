from flask import Flask, Response
import pandas as pd
import json
import os

app = Flask(__name__)

# Конфигурация пути к CSV файлу
app.config['CSV_FILE_PATH'] = 'news_selenium.csv'
app.config['CSV_FILE_PATH_BS'] = 'news_requests.csv'

# Общий метод для чтения и возврата данных из CSV файла
def read_and_return_csv(csv_file_path):
    if not os.path.exists(csv_file_path):
        return Response(json.dumps({'error': 'File not found'}), status=404, content_type='application/json; charset=utf-8')
    try:
        df = pd.read_csv(csv_file_path).fillna('')
        json_data = df.to_json(orient='records', force_ascii=False, indent=4)
        return Response(json_data, content_type='application/json; charset=utf-8')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, content_type='application/json; charset=utf-8')

# Маршрут для запуска парсера Selenium и сохранения данных в CSV
@app.route('/run-selenium', methods=['GET'])
def run_parser_selenium():
    from parsers.SeleniumParser import NewsScraperSelenium
    try:
        scraper = NewsScraperSelenium()
        news_data = scraper.scrape_all_categories()
        scraper.save_to_csv(news_data, filename=app.config['CSV_FILE_PATH'])
        scraper.close()
        return Response(json.dumps({'message': 'Data successfully scraped and saved to CSV'}), status=200,
                        content_type='application/json; charset=utf-8')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, content_type='application/json; charset=utf-8')

# Маршрут для получения данных из CSV файла (Selenium) в формате JSON
@app.route('/parse-selenium', methods=['GET'])
def parse_data_selenium():
    return read_and_return_csv(app.config['CSV_FILE_PATH'])

# Маршрут для запуска парсера BeautifulSoup и сохранения данных в CSV
@app.route('/run-beautifulsoup', methods=['GET'])
def run_parser_beautifulsoup():
    from parsers.BeautifulSoupParser import NewsScraperBeautifulSoup
    try:
        scraper = NewsScraperBeautifulSoup()
        news_data = scraper.scrape_all_categories()
        scraper.save_to_csv(news_data, filename=app.config['CSV_FILE_PATH_BS'])
        return Response(json.dumps({'message': 'Data successfully scraped and saved to CSV'}), status=200,
                        content_type='application/json; charset=utf-8')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, content_type='application/json; charset=utf-8')

# Маршрут для получения данных из CSV файла (BeautifulSoup) в формате JSON
@app.route('/parse-beautifulsoup', methods=['GET'])
def parse_data_beautifulsoup():
    return read_and_return_csv(app.config['CSV_FILE_PATH_BS'])

if __name__ == '__main__':
    app.run(port=5000)