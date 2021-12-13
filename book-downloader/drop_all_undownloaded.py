# deletes any books that are not present on the computer from the dataset
# you could also manually filter the CSV
# but this is a bit easier if you are sure that you are not going to use any books in the dataset that arent downloaded

import pandas as pd
from os.path import exists


def main():
    if exists('books.csv'):
        print('WARNING - Running this program will delete any books in books.csv that do not have corresponding text files.')
        confirmation = input('Type "y" to confirm: ')
        if not confirmation.lower() == 'y':
            return
    else:
        print('Could not find books.csv.')
        return

    df = pd.read_csv('trimmed_books.csv')

    indices_to_delete = []
    for ind in df.index:
        catalog_number = df['catalog_number'][ind]
        if not exists(f'books/{catalog_number}/{catalog_number}_rawdata.txt'):
            indices_to_delete.append(ind)

    print(f'This operation will delete {len(indices_to_delete)} entries.')
    confirmation = input('Type "y" to confirm: ')
    if not confirmation.lower() == 'y':
        return
    df.drop(index=indices_to_delete, inplace=True)
    df.to_csv('trimmed_books.csv', index=False)

if __name__ == "__main__":
    main()