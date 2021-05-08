"""
Preliminary assumptions:
- file with param is in the given schema:
category; word1:positive/negative, word2:positive/negative...
- there are no typos in input files
"""
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# a tool for stemming words needs to be declared to make it work
ps = PorterStemmer()


def process_word(word):
    word = ps.stem(word)  # stem words
    word = word.lower()  # make words lowercase
    word = word.strip()  # strip it both sides
    return word


if __name__ == '__main__':
    categories = {}
    with open('categories_list_txt.txt', 'r') as params:
        for line in params.readlines():
            # split it int categories and words
            cat = line[:line.find('; ')]
            words = line[line.find('; ') + 2:]
            words = words.split(', ')

            # create a dict for words
            dict_words = {}
            for word in words:
                w = word.split(':')
                w[1] = w[1].replace('\n', '')
                dict_words[w[0]] = w[1]
            categories[cat] = dict_words

    with open('test_text_input.txt', 'r') as input_text:
        in_txt = input_text.read()

    in_txt_tokens_words = word_tokenize(in_txt)

    # define variables and dictionares to store information of all collected data
    all_positive = 0
    all_negative = 0
    cat_occurence = {}
    param_occurence = {}
    for cat in categories.keys():
        # define variables and dictionares to store information of categories data
        cat_occurence[cat] = 0
        cat_positive = 0
        cat_negative = 0
        print(f'=== {cat.upper()} ===')
        for param in categories[cat].keys():
            # define variables and dictionares to store information of parameter data
            param_occurence[param] = 0
            processed_word_params = process_word(param)  # process param
            for token in in_txt_tokens_words:
                processed_word_input = process_word(token)  # proces token out of text
                if processed_word_params == processed_word_input:
                    cat_occurence[cat] += 1
                    param_occurence[param] += 1
                    if categories[cat][param] == 'positive':
                        all_positive += 1
                        cat_positive += 1
                    else:
                        all_negative += 1
                        cat_negative += 1
            # analysys after param loop ends
            # prints occurences of param
            print(f'"{param}" occurence: {param_occurence[param]}')
        # analysys after category loop ends
        # prints occurences of param and number of positive or negative ones
        print(f' >> {cat.upper()} occurence: {cat_occurence[cat]}')
        print(f' >> {cat.upper()} positives: {cat_positive}, negatives: {cat_negative}')
        # creates and then prints
        cat_pos_neg = cat_positive + cat_negative
        if cat_positive != 0:
            print(f' >> {cat_positive / cat_pos_neg * 100}% of positives')
        if cat_negative != 0:
            print(f' >> {cat_negative / cat_pos_neg * 100}% of negatives')
        print('===============\n')  # separates categories with 15 equal sings and new line

    # prints final results
    print('\n\n')
    print('=== FINAL RESULTS ===')

    # occurences of words by categories
    numbers = [cat_occurence[cat] for cat in cat_occurence]  # list comprahension

    max = max(numbers)

    most_occured_cat = [cat for cat in cat_occurence if cat_occurence[cat] == max]

    """ to samo co w linijce 92:
    most_occured = []
    for cat in cat_occurence:
        if cat_occurence[cat] == max:
            most_occured.append(cat)
    """

    print('Mostly occuring:')
    for moc in most_occured_cat:
        print(f'{moc} occured {max} times')

    # positive/negative for all content
    all_pos_neg = all_positive + all_negative
    ## if all_positive != 0:
    print(f'{all_positive / all_pos_neg * 100}% of positives')
    ## if all_negative != 0:
    print(f'{all_negative / all_pos_neg * 100}% of negatives')
