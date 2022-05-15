import pandas as pd
from sqlalchemy import create_engine
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json

def create_dataframes():

    """Функция, которая создает DataFrame таблицы по запросам SQL"""

    engine = create_engine('mysql+pymysql://root:f,fksvjd@localhost:3306/alikson')

    # Сделаем 2 запроса в базу данных
    sql_1 = 'select id, name, marketplace_id from products where marketplace_id = 1 limit 50'
    sql_2 = 'select id, name, marketplace_id from products where marketplace_id = 2 limit 10000'

    # Форматируем данные в DataFrame с помощью pandas
    df_1 = pd.read_sql(sql_1, engine)
    df_2 = pd.read_sql(sql_2, engine)
    return (df_1, df_2)


def check_similarity(df):

    """Функция, которая проверяет на сходство наименования товаров с 2 Маркетплейсов"""

    res = []
    df_1, df_2 = df

    # Извлекаем значения из столбцов таблиц и назначаем каждому столбцу переменную
    df_1_columns = list(df_1.columns.values)
    product_id1, name1, marketplace_id1 = df_1_columns[0], df_1_columns[1], df_1_columns[2]

    df_2_columns = list(df_2.columns.values)
    product_id2, name2, marketplace_id2 = df_2_columns[0], df_2_columns[1], df_2_columns[2]

    for i, row1 in df_1.iterrows():
        for j, row2 in df_2.iterrows():
            if fuzz.WRatio(row1[name1], row2[name2]) >= 80:
                res.append(
                    {
                        'Товар с Маркетплейса 1': [row1[name1], row1[product_id1]],
                        'Товар с Маркетплейса 2': [row2[name2], row2[product_id2]],
                        'Сходство товаров': [row1[product_id1], row2[product_id2], fuzz.WRatio(row1[name1], row2[name2])]
                    }
                )

    with open('Result.json', 'a', encoding='utf-8') as file:
        json.dump(res, file, indent=4, ensure_ascii=False)

    print('\n......Все продукты обработаны......')


if __name__ == '__main__':
    dataframes = create_dataframes()
    check_similarity(dataframes)
