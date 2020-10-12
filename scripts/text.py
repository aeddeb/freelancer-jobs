'''
Date: 2020-09-10
Author: Ali Eddeb

Purpose: Store functions used to vectorize text fields.
'''

#IMPORT LIBRARIES
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import string
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')
ENGLISH_STOP_WORDS = stopwords.words('english')

def spl_tokenizer(sentence):
    '''
    Tokenizer with following specs:
    - removes english stopwords
    - removes punctuation
    - lemmatizes words
    '''
    for punctuation_mark in string.punctuation:
        # Remove punctuation and set to lower case
        sentence = sentence.replace(punctuation_mark,'').lower()

    # split sentence into words
    listofwords = sentence.split(' ')
    listoflemmatized_words = []
        
    # Remove stopwords and any tokens that are just empty strings
    for word in listofwords:
        if (not word in ENGLISH_STOP_WORDS) and (word!=''):
            # Lemmatize words
            token = WordNetLemmatizer().lemmatize(word)            
            '''
            #add t_ prefix to indicate word is from title or d_ if from description
            try:
                if tfidf.type == 'job_title':
                    token = 't_' + token
                elif tfidf.type == 'description':
                    token = 'd_' + token
            except:
                pass
            '''
            #append token to list
            listoflemmatized_words.append(token)

    return listoflemmatized_words



def sps_tokenizer(sentence):
    '''
    Tokenizer with following specs:
    - removes english stopwords
    - removes punctuation
    - stems words
    '''
    for punctuation_mark in string.punctuation:
        # Remove punctuation and set to lower case
        sentence = sentence.replace(punctuation_mark,'').lower()

    # split sentence into words
    listofwords = sentence.split(' ')
    listofstemmed_words = []
    #instantiate stemmer
    stemmer = PorterStemmer() 

    # Remove stopwords and any tokens that are just empty strings
    for word in listofwords:
        if (not word in ENGLISH_STOP_WORDS) and (word!=''):
            # Lemmatize words
            token = stemmer.stem(word)  
            '''
            #add t_ prefix to indicate word is from title or d_ if from description
            try:
                if tfidf.type == 'job_title':
                    token = 't_' + token
                elif tfidf.type == 'description':
                    token = 'd_' + token
            except:
                continue
            '''
            #append token to list
            listofstemmed_words.append(token)

    return listofstemmed_words




def bagofwords(dataframe_column, tokenizer, min_df=0.02, max_df=0.8, ngram_range=(1,1)):
    '''
    #0. For tokenization, need to determine what prefix (t_ or d_) to add to each token
    #To do so, retrieve the name of the column from which the tokens are generated
    column_name = dataframe_column.name
    #Next, assign an attribute (called type) to the tfidf function to indicate if the tokens are from title or description
    if column_name == 'job_title':
        tfidf.type = 'job_title'
    elif column_name == 'description':
        tfidf.type = 'description'
    else:
        tfidf.type = None
    '''
    # 1. Instantiate  (stop_words='english')
    vectorizer = CountVectorizer(min_df = min_df, max_df = max_df, tokenizer = tokenizer, ngram_range = ngram_range)
    
    # 2. Fit 
    vectorizer.fit(dataframe_column)
    
    # 3. Transform
    reviews_tokenized = vectorizer.transform(dataframe_column)
    
    # We extract the information and put it in a data frame
    tokens = pd.DataFrame(columns=vectorizer.get_feature_names(), data=reviews_tokenized.toarray())
    
    return tokens
