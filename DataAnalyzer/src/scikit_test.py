import time

from sklearn.datasets import load_svmlight_file
from sklearn.externals.joblib import Memory

from sklearn import cross_validation
from sklearn import metrics

from sklearn import svm
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

mem = Memory("C:\\text_mining\cache")

@mem.cache
def get_data():
    data = load_svmlight_file("C:\\text_mining\outputs\\tweet_tp_50k.dat")
    return data[0], data[1]     # X, y

classifiers = [
    ['NB multi', MultinomialNB(alpha=1.0)],
    ['NB berno', BernoulliNB()],
    ['MaxEnt', LogisticRegression()],
    ['CART', tree.DecisionTreeClassifier()],
    ['RandForest', RandomForestClassifier()],
    #['KNN', KNeighborsClassifier(3)],
    ['SVM', svm.SVC(verbose=0, kernel='rbf', cache_size=1024)],  # svm.SVC(verbose=2, kernel='poly', degree=3)
]

# Load data file and print info.
#data = load_svmlight_file("C:\\text_mining\outputs\\article_tp_15k_10df.dat")
data = load_svmlight_file("C:\\text_mining\outputs\\tweet_100k_3gf.dat")
print('===Dataset information===')
print('Number of samples: %d, number of features: %d') % (data[0].shape[0], data[0].shape[1])
# Create data sets.
# http://scikit-learn.org/stable/modules/cross_validation.html
X_train, X_test, y_train, y_test = cross_validation.train_test_split(data[0], data[1], test_size=0.35, random_state=4)

# Classify data with all classifiers.
for (name, clf) in classifiers:
    print('===%s===') % name
    start_time = time.time()

    clf.fit(X_train, y_train)

    y_predicted = clf.predict(X_test)

    end_time = time.time()
    print('Runtime: %s seconds') % round(end_time - start_time, 3)
    # http://scikit-learn.org/stable/modules/model_evaluation.html
    #print(metrics.classification_report(y_test, y_predicted, digits=4))
    #print(metrics.confusion_matrix(y_test, y_predicted, [1, 2]))
    accuracy = metrics.accuracy_score(y_test, y_predicted)
    f1_score = metrics.f1_score(y_test, y_predicted, average='weighted', pos_label=None)
    precision = metrics.precision_score(y_test, y_predicted, average='weighted', pos_label=None)
    recall = metrics.recall_score(y_test, y_predicted, average='weighted', pos_label=None)
    print('Accuracy: %s') % (round(accuracy, 4) * 100)
    print('Precision %s, Recall %s, F1 %s') % (round(precision, 4), round(recall, 4), round(f1_score, 4))
    #break



