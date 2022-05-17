import pandas as pd
from sqlalchemy import create_engine
from fuzzywuzzy import fuzz
import json


def create_dataframes():

    """Функция, которая создает DataFrame таблицы по запросам SQL"""

    engine = create_engine('mysql+pymysql://root:f,fksvjd@localhost:3306/alikson')

    sql_1 = '''
        SELECT products.id, products.name, marketplace_id, brandnames.name AS brandname
        FROM brands
        JOIN products ON brands.id = products.brand_id
        JOIN brandnames ON brands.id = brandnames.brand_id
        WHERE marketplace_id = 1
        LIMIT 20000;
        '''
    sql_2 = '''
        SELECT products.id, products.name, marketplace_id, brandnames.name AS brandname
        FROM brands
        JOIN products ON brands.id = products.brand_id
        JOIN brandnames ON brands.id = brandnames.brand_id
        WHERE marketplace_id = 2
        LIMIT 20000;
        '''

    # Форматируем данные в DataFrame с помощью pandas
    df_1 = pd.read_sql(sql_1, engine)
    df_2 = pd.read_sql(sql_2, engine)
    return df_1, df_2


def check_similarity(df):

    """Функция, которая фильтрует товары с 2 Маркетплейсов по бренду и проверяет их наименования на сходство"""

    res = []
    df_1, df_2 = df

    # Переведем названия всех брендов в нижний регистр, для точности фильтрации
    df_1['brandname'], df_2['brandname'] = df_1.brandname.str.lower(), df_2.brandname.str.lower()

    # Извлекаем значения из столбцов таблиц и назначаем каждому столбцу переменную
    df_1_columns = list(df_1.columns.values)
    product_id1, name1, marketplace_id1, brandname1 = df_1_columns[0], df_1_columns[1], df_1_columns[2], df_1_columns[3]

    df_2_columns = list(df_2.columns.values)
    product_id2, name2, marketplace_id2, brandname2 = df_2_columns[0], df_2_columns[1], df_2_columns[2], df_1_columns[3]

    # Создадим множество пересекающихся брендов brands из двух Маркетплейсов
    brands = {b.lower() for b in df_1[brandname1]} & {b.lower() for b in df_2[brandname2]}

    for brand in brands:

        for i, row1 in df_1.loc[df_1[brandname1] == brand].iterrows():

            for j, row2 in df_2.loc[df_2[brandname2] == brand].iterrows():

                similarity_by_name = fuzz.WRatio(row1[name1], row2[name2])
                if similarity_by_name >= 88:
                    res.append(
                        {
                            'Товар с Маркетплейса 1': [row1[name1], row1[product_id1]],
                            'Товар с Маркетплейса 2': [row2[name2], row2[product_id2]],
                            'ID схожих товаров': [row1[product_id1], row2[product_id2]]
                        }
                    )

    with open('Result.json', 'a', encoding='utf-8') as file:
        json.dump(res, file, indent=4, ensure_ascii=False)

    print('\n......Все продукты обработаны......')


if __name__ == '__main__':
    dataframes = create_dataframes()
    check_similarity(dataframes)
