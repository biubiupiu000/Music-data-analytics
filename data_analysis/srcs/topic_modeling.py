# -*- coding:utf-8 -*-

import time
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from gensim import models, corpora
import re
import collections

def main():
    topic_model()


def topic_model():

    #read stopwords
    stopwords = {}
    with open('Data/stops.txt', 'r') as f:
        data = f.readlines()
        for i in data:
            stopwords[re.sub(r'\n', '', i)] = 0
    f.close()
    print('start biography text')
    texts = []
    lemmatizer = WordNetLemmatizer()
    text = pd.read_csv('Data/text_clean.csv')
    removal=re.compile(r'(music|musician|singer|musical|song|year)')
    for i in range(text.shape[0]):
        try:
            words = text.loc[i]['biography'].casefold()
        except:
            continue
        if words!='no content':
            # words = re.sub(removal, '', words)
            words = words.split()
            words = [i for i in words if '=' not in i]
            words=[i for i in words if not re.match(removal,i)]
            words = [re.sub(r'\W', '', i) for i in words if not re.search('http', i)]
            words = [i for i in words if i not in stopwords]
            words = [lemmatizer.lemmatize(i) for i in words if i != '' and len(i) > 1]
            texts.append(words)
    print('preprocessing complete')
    print('have all corpus:',len(texts))
    print('*' * 50)
    terms_dict = corpora.Dictionary(texts)
    corpus = [terms_dict.doc2bow(text) for text in texts]
    lda=models.LdaModel(corpus=corpus,id2word=terms_dict,iterations=30,num_topics=50,passes=10)
    topics=lda.print_topics(num_topics=5)
    print('top5 topics')
    print('*' * 50)
    np.save('topics_bio.npy',topics)
    for topic in topics:
        print(topic)
    textss=lda.get_document_topics(corpus)

    a=collections.Counter([sorted(i,reverse=True,key=lambda x:x[1])[0][0] for i in textss])
    print('top10 distribution of docs')
    print('*' * 50)
    distributions=[]
    num=0
    for i in a:
        distributions.append(lda.show_topic(i))
        print(lda.show_topic(i))
        num+=1
        if num==10:
            break
    np.save('dis_bio.npy', distributions)
    coherence=models.CoherenceModel(model=lda,texts=texts,dictionary=terms_dict,coherence='u_mass')
    coherence_lda=coherence.get_coherence()
    print('the coherence score is:',coherence_lda)
    print('*'*50)
    print('start influence text')
    texts=[]
    removal = re.compile(r'(music|musician|singer|musical|song|influenced|influence|influencial)')
    for i in range(text.shape[0]):

        words = text.loc[i]['influence'].casefold()
        if words != 'no content':
            # words = re.sub(removal, '', words)
            words = words.split()
            words = [i for i in words if '=' not in i]
            words=[i for i in words if not re.match(removal,i)]
            words = [re.sub(r'\W', '', i) for i in words if not re.search('http', i)]
            words = [i for i in words if i not in stopwords]
            words = [lemmatizer.lemmatize(i) for i in words if i != '' and len(i) > 1]
            texts.append(words)
    print('preprocessing complete')
    print('have all corpus:',len(texts))
    print('*' * 50)
    terms_dict = corpora.Dictionary(texts)
    corpus = [terms_dict.doc2bow(text) for text in texts]
    lda=models.LdaModel(corpus=corpus,id2word=terms_dict,iterations=30,num_topics=50,passes=10)
    topics=lda.show_topics(formatted=True,num_topics=2)
    print('top2 topics')
    print('*' * 50)
    np.save('topics_inf.npy', topics)
    for topic in topics:
        print(topic)
    textss = lda.get_document_topics(corpus)

    a = collections.Counter([sorted(i, reverse=True, key=lambda x: x[1])[0][0] for i in textss])
    print('top3 distribution of docs')
    print('*' * 50)
    distributions = []
    num = 0
    for i in a:
        distributions.append(lda.show_topic(i))
        print(lda.show_topic(i))
        num += 1
        if num == 3:
            break
    np.save('dis_inf.npy', distributions)
    coherence = models.CoherenceModel(model=lda, texts=texts, dictionary=terms_dict, coherence='u_mass')
    coherence_lda = coherence.get_coherence()
    print('the coherence score is:',coherence_lda)
if __name__ == '__main__':
    main()