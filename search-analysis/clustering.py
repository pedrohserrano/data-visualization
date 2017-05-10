#!/usr/local/Cellar/python3/3.5.1/bin/python3

"""
=======================================
Clustering text documents using k-means
=======================================

This is an example showing how the scikit-learn can be used to cluster
documents by topics using a bag-of-words approach. This example uses
a scipy.sparse matrix to store the features instead of standard numpy arrays.

Two feature extraction methods can be used in this example:

  - TfidfVectorizer uses a in-memory vocabulary (a python dict) to map the most
    frequent words to features indices and hence compute a word occurrence
    frequency (sparse) matrix. The word frequencies are then reweighted using
    the Inverse Document Frequency (IDF) vector collected feature-wise over
    the corpus.

  - HashingVectorizer hashes word occurrences to a fixed dimensional space,
    possibly with collisions. The word count vectors are then normalized to
    each have l2-norm equal to one (projected to the euclidean unit-ball) which
    seems to be important for k-means to work in high dimensional space.

    HashingVectorizer does not provide IDF weighting as this is a stateless
    model (the fit method does nothing). When IDF weighting is needed it can
    be added by pipelining its output to a TfidfTransformer instance.

Two algorithms are demoed: ordinary k-means and its more scalable cousin
minibatch k-means.

Additionally, latent semantic analysis can also be used to reduce dimensionality
and discover latent patterns in the data.

It can be noted that k-means (and minibatch k-means) are very sensitive to
feature scaling and that in this case the IDF weighting helps improve the
quality of the clustering by quite a lot as measured against the "ground truth"
provided by the class label assignments of the 20 newsgroups dataset.

This improvement is not visible in the Silhouette Coefficient which is small
for both as this measure seem to suffer from the phenomenon called
"Concentration of Measure" or "Curse of Dimensionality" for high dimensional
datasets such as text data. Other measures such as V-measure and Adjusted Rand
Index are information theoretic based evaluation scores: as they are only based
on cluster assignments rather than distances, hence not affected by the curse
of dimensionality.

Note: as k-means is optimizing a non-convex objective function, it will likely
end up in a local optimum. Several runs with independent random init might be
necessary to get a good convergence.

"""

# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Lars Buitinck
# License: BSD 3 clause

# from __future__ import print_function

# from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

import json
from scipy.spatial.distance import cdist
from scipy.cluster.vq import kmeans,vq
from sklearn.cluster import KMeans, MiniBatchKMeans
import matplotlib.pyplot as plt

import logging
from optparse import OptionParser
import sys

import numpy as np

if __name__ == "__main__":
    lineas=[]
    while True:
        linea = sys.stdin.readline()
        if not linea:
            break
        lineas.append(linea)
    data = np.array(lineas)


    # Display progress logs on stdout
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    # parse commandline arguments
    op = OptionParser()
    op.add_option("--lsa",
                  dest="n_components", type="int",
                  help="Preprocess documents with latent semantic analysis.")
    op.add_option("--no-minibatch",
                  action="store_false", dest="minibatch", default=False,
                  help="Use ordinary k-means algorithm (in batch mode).")
    op.add_option("--no-idf",
                  action="store_false", dest="use_idf", default=True,
                  help="Disable Inverse Document Frequency feature weighting.")
    op.add_option("--use-hashing",
                  action="store_true", default=False,
                  help="Use a hashing feature vectorizer")
    op.add_option("--n-features", type=int, default=10000,
                  help="Maximum number of features (dimensions)"
                       " to extract from text.")
    op.add_option("--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Print progress reports inside k-means algorithm.")

    op.add_option("--n-clusters", type=int, default=5,
                  help="Number of clusters to extract from text.")

    print(__doc__)
    op.print_help()

    (opts, args) = op.parse_args()
    if len(args) > 0:
        op.error("this script takes no arguments.")
        sys.exit(1)


    ###############################################################################
    # Load some categories from the training set
    #categories = [
    #    'alt.atheism',
    #    'talk.religion.misc',
    #    'comp.graphics',
    #    'sci.space',
    #]
    # Uncomment the following to do the analysis on all the categories
    #categories = None

    print("Loading data:")
    #print(categories)

    #dataset = fetch_20newsgroups(subset='all', categories=categories,
    #                             shuffle=True, random_state=42)

    

    print("%d querys" % len(data))
    #print("%d categories" % len(dataset.target_names))
    print()

    #labels = dataset.target
    #true_k = np.unique(labels).shape[0]
    true_k = opts.n_clusters # este es un parametro a estimar

    print("Extracting features from the training dataset using a sparse vectorizer")
    if opts.use_hashing:
        if opts.use_idf:
            # Perform an IDF normalization on the output of HashingVectorizer
            hasher = HashingVectorizer(n_features=opts.n_features,
                                       stop_words='english', non_negative=True,
                                       norm=None, binary=False)
            vectorizer = make_pipeline(hasher, TfidfTransformer())
        else:
            vectorizer = HashingVectorizer(n_features=opts.n_features,
                                           stop_words='english',
                                           non_negative=False, norm='l2',
                                           binary=False)
    else:
        vectorizer = TfidfVectorizer(max_df=0.5, max_features=opts.n_features,
                                     min_df=2, stop_words='english',
                                     use_idf=opts.use_idf)
    X = vectorizer.fit_transform(data)

    print("n_samples: %d, n_features: %d" % X.shape)
    print()

    if opts.n_components:
        print("Performing dimensionality reduction using LSA")
        # Vectorizer results are normalized, which makes KMeans behave as
        # spherical k-means for better results. Since LSA/SVD results are
        # not normalized, we have to redo the normalization.
        svd = TruncatedSVD(opts.n_components)
        normalizer = Normalizer(copy=False)
        lsa = make_pipeline(svd, normalizer)

        X = lsa.fit_transform(X)

        explained_variance = svd.explained_variance_ratio_.sum()
        print("Explained variance of the SVD step: {}%".format(
            int(explained_variance * 100)))

        print()


    ###############################################################################
    # Do the actual clustering

    # A MAJOR DRAWBACK IS THAT THE NUMBER OF CLUSTERS HAS TO BE SEEN ON THE GRAPHIC
    ##### cluster data into K=1..10 clusters #####
    K = range(1,10)

    if opts.minibatch:
        KM = [MiniBatchKMeans(n_clusters=k, verbose=opts.verbose).fit(X)  for k in K]
    else:
        KM = [KMeans(n_clusters=k, max_iter=100, verbose=opts.verbose).fit(X) for k in K]

    #KM = [kmeans(X,k) for k in K]

    #print("Clustering sparse data with {}".format(km))
    #km.fit(X)
    #print()


    # scipy.cluster.vq.kmeans
    centroids = [metodo.cluster_centers_ for metodo in KM]   # cluster centroids kmeans.cluster_centers_
    # centroids = [cent for (cent,var) in KM]
    #avgWithinSS = [var for (cent,var) in KM] # mean within-cluster sum of squares



    # alternative: scipy.cluster.vq.vq
    #Z = [vq(X,cent) for cent in centroids]
    #avgWithinSS = [sum(dist)/X.shape[0] for (cIdx,dist) in Z]

    # alternative: scipy.spatial.distance.cdist
    #print(centroids)

    D_k = [cdist(X.todense(), cent, 'euclidean') for cent in centroids]
    
    cIdx = [np.argmin(D,axis=1) for D in D_k]
    dist = [np.min(D,axis=1) for D in D_k]
    avgWithinSS = [sum(d)/X.todense().shape[0] for d in dist]

    ##### plot ###
    kIdx = 5

    # elbow curve
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(K, avgWithinSS, 'b*-')
    ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
        markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average within-cluster sum of squares')
    plt.title('Elbow for KMeans clustering')

    # scatter plot
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # #ax.scatter(X[:,2],X[:,1], s=30, c=cIdx[k])
    # clr = ['b','g','r','c','m','y','k']

    # for i in range(K[kIdx]):
    #     ind = (cIdx[kIdx]==i)
    #     ax.scatter(X[ind,2],X[ind,1], s=30, c=clr[i], label='Cluster %d'%i)
    # plt.xlabel('Petal Length')
    # plt.ylabel('Sepal Width')
    # plt.title('Iris Dataset, KMeans clustering with K=%d' % K[kIdx])
    # plt.legend()

    plt.show()
    

    '''
    # it requires a clasified dataset
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
    print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
    print("Adjusted Rand-Index: %.3f"
          % metrics.adjusted_rand_score(labels, km.labels_))
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X, km.labels_, sample_size=1000))

    print()
    '''

    
    if not opts.use_hashing:
        print("Top terms per cluster:")

        if opts.n_components:
            original_space_centroids = svd.inverse_transform(KM[kIdx].cluster_centers_)
            order_centroids = original_space_centroids.argsort()[:, ::-1]
        else:
            order_centroids = KM[kIdx].cluster_centers_.argsort()[:, ::-1]

        terms = vectorizer.get_feature_names()
        for i in range(K[kIdx]):
            print("Cluster %d:" % i, end='')
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind], end='')
            print()
    