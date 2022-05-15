import pandas as pd
from fuzzywuzzy import fuzz



"""Протестируем работу алгоритма, в частности, из библиотеки """
#Создаем Дата Фрейм

df_marketplace1 = pd.DataFrame({
    'name': ['apple', 'banana', 'orange', 'mango'],
    'prod_id': [1, 2, 3, 4]
})

df_marketplace2 = pd.DataFrame({
    'name': ['lime', 'mango', 'banana', 'pear', 'bnana', 'aple 4'],
    'prod_id': [1, 2, 3, 4, 5, 6]
})

def check_similarity(df1, df2):
    res = []
    df1, df2 = df_marketplace1, df_marketplace2
    for i, row1 in df1.iterrows():
        for j, row2 in df2.iterrows():
            if fuzz.WRatio(row1['name'], row2['name']) >= 80:
                print(f'Продукты {row1["name"]} и {row2["name"]} схожи на {fuzz.WRatio(row1["name"], row2["name"])}%')
                res.append((row1['prod_id'], row2['prod_id']))
            else:
                print(f'Продукты {row1["name"]} и {row2["name"]} схожи на {fuzz.WRatio(row1["name"], row2["name"])}%')
        print('......Обработан один продукт......\n')
    print('......Все продукты обработаны......\n')
    print(*res, sep='\n')

if __name__ == '__main__':
    check_similarity(df_marketplace1, df_marketplace2)