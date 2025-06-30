# Дашборд в DataLens ➡️ <a href = "https://datalens.yandex/omc4fa8tzn6oa">Дашборд онлайн <a/>
- Google Actions запускается по Cron каждый день в 1:13
- Данные загружаются с яндекс метрики в <a href = "https://docs.google.com/spreadsheets/d/12gqdb8ovOHyxhKFq0qnPSdzLlQ9h8d39ZqGIYuXO7AM/edit?usp=sharing">Гугл таблицы <a/>
- DataLens загружает данные для дашборда.
# Метрики:
- Количество пользователей + количество пользователей MoM
- Поиск пользователями по дням, времени, сайту, городу.
- Динамика посещения по дням, неделям, месяцам, кварталам.
# DataLens-Google_sheets
## Получение данных по API с Яндекс метрики в Google Sheets.
### Cron файл `blank_main` запускает main.py каждый день через <a href = "https://github.com/DullSystem/DataLens-Google_sheets/actions">Google Actions<a/>.
### Для работы данного скрипта нужно получить данные и убрать в <a href = "https://github.com/DullSystem/DataLens-Google_sheets/settings/secrets/actions">Secrets and variables<a/>:
- `COUNTER_ID` (ID счётчика в <a href = "https://metrika.yandex.ru/list?period=week&group=day">Яндекс Метрике<a/>)
- `GOOGLE_SERVICE_ACCOUNT` (токен Google Sheets)
- `HIT_SHEET_URL` (ссылка на файл с хитами)
- `START_DATE` (начальная дата для получения данных с Яндекс Метрики)
- `TOKEN` (токен с яндекс метрики)
- `VISIT_SHEET_URL` (ссылка на файл с визитами)

### Для получения ссылки нужно:
- открыть файл в <a href = "https://docs.google.com/spreadsheets/u/0/">Google Sheets<a/>;
- открыть настройки доступа к файлу;
- включить доступ у всех, у кого есть ссылка, на уровне редактора.


#### `START_DATE` - Яндекс Метрика даёт данные не боллее чем за год, необходимо следить за начальной датой и при необходимости обновлять.
#### `TOKEN` - токен с яндекс метрики выдается только на <a href = "https://oauth.yandex.ru/">год<a/> (Для того, чтобы делать запросы к API Яндекс Метрики по своему счётчику, нужно получить токен API. Сделать это нужно согласно инструкции в <a href = "https://yandex.ru/dev/metrika/ru/">официальной документации<a/>.)
#### `COUNTER_ID` - Для того, чтобы обновлять файлы Google Sheets, нужно тоже получать доступы. Рекомендую следовать инструкции из <a href = "https://docs.gspread.org/en/latest/oauth2.html">официальной документации<a/>. Полученный JSON нужно будет положить в секрет под названием `GOOGLE_SERVICE_ACCOUNT`.
