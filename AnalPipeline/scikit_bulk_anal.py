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

from src.TextWriter import TextWriter
import src.file_processing as my_fp
from src.classification import classify_data

########
# Parameter definitions
########

# File paths
vectext_dir = os.path.abspath('VecText')
input_dir = os.path.abspath('../outputs/vec_text/company_48')
output_dir = os.path.abspath('../outputs/scikit_results')

# Specify used classifiers.
classifiers = [
    ['NB-multi', MultinomialNB(alpha=1.0)],
    ['NB-berno', BernoulliNB()],
    ['MaxEnt', LogisticRegression()],
    ['CART', tree.DecisionTreeClassifier()],
    ['RandForest', RandomForestClassifier()],
]

# Document types.
#doc_types = ['article', 'test', 'tweet', 'fb-post', 'fb-comment', ]
doc_types = ['tweet']

# Text writer object
text_writer = TextWriter(output_dir)

# Results file - one for every document type.
# For every file, there is for every classifier one row in following format:
header_str = 'timestamp,input_file,doc_type,company,variable_type,days_delay,const_border_top,vector_type,n_samples,n_features,algo_name,accuracy,precision,recall,f1_score,runtime'
header_list = header_str.split(',')
# Edit document
r_description = ''

#######
# Performing part
#######

# Process all SVMlight files in input directory.
# They have name in following format: <doc type>_<all|company ID>_<price type>_<days delay>_<const border top>_
# <local weight-global weight-normalization>.SVMlight.dat
for d_type in doc_types:
    print('======Processing %s======') % d_type

    # Process all applicable files.
    for file_name in sorted(os.listdir(input_dir)):
        if file_name.startswith(d_type) and file_name.endswith('.SVMlight.dat'):
            print('===%s===') % file_name
            # Create path to file.
            file_path = os.path.join(input_dir, file_name)
            # Check if file is not empty.
            if not my_fp.is_not_empty_file(file_path):
                print('File is empty, skipping it.')
                continue
            # Check type of file and if corresponding results file exists.
            res_filename = my_fp.check_and_reset_results_file(file_name, output_dir, text_writer, header_list, r_description)
            # Get file name.
            base_filename = file_name.replace('.SVMlight.dat', '')
            # Load file into matrix.
            data_matrix = load_svmlight_file(file_path)
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
                                                                                 test_size=0.35, random_state=37)
            # Analyze data with all classifiers.
            rows_algos = []
            for (clf_name, clf_object) in classifiers:
                algo_row = list(common_data)
                algo_row.insert(0, str(datetime.datetime.now()))
                # Fit and predict data. Return accuracy, precision, recall, f1 score, runtime.
                clf_results = classify_data(clf_object, X_train, X_test, y_train, y_test)
                print('%s: %s') % (clf_name, str([round(x, 4) for x in clf_results]))
                # Populate row data.
                algo_row.append(clf_name)
                algo_row.extend(clf_results)
                rows_algos.append(algo_row)
            # Save results to file.
            text_writer.write_to_results_file(res_filename, rows_algos)
    # end
    print(">>>%s processing ended") % d_type
