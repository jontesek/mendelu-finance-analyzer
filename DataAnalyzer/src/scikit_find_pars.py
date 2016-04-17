import time

from sklearn.datasets import load_svmlight_file

from sklearn import cross_validation
from sklearn import metrics

from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC

if __name__ == "__main__":
    # Load data file and print info.
    #data = load_svmlight_file("C:\\text_mining\outputs\\article_tp_15k_10df.dat")
    data = load_svmlight_file("C:\\text_mining\outputs\\tweet_100k_3gf.dat")
    print('===Dataset information===')
    print('Number of samples: %d, number of features: %d') % (data[0].shape[0], data[0].shape[1])

    # Create data sets.
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(data[0], data[1], test_size=0.5)

    # Find best params for SVM.
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
                        {'kernel': ['poly'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000], 'degree': [2, 3, 4]},
                        {'kernel': ['sigmoid'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

    scores = ['accuracy', 'precision_weighted', 'recall_weighted']

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(SVC(C=1, cache_size=4000), tuned_parameters, cv=2, scoring=score, n_jobs=1)
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        for params, mean_score, scores in clf.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean_score, scores.std() * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print(metrics.classification_report(y_true, y_pred))
        print()


