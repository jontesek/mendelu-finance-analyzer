import time

from sklearn import metrics


def classify_data(clf_obj, X_train, X_test, y_train, y_test):
    # Train and test model.
    start_time = time.time()
    clf_obj.fit(X_train, y_train)
    y_predicted = clf_obj.predict(X_test)
    end_time = time.time()
    total_runtime = round(end_time - start_time, 3)
    # Evaluate model
    accuracy = metrics.accuracy_score(y_test, y_predicted)
    precision = metrics.precision_score(y_test, y_predicted, average='weighted', pos_label=None)
    recall = metrics.recall_score(y_test, y_predicted, average='weighted', pos_label=None)
    f1_score = metrics.f1_score(y_test, y_predicted, average='weighted', pos_label=None)
    # Return data
    results = [round(accuracy, 4), round(precision, 4), round(recall, 4), round(f1_score, 4), total_runtime]
    return results

