# currently the download process is fairly unreliable
# if a download is corrupted or is cancelled early, we will be left with bad data in our dataset
# this script will delete all of the bad data from the dataset so it can be re-downloaded
# criteria for being a bad download is any of the following:
#   - file does not exist when it should (indicates downloads were stopped prematurely)
#   - first line of eBook does not contain the string 'Gutenberg' (indicates damage at beginning of file)
#   - last line of eBook does not contain the standard message asking users to subscribe (indicates incomplete download)

import pandas as pd
import os
from os.path import exists


def verify_book_downloads(delete_malformed_downloads=True):
    """
    Verifies that every book in the dataset was successfully downloaded.
    Deletes any malformed downloads.
    :return: True if every book in the dataset is correctly installed.
    """
    try:
        books = pd.read_csv('books.csv')
    except FileNotFoundError:
        print('Dataset not found. Cannot verify installation.')
        return False

    all_books_successfully_downloaded = True

    for num in books['catalog_number']:
        book_location = f'./books/{num}/{num}_rawdata.txt'

        if exists(book_location):
            valid_download = True
            # verify header integrity
            with open(book_location, 'r', encoding="utf-8") as f:
                book_lines = f.readlines()
                # book lines could be empty so be sure to check for that to prevent crashes
                if not book_lines or 'gutenberg' not in book_lines[0].lower():
                    print(f'WARNING: {num} has malformed header.')
                    all_books_successfully_downloaded = False
                    valid_download = False

                # if header is valid, verify footer integrity
                # for some reason they pad the end of their eBooks with a random number of newlines
                # we don't really care about these, it's better to verify with some text
                # this is why we are checking the last few lines of the file
                footer_found = False
                for line in reversed(book_lines):
                    if line.strip() == 'subscribe to our email newsletter to hear about new eBooks.':
                        footer_found = True
                        break

                if not footer_found:
                    print(f'WARNING: {num} was not fully downloaded.')
                    all_books_successfully_downloaded = False
                    valid_download = False

            if delete_malformed_downloads and not valid_download:
                print('    deleting malformed download...')
                os.remove(book_location)
        else:
            print(f'WARNING: {book_location} does not exist.')
            all_books_successfully_downloaded = False
    return all_books_successfully_downloaded


if __name__ == '__main__':
    verify_book_downloads()
