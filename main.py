# import os

# from datetime import date
# from dateutil.relativedelta import relativedelta
# from gspread import service_account

# from api_util import get_log_data
# from api_fields import hit_field_list, visit_field_list


# if __name__ == "__main__":
#     token = os.getenv("TOKEN")
#     counter_id = os.getenv("COUNTER_ID")
#     api_host_url = "https://api-metrika.yandex.ru"

#     start_date = os.getenv("START_DATE")
#     yesterday = (date.today() - relativedelta(days=1)).strftime("%Y-%m-%d")
#     end_date = os.getenv("END_DATE", default=yesterday)

#     data_list = [{
#         "source": "hits",
#         "api_field_list": hit_field_list,
#         "google_sheet_url": os.getenv("HIT_SHEET_URL")
#     }, {
#         "source": "visits",
#         "api_field_list": visit_field_list,
#         "google_sheet_url": os.getenv("VISIT_SHEET_URL")
#     }]
#     gc = service_account()

#     for data_elem in data_list:
#         data = get_log_data(api_host_url,
#                             counter_id,
#                             token,
#                             data_elem["source"],
#                             start_date,
#                             end_date,
#                             data_elem["api_field_list"])

#         sh = gc.open_by_url(data_elem["google_sheet_url"])
#         sh.sheet1.update([data.columns.values.tolist()]
#                          + data.fillna("Unknown").values.tolist())

import os
from datetime import date
from dateutil.relativedelta import relativedelta
from gspread import service_account

from api_util import get_log_data
from api_fields import hit_field_list, visit_field_list


def get_existing_keys(sheet, key_column):
    records = sheet.get_all_records()
    if not records or key_column not in records[0]:
        return set()
    return set(str(row[key_column]) for row in records)

def ensure_headers(sheet, data):
    """Проверяем наличие заголовков и добавляем, если их нет."""
    existing_values = sheet.get_all_values()
    if not existing_values:
        sheet.append_row(data.columns.tolist(), value_input_option="RAW")


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    counter_id = os.getenv("COUNTER_ID")
    api_host_url = "https://api-metrika.yandex.ru"

    start_date = os.getenv("START_DATE")
    yesterday = (date.today() - relativedelta(days=1)).strftime("%Y-%m-%d")
    end_date = os.getenv("END_DATE", default=yesterday)

    data_list = [{
        "source": "hits",
        "api_field_list": hit_field_list,
        "google_sheet_url": os.getenv("HIT_SHEET_URL"),
        "unique_key": "ym:pv:date"
    }, {
        "source": "visits",
        "api_field_list": visit_field_list,
        "google_sheet_url": os.getenv("VISIT_SHEET_URL"),
        "unique_key": "ym:s:dateTime"
    }]
    
    gc = service_account()

    for data_elem in data_list:
        data = get_log_data(api_host_url,
                            counter_id,
                            token,
                            data_elem["source"],
                            start_date,
                            end_date,
                            data_elem["api_field_list"])

        unique_key = data_elem["unique_key"]
        data[unique_key] = data[unique_key].astype(str)

        sh = gc.open_by_url(data_elem["google_sheet_url"])
        sheet = sh.sheet1

        # Убедимся, что заголовки есть
        ensure_headers(sheet, data)

        existing_keys = get_existing_keys(sheet, unique_key)
        new_data = data[~data[unique_key].isin(existing_keys)]

        if not new_data.empty:
            rows_to_append = new_data[data.columns].fillna("Unknown").values.tolist()
            sheet.append_rows(rows_to_append, value_input_option="USER_ENTERED")
            print(f"✅ Добавлено {len(rows_to_append)} строк в {data_elem['source']}")
        else:
            print(f"ℹ️ Нет новых данных для источника {data_elem['source']}")

