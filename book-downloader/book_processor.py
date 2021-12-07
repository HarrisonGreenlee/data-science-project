'''
Book Processor

A collection of functions that are used to process books (i.e. remove header/footer, tokenize, vectorize, etc.)
'''



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
