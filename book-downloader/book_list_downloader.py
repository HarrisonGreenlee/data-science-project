from bs4 import BeautifulSoup  # pip install beautifulsoup4
import pandas as pd            # pip install pandas
import requests
import time

def main():
    books = load_csv()
    print(books)

    print('Downloading data for books.csv.')
    print('If your internet is slow this may take a while.')



def load_csv():
    """
    Make sure that the file is set up properly.
    If it isn't - help the user set it up.
    :return: The books dataframe.
    """
    try:
        return pd.read_csv('books.csv')
    except FileNotFoundError:
        selection = input('You do not have a books.csv file yet. Would you like to generate one? [y/n]: ')
        if selection.strip().lower() != 'y':
            print('Cannot download without a CSV file, exiting.')
            quit()
        import book_list_generator
        book_list_generator.main()
        print()
        return load_csv()

if __name__ == '__main__':
    main()