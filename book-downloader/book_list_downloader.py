from bs4 import BeautifulSoup  # pip install beautifulsoup4
import pandas as pd  # pip install pandas
import pathlib
import requests
import time
from os.path import exists

from book_download_verifier import verify_book_downloads


def main():
    download_books()
    # ensure downloaded books are valid
    # if they are not, remove them and try to download them again
    # limit the number of times we try this to prevent an infinite loop
    for attempt in range(3):
        if not verify_book_downloads():
            print("Download failed. Re-downloading malformed downloads.")
            download_books()
    if verify_book_downloads(delete_malformed_downloads=False):
        print("All books successfully downloaded.")
    else:
        print("Books could not be successfully installed.")
        print("Try connecting to a more reliable network and trying again.")
        print("NOTE: this could also be caused by a book with non-standard formatting.")


def download_books():
    books = load_csv()

    print("Downloading data for books.csv.")
    print("If your internet is slow this may take a while.")
    for num in books["catalog_number"]:
        if not exists(f"./books/{num}/{num}_rawdata.txt"):
            r = requests.get(
                f"http://gutenberg.org/files/{num}/{num}-0.txt", allow_redirects=True
            )
            r.encoding = "utf-8-sig"
            pathlib.Path(f"./books/{num}").mkdir(parents=True, exist_ok=True)
            with open(f"./books/{num}/{num}_rawdata.txt", "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"    Successfully Downloaded: {num}")
            # wait a bit before the next download to prevent overloading Project Gutenberg servers and getting IP banned
            # lowering this will massively increase download speed, if necessary
            time.sleep(1)
        else:
            print(f"    Already downloaded:      {num}")


def load_csv():
    """
    Make sure that the file is set up properly.
    If it isn't - help the user set it up.
    :return: The books dataframe.
    """
    try:
        return pd.read_csv("books.csv")
    except FileNotFoundError:
        selection = input(
            "You do not have a books.csv file yet. Would you like to generate one? [y/n]: "
        )
        if selection.strip().lower() != "y":
            print("Cannot download without a CSV file, exiting.")
            quit()
        import book_list_generator

        book_list_generator.main()
        print()
        return load_csv()


if __name__ == "__main__":
    main()
