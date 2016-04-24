###########
# Imports
###########
import datetime
import os

from sklearn.datasets import load_svmlight_file
from sklearn import cross_validation

from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm

from src.TextWriter import TextWriter
import src.file_processing as my_fp
import src.classification as my_clf

########
# Parameter definitions
########

# Define basic file paths.
base_input_dir = os.path.abspath('../outputs/vec_text')
output_dir = os.path.abspath('../outputs/scikit_results')
model_save_dir = os.path.abspath('../outputs/scikit_models')

# Check and possibly create logs directory.
log_dir = os.path.join(output_dir, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Specify used classifiers.
classifiers = [
    ['NB-multi', MultinomialNB(alpha=1.0)],
    ['NB-berno', BernoulliNB()],
    ['MaxEnt', LogisticRegression()],
    ['CART', tree.DecisionTreeClassifier()],
    ['RandForest', RandomForestClassifier()],
    #['SVM', svm.SVC(verbose=False, kernel='rbf', cache_size=1024)],
    #['SVM', svm.SVC(verbose=False, kernel='poly', degree=3)],
]

# Create a Text writer object.
text_writer = TextWriter(output_dir)

# Results file - one for every document type.
# For every file, there is for every classifier one row in following format:
header_str = 'timestamp,input_file,doc_type,company,variable_type,days_delay,const_border_top,vector_type,' \
             'n_samples,n_features,class_1_test_samples,class_2_test_samples,' \
             'algo_name,accuracy,precision,recall,f1_score,train_time,test_time'
header_list = header_str.split(',')
# Special results name (include underscore).
r_description = ''

#### Execution parameters.

# Define processed folders.
input_dir_names = ['article', 'fb_com_10pd', 'fb_post', 'twitter_4']
input_dir_names = ['xtest']
input_directories = [os.path.join(base_input_dir, x) for x in input_dir_names]

# Save fitted model to disk?
SAVE_CLF_MODEL_TO_DISK = False

#######
# Execution
#######

for input_dir in input_directories:
    # Get directory name.
    input_dirname = os.path.basename(input_dir)
    print('======Processing %s======') % input_dirname

    # Prepare results and log file.
    res_filename = my_fp.get_or_create_results_file(input_dirname, output_dir, text_writer, header_list, r_description)
    log_filepath = my_fp.get_or_create_log_file(log_dir, input_dirname, r_description)

    # Process all SVMlight files in input directory.
    # They have name in following format: <doc type>_<all|company ID>_<price type>_<days_delay>_<const border top>_
    # <local weight-global weight-normalization>.SVMlight.dat
    for input_filename in sorted(os.listdir(input_dir)):
        if input_filename.endswith('.SVMlight.dat'):
            print('===%s===') % input_filename
            # Create path to file.
            input_filepath = os.path.join(input_dir, input_filename)
            # Check if file is not empty.
            if not my_fp.is_not_empty_file(input_filepath):
                print('File is empty, skipping it.')
                continue
            # Get basic file name.
            base_filename = input_filename.replace('.SVMlight.dat', '')
            # Load file into matrix.
            data_matrix = load_svmlight_file(input_filepath)
            n_samples = data_matrix[0].shape[0]
            n_features = data_matrix[0].shape[1]
            print('Number of samples/features: %d, %d') % (n_samples, n_features)
            # Prepare common info.
            file_features = my_fp.get_features_from_vector_filename(base_filename).values()
            common_data = [base_filename]
            common_data.extend(file_features)
            common_data.extend([n_samples, n_features])
            # Prepare data sets.
            X_train, X_test, y_train, y_test = cross_validation.train_test_split(data_matrix[0], data_matrix[1],
                                                                                 test_size=0.35, random_state=47)
            # Update log file.
            my_clf.update_log_header(log_filepath, input_filename, n_samples, n_features)
            # Analyze data with all classifiers.
            rows_algos = []
            for (clf_name, clf_object) in classifiers:
                # Prepare data.
                algo_row = list(common_data)
                algo_row.insert(0, str(datetime.datetime.now()))
                # Should the model be saved?
                if SAVE_CLF_MODEL_TO_DISK:
                    save_model_filepath = os.path.join(model_save_dir, base_filename + '.pkl')
                else:
                    save_model_filepath = False
                # Fit and predict data.
                try:
                    # Return [accuracy, precision, recall, f1 score, runtime] and [y_test, y_predicted]
                    clf_results, clf_eval_data, tested_counts = my_clf.classify_data(
                        clf_object, X_train, X_test, y_train, y_test, save_model_filepath)
                    print('%s: %s') % (clf_name, str([round(x, 4) for x in clf_results]))
                except Exception, e:
                    print('Exception occured: %s') % str(e)
                    my_clf.update_log_algo(log_filepath, clf_name, None, None, str(e))
                    continue
                # Insert number of tested samples (class 1 and 2).
                algo_row.extend(tested_counts)
                # Populate classification data row.
                algo_row.append(clf_name)
                algo_row.extend(clf_results)
                rows_algos.append(algo_row)
                # Save info to log file.
                my_clf.update_log_algo(log_filepath, clf_name, clf_results, clf_eval_data)

            # Save all results to file.
            text_writer.write_to_results_file(res_filename, rows_algos)
    # end
    print(">>>%s processing ended.") % input_dirname
