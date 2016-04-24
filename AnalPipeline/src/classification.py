import time

from sklearn import metrics
from sklearn.externals import joblib


### SCIKIT LEARN

def classify_data(clf_obj, X_train, X_test, y_train, y_test, save_model_filepath=False):
    # Train model.
    start_time = time.time()
    clf_obj.fit(X_train, y_train)
    train_runtime = round(time.time() - start_time, 6)
    # If desired, save model to disk.
    if save_model_filepath:
        joblib.dump(clf_obj, save_model_filepath)
    # Test model.
    start_time = time.time()
    y_predicted = clf_obj.predict(X_test)
    test_runtime = round(time.time() - start_time, 6)
    # Evaluate model.
    accuracy = metrics.accuracy_score(y_test, y_predicted)
    precision = metrics.precision_score(y_test, y_predicted, average='weighted', pos_label=None)
    recall = metrics.recall_score(y_test, y_predicted, average='weighted', pos_label=None)
    f1_score = metrics.f1_score(y_test, y_predicted, average='weighted', pos_label=None)
    # Get number of tested samples for class 1 and 2.
    conf_matrix = metrics.confusion_matrix(y_test, y_predicted, labels=[1, 2])
    cl_1_count = conf_matrix[0][0] + conf_matrix[0][1]
    cl_2_count = conf_matrix[1][0] + conf_matrix[1][1]
    # Return data.
    tested_counts = [cl_1_count, cl_2_count]
    results = [accuracy, precision, recall, f1_score, train_runtime, test_runtime]
    eval_data = [y_test, y_predicted]
    return results, eval_data, tested_counts


### LOGGING

def update_log_header(log_filepath, input_filename, n_samples, n_features):
    # Open file.
    log_file = open(log_filepath, 'a')
    # Write header line.
    log_file.write('======INPUT: %s======\n' % input_filename)
    # Write dataset info.
    log_file.write('====DATASET info====\n')
    log_file.write('Number of samples / features: %d, %d \n' % (n_samples, n_features))
    # OK
    log_file.close()


def update_log_algo(filepath, algo_name, results, eval_data, error_string=None):
    # Open file.
    log_file = open(filepath, 'a')
    log_file.write('====ALGO: %s====\n' % algo_name)
    # If present, write error string.
    if error_string:
        log_file.write('>>PROCESS ERROR: %s \n' % error_string)
        log_file.close()
        return True
    # Write list summary.
    log_file.write(str([round(x, 6) for x in results]) + '\n')
    # Write accuracy and runtime.
    log_file.write('Accuracy: %s\n' % results[0])
    log_file.write('Train / test time: %s, %s [s]\n' % (results[-2], results[-1]))
    # Write info.
    y_test = eval_data[0]
    y_predicted = eval_data[1]
    log_file.write('==Classification report==\n')
    log_file.write(metrics.classification_report(y_test, y_predicted, digits=6, labels=[1, 2]))
    log_file.write('==Confusion matrix==\n')
    log_file.write(str(metrics.confusion_matrix(y_test, y_predicted, labels=[1, 2])) + '\n')
    # Close file.
    log_file.close()
