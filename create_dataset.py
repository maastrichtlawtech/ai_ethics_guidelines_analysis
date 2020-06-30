import pandas as pd
import re
import os
import nltk  # import the natural language toolkit library
from io import StringIO

import pdftotext
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from nltk.corpus import stopwords
from string import punctuation
import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
#some of the texts were too long, so i had to manually increase the limit set by nlp (used when lemmatizing the texts)
nlp.max_length = 10000000

"""This function takes path to a pdf and returns a string of the whole document"""
def pdf_to_text(pdf_path):
    # Load your PDF
    with open(pdf_path, "rb") as f:
        pdf = pdftotext.PDF(f)

    # How many pages?
    #print(len(pdf))

    # Iterate over all the pages
    # for page in pdf:
    #   print(page)

    # Read some individual pages
    # print(pdf[0])
    # print(pdf[1])

    # Read all the text into one string
    one_string = "\n\n".join(pdf)
    # print("\n\n".join(pdf))

    return one_string

def get_tokens(raw,encoding='utf8'):
    #get the nltk tokens from a text
    tokens = nltk.word_tokenize(raw) #tokenize the raw UTF-8 text
    return tokens


def get_nltk_text(raw,encoding='utf8'):
    #create an nltk text using the passed argument (raw) after filtering out the commas
    #turn the raw text into an nltk text object
    no_commas = re.sub(r'[.|,|\']',' ', raw) #filter out all the commas, periods, and appostrophes using regex
    tokens = nltk.word_tokenize(no_commas) #generate a list of tokens from the raw text
    text=nltk.Text(tokens,encoding) #create a nltk text from those tokens
    return text

def filter_stopwords(text,stopword_list):
    #normalizes the words by turning them all lowercase and then filters out the stopwords
    words=[str(w).lower() for w in text] #normalize the words in the text, making them all lowercase
    #filtering stopwords
    filtered_words = [] #declare an empty list to hold our filtered words
    for word in words: #iterate over all words from the text
        if word not in stopword_list and word.isalpha() and len(word) > 1: #only add words that are not in the stopwords list, are alphabetic, and are more than 1 character
            filtered_words.append(word) #add word to filter_words list if it meets the above conditions
    filtered_words.sort() #sort filtered_words list
    return filtered_words

def get_stopswords():
    stopwords_list = set(stopwords.words('english'))

    # also add the punctuation signs to the list of stopwords
    signs = list(set(punctuation))

    stopwords_list = list(stopwords_list) + signs
    return stopwords_list

def clean_vocabulary(df):
    # clean all cases texts
    for index, doc in df.iterrows():
        print(index)
        text = doc['text']
        if isinstance(text, str):
            lem_case = nlp(text)
            lem_words = list()
            for word in lem_case:
                lem_words.append(word.lemma_)
            lem_words = filter_stopwords(lem_words, get_stopswords())
            words_str = ' '.join(map(str, lem_words))
            df.loc[index, 'text'] = words_str
        else:
            df.loc[index, 'text'] = ''
    return df


#def get_texts_for_pdf_dataset(path):
def create_dataset(path):
    names=[]
    texts=[]
    counter =0
    for doc in os.listdir(path):
        names.append(doc)
        print(doc)
        try:
            text = pdf_to_text(path+str(doc))
        except:
            print("FAILED : ")
            text=''
        texts.append(text)
        #print(text)
        counter+=1
    print(counter)

    full_text_dataset = pd.DataFrame({'name':names,'text':texts})
    return full_text_dataset


#path to the folder where the pdf documents of all the ethical guidelines documents are stored
path = "data/AI ETHICS DOCUMENTS (PDF)/"

#create and store full text dataset
full_text_dataset = create_dataset(path)
full_text_dataset.to_csv("data/full_text_dataset.csv", index=False)

#create and store lemmatized datasets
full_text_dataset = pd.read_csv("data/full_text_dataset.csv")
#create the lemmatized version of the dataset
lemmatized_dataset = clean_vocabulary(full_text_dataset)
lemmatized_dataset.to_csv("data/lemmatized_dataset.csv")
