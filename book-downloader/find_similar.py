# finds similar books using pre-calculated metrics
import pandas as pd
df = pd.read_csv('books_with_metrics.csv')

# normalize metrics
df['flesch_kincaid'] = (df['flesch_kincaid'] - df['flesch_kincaid'].min()) / (df['flesch_kincaid'].max() - df['flesch_kincaid'].min())
df['adi'] = (df['adi'] - df['adi'].min()) / (df['adi'].max() - df['adi'].min())
df['word_count'] = (df['word_count'] - df['word_count'].min()) / (df['word_count'].max() - df['word_count'].min())

book_to_match = input('Enter the title of your favorite book: ')
while book_to_match not in df['title'].values:
    print(f'Could not find {book_to_match}. Please enter a book that is within the dataset.')
    book_to_match = input('Enter the title of your favorite book: ')

book_to_match = df.loc[df['title'] == book_to_match].iloc[0]
book_to_match_flesch_kincaid = book_to_match['flesch_kincaid']
book_to_match_adi = book_to_match['adi']
book_to_match_word_count = book_to_match['word_count']

df["euclidean_distance_from_book_to_match"] = (book_to_match_flesch_kincaid - df['flesch_kincaid'])**2 + (book_to_match_adi - df['adi'])**2 + (book_to_match_word_count - df['word_count'])**2
df.sort_values(by=['euclidean_distance_from_book_to_match'], inplace=True)
print()
print('TOP 10 MATCHES:')
print(df.head(n=10).to_string(index=False))