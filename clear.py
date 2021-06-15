import json

import nltk
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english")


def tokenize_and_stem(text):
    # 按句子进行标记
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # 过滤掉任何不包含字母的标记
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def main():
    articles = None
    with open('articles.json', 'r', encoding='utf-8') as fin:
        articles = json.loads(fin.read())
    # print(articles)

    abstracts = [it['abstract'] for it in articles]
    # print(abstracts)
    tv = TfidfVectorizer(max_df=0.4, max_features=200000,
                         min_df=0.3, stop_words='english',
                         use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))

    tv_fit = tv.fit_transform(abstracts)
    # terms = tv.get_feature_names()
    dist = 1 - cosine_similarity(tv_fit)
    np.savetxt('test.csv', dist, delimiter=',')


if __name__ == '__main__':
    main()
