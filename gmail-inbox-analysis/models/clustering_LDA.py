#!/Users/pedrohserrano/.pyenv/versions/3.4.2/bin/python3.4

import sys

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

import numpy as np


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()



n_features = 1000 # belive that max number of words
n_topics = 5
n_top_words = 20

if __name__ == "__main__":
    lineas=[]
    while True:
        linea = sys.stdin.readline()
        if not linea:
            break
        lineas.append(linea)
    data_samples = np.array(lineas)

    n_samples = len(data_samples)

    # Use tf-idf features for NMF.
    print("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                       max_features=n_features,
                                       stop_words='english')
    #t0 = time()
    tfidf = tfidf_vectorizer.fit_transform(data_samples)
    #print("done in %0.3fs." % (time() - t0))

    # Use tf (raw term count) features for LDA.
    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                    max_features=n_features,
                                    stop_words='english')
    #t0 = time()
    tf = tf_vectorizer.fit_transform(data_samples)
    #print("done in %0.3fs." % (time() - t0))

    # Fit the NMF model
    print("Fitting the NMF model with tf-idf features, "
          "n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    #t0 = time()
    nmf = NMF(n_components=n_topics, random_state=1,
              alpha=.1, l1_ratio=.5).fit(tfidf)
    #print("done in %0.3fs." % (time() - t0))

    print("\nTopics in NMF model:")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, n_top_words)

    print("Fitting LDA models with tf features, "
          "n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    #t0 = time()
    lda.fit(tf)
    #print("done in %0.3fs." % (time() - t0))

    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)