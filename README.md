# News-parser

Для создания виртуального окружения и установки пакетов из файла `requirements.txt`, выполните следующие шаги:

1. **Создание виртуального окружения:**

   Откройте терминал или командную строку и выполните следующую команду:

   ```bash
   python -m venv .venv
   ```

   Здесь `myenv` — это имя виртуального окружения. Вы можете выбрать любое другое имя.

2. **Активация виртуального окружения:**

   - **Windows:**

     ```bash
      .venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source  .venv/bin/activate
     ```

   После активации виртуального окружения, ваш командный prompt изменится, чтобы показать имя активного окружения, например:

   ```bash
   (.venv) C:\YourProject>
   ```

3. **Установка пакетов из `requirements.txt`:**

   С активным виртуальным окружением выполните следующую команду:

   ```bash
   pip install -r requirements.txt
   ```

   Эта команда установит все пакеты, перечисленные в файле `requirements.txt`, в ваше виртуальное окружение.

Теперь ваше виртуальное окружение настроено и все необходимые пакеты установлены. Вы можете начать работу над вашим проектом.

Запуск приложения:
```bash
python app.py
```
Все маршруты:
```
http://127.0.0.1:5000/run-selenium
```
![image](https://github.com/IgorMonchD/News-parser/assets/113885516/c8e2c4c4-cf63-4e01-840d-05d0f3a1297f)

```
http://127.0.0.1:5000/parse-selenium
```
**Отсутствие файла:**

![image](https://github.com/IgorMonchD/News-parser/assets/113885516/53cf67ef-0320-433b-bd7a-75ce6c3498c5)

**Успешный запрос:**

![image](https://github.com/IgorMonchD/News-parser/assets/113885516/6d78e0e6-970b-4c9f-9dc3-c1d4472328b5)

```
http://127.0.0.1:5000/run-beautifulsoup
http://127.0.0.1:5000/parse-beautifulsoup
```
