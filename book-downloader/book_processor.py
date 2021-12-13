'''
Book Processor

A collection of functions that are used to process books (i.e. remove header/footer, tokenize, vectorize, etc.)
'''

import fileinput
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re
import os

def remove_header_footer(inpBookStr):

    '''
    Removes the header and footer of the book string based on loops
    WARNING: There is a chance that the book header/footer varies in such a way that the split does not happen appropriately.
        It is worth double-checking to make sure the book was pre-processed by searching for a string normally found in the header/footer
        Currently this processor handles 2 types of header/footer formats encountered
    '''


    # using a loop to trim off the front and back of the ebook
    # this could be done using a regex but it takes too darn long
    splitter = 3


    # there should be four instances of "***", get rid of the first instance because it can get confusing if left in, as the preceding text is the
    #  title of the book and changes, so no way to appropriately match on the second *** until the first *** is removed
    #  this way we don't end up starting the book at the wrong spot
    while splitter < len(inpBookStr) + 20:

        if (inpBookStr[splitter] == '*' and inpBookStr[splitter + 4] == 'S' and inpBookStr[splitter + 8]) == 'T' or \
            (inpBookStr[splitter] == '*' and inpBookStr[splitter + 3] == 'S' and inpBookStr[splitter + 7] == 'T'):
            inpBookStr = inpBookStr[(splitter + 8):]
            break

        splitter += 1

    
    # now it is easier to split out the book using the remaining header instance
    splitter = 3

    while splitter < len(inpBookStr) + 20:

        if inpBookStr[splitter] == '*' and inpBookStr[splitter - 1] == '*' and inpBookStr[splitter - 2] == '*':
            inpBookStr = inpBookStr[(splitter + 1):]
            break

        splitter += 1


    # now do the same working backwards to get the end of the book proper
    splitter = len(inpBookStr) - 33

    while splitter > 20:

        if inpBookStr[splitter:splitter + 10] == "*** END OF" or \
            inpBookStr[splitter:splitter + 9] == "***END OF":
            
            inpBookStr = inpBookStr[:(splitter - 1)]
            break

        splitter -= 1


    # strip and lowercase book text
    outBookStr = inpBookStr.strip()
    outBookStr = outBookStr.lower()

    return outBookStr


# function to lemmatize a book file
def lemmatizeFile(inpData):

    outText = ""
    lemmatizer = WordNetLemmatizer()

    # get list of sentences
    a_list = sent_tokenize(inpData)

    processed_features = []

    for sentence in range(0, len(a_list)):

        # Remove all the special characters
        processed_feature = re.sub(r'\W', ' ', str(a_list[sentence]))

        # Substituting multiple spaces with single space
        processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

        processed_features.append(processed_feature)


    for sentence in processed_features:

        currentSentence = ""

        # Tokenize: Split the sentence into words
        word_list = word_tokenize(sentence)

        for i in word_list:

            lemmaSent = lemmatizer.lemmatize(i)

            currentSentence += str(lemmaSent)

        # Lemmatize list of words and join
        lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])

        # add sentence to output text

        outText+=str(' ' + lemmatized_output)

    return outText
    

# get path of all books
filename = os.getcwd() + '\\books\\'


# set up list for storing file addresses
filelist = []

# store file address by running through directory
for root, dirs, files in os.walk(filename):
	for file in files:
        #append the file name to the list
		filelist.append(os.path.join(root,file))


# open each file in the list and lemmatize
for fileName in filelist:

    with open(fileName, 'r', encoding="utf-8") as f:
        data = f.read().rstrip()

    newData = lemmatizeFile(data)

    # WARNING: Enabling this line of code will delete the old non-lemmatized file. USE WITH CAUTION
    #os.remove(fileName)

    outFile = fileName[:-4]

    # save as a different file type to mark the file has been lemmatized
    outFile += "-LEMMA.txt"

    # save as a new file
    with open(outFile, "w", encoding="utf-8") as text_file:
        text_file.write(newData)

    


