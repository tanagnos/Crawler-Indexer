import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string


class Index:
    the_dict = {}  # in this dictionary we save the inverted index in memory and we update it.
    words_of_doc = 0   # the length of the text of the current URL will be saved here

    def __init__(self, text, url):
        self.current_text = list(self.preprocess(text))  # update the text after preprocessing.
        self.the_dictionary(self.current_text, url)  # update the dictionary(inverted index).

    def __iter__(self):
        return (x for x in self.current_text)

    @staticmethod
    def preprocess(text):
        text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuations
        text = re.sub(r'[^\w]', ' ', text)  # remove rest symbols that are not punctuations
        text = re.sub(r'\d+', '', text)  # remove numbers
        text = re.sub(r'[^\x00-\x7f]', r'', text)  # keep only latin characters
        text = text.lower()  # all letters lowercase

        # remove stopwords
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)

        text = [w for w in word_tokens if not w in stop_words]
        text = []
        for w in word_tokens:
            if w not in stop_words:
                text.append(w)

        # Lemmatization(root of the word)
        lemmatizer = WordNetLemmatizer()
        for counter, word in enumerate(text):
            text[counter] = lemmatizer.lemmatize(word)

        text.sort()  # sort the words alphabetically
        Index.words_of_doc = len(text)

        return text

    # it keeps the info of the words that are found with the frequency only for the current URL.
    @staticmethod
    def docs_dictionary(text):
        d = dict()

        for word in text:
            if word in d:  # if the word found already update the frequency.
                d[word] = d[word] + 1
            else:  # else save we found for the first time.
                d[word] = 1
        return d

    # this is the inverted index.We update the_dict after we scan and preprocess the text that the current URL contains.
    @staticmethod
    def the_dictionary(text, page_url):
        temp_dict = Index.docs_dictionary(text)  # this is a temp dictionary that calls the docs_dictionary to inform
        # us for the words this URL contains
        for x, y in temp_dict.items():  # scan every word in this URL
            if x not in Index.the_dict:  # and check if there are already in the inverted index.
                Index.the_dict[x] = [y, page_url, Index.words_of_doc]  # if they are not then update the inverted index
                # with the first time found word and this URL.
            else:  # if the word was in the inverted index
                appe = [y, page_url, Index.words_of_doc]  # appe from append
                if len(Index.the_dict[x]) == 2:  # and if was found before only once
                    Index.the_dict[x] = [Index.the_dict[x], appe]  # update for the second time we found it.
                else:  # just append it.
                    Index.the_dict[x].append(appe)
        Index.the_dict = dict(sorted(Index.the_dict.items()))  # every time sort the inverted index.
