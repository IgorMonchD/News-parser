from flask import Flask, Response, request
import pandas as pd
import json
import os
from parser import NewsScraper

app = Flask(__name__)

# Конфигурация пути к CSV файлу
app.config['CSV_FILE_PATH'] = 'news_selenium.csv'


# Маршрут для запуска парсера и сохранения данных в CSV
@app.route('/run', methods=['GET'])
def run_parser():
    try:
        scraper = NewsScraper()
        news_data = scraper.scrape_all_categories()
        scraper.save_to_csv(news_data, filename=app.config['CSV_FILE_PATH'])
        scraper.close()
        return Response(json.dumps({'message': 'Data successfully scraped and saved to CSV'}), status=200,
                        content_type='application/json; charset=utf-8')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, content_type='application/json; charset=utf-8')


# Маршрут для получения данных из CSV файла в формате JSON
@app.route('/parse', methods=['GET'])
def parse_data():
    csv_file_path = app.config['CSV_FILE_PATH']

    # Проверка наличия файла
    if not os.path.exists(csv_file_path):
        return Response(json.dumps({'error': 'File not found'}), status=404,
                        content_type='application/json; charset=utf-8')
    try:
        # Чтение данных из CSV файла
        df = pd.read_csv(csv_file_path)
        df.fillna('', inplace=True)
        json_data = df.to_json(orient='records', force_ascii=False, indent=4)
        return Response(json_data, content_type='application/json; charset=utf-8')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, content_type='application/json; charset=utf-8')


if __name__ == '__main__':
    app.run(port=5000)