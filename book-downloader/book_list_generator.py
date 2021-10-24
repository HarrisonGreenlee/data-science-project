# step one of assembling the dataset
# scans Project Gutenberg's most popular books and generates a list of them
# does not download the actual text from the book yet, just collects titles and download links

from bs4 import BeautifulSoup  # pip install beautifulsoup4
import pandas as pd            # pip install pandas
import requests
import time


def main():
    confirmation = input('Running this program will delete books.csv if it already exists. Type "y" to confirm: ')
    if confirmation.lower() == 'y':
        print('Each page of Project Gutenberg has 25 ebooks on it.')
        pages_to_read = input('How many pages would you like to index? ')

        # safely convert user input to an integer, asking them for correct input if necessary
        while not isinstance(pages_to_read, int):
            try:
                pages_to_read = int(pages_to_read)
            except ValueError:
                print('Invalid selection. Please enter a number.')
                pages_to_read = input('How many pages would you like to index? ')
        save_books_list(generate_books_list(pages_to_read))
        print()
        print('DONE! Check books.csv.')


def generate_books_list(pages):
    # use this dict format so we can easily convert it into a dataframe later
    books = {'title':[], 'link_id':[]}

    for page_num in range(pages):
        # there are 25 entries per page, starting with entry #1
        start_index = page_num * 25 + 1
        print(f'{page_num / pages * 100}% done.')
        print(f'Indexing books {start_index} - {start_index + 25}')
        # get the webpage so we can parse it
        webpage = requests.get(f'https://www.gutenberg.org/ebooks/search/?sort_order=downloads&start_index={start_index}')
        soup = BeautifulSoup(webpage.content, 'html.parser')
        # all of the data we want is contained in classes called 'booklink'
        book_links = soup.find_all(class_='booklink')
        for book_link in book_links:
            # get the title of the book
            # we don't really NEED to save the title yet (it's available in the metadata), but it's useful for reference
            title = book_link.find(class_='title').string.strip()
            # get the ID that the book is located at in Project Gutenberg
            # this can be used to access the book at https://www.gutenberg.org/ebooks/ID (replace ID with the book ID)
            # in order to get just the ID, remove the first 8 characters from the string to remove the '/ebooks/' prefix
            # this will cause issues if we ever parse something that is not an ebook, but we are in the ebooks section
            link_id = book_link.find("a", href=True)["href"].strip()[8:]
            # show the user the book
            print(f'    Indexed {title} - {link_id}')
            # add the current book to the books dictionary
            books['title'].append(title)
            books['link_id'].append(link_id)

        # don't spam web requests to quickly or our scraper will get IP blocked
        # this sleep statement will limit the number of times we query the website per second
        time.sleep(1)

    return books


def save_books_list(books_list):
    df = pd.DataFrame(books_list)
    df.to_csv('books.csv')


if __name__ == "__main__":
    main()