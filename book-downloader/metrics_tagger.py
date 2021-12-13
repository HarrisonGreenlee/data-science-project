import pandas as pd
import numpy as np
from metrics_calculator import calc_metrics

df = pd.read_csv('books.csv')
df["flesch_kincaid"] = np.nan
df["adi"] = np.nan
df["word_count"] = np.nan
print(df)

for index, row in df.iterrows():
    print(f'Analyzing {row["title"]}...')
    catalog_number = row['catalog_number']
    # this is a really long process so if it fails on a single book for some reason we don't want to lose our progress
    # better to just catch the exception and leave a NaN to be dropped or fixed manually
    try:
        metrics_results = calc_metrics(f'books/{catalog_number}/{catalog_number}_rawdata.txt')
        print(metrics_results)
        df.loc[index, 'flesch_kincaid'] = metrics_results['flesch_kincaid']
        df.loc[index, 'adi'] = metrics_results['adi']
        df.loc[index, 'word_count'] = metrics_results['word_count']
    except Exception as e:
        print(f'WARNING - COULD NOT CALCULATE METRICS FOR {catalog_number}.')
        print(e)

df.to_csv('books_with_metrics.csv', index=False)