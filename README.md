# Setting Up the Dataset
1. Run `book-downloader.py`.
2. When asked if you would like to generate a books.csv file, select 'y'.
3. Select the number of website pages that you would like to scan. This will determine the size of your dataset.
4. Wait for books to be downloaded.
5. Book data will be stored in `books.csv` and the corresponding book will be in `books/[catalog_number]/[catalog_number]_rawdata.txt`. 

  NOTE: Book text is not stored in the CSV file because this would cause memory issues for a large dataset.
  
  **TODO: Download book metadata from website and add to CSV**
  
# Tidying the Dataset
- **TODO: Make a script to remove useless text from the .txt (header, title, author, release date, and licensing information at the end of the file). This will probably require some regular expressions or pattern matching.**
- **TODO: Make a script to split the chapters into individual text files (or do we just want the whole plaintext without chapters at all? - looking for input on this.)**
