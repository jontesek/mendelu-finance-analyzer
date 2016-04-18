###########
# Imports
###########
import os
import subprocess

from src.vector_helpers import build_query_from_params, check_if_vector_file_exists

########
# Parameter definitions
########

# Set file paths
vectext_dir = os.path.abspath('VecText')
input_dir = os.path.abspath('../outputs/class_text')
output_dir = os.path.abspath('../outputs/vec_text')

# Specific run configurations for VecText.
run_configs = [
    {'conf_id': 'tp-no-no', 'local_weights': 'Binary (Term Presence)', 'global_weights': 'none', 'normalization': 'none'},
    {'conf_id': 'tf-idf-cos', 'local_weights': 'Term Frequency (TF)', 'global_weights': 'Inverse Document Frequency (IDF)', 'normalization': 'Cosine'},
]

# Specific configurations for min_document_frequency based on document type.
doc_freqs_param = {
    'article': 10, 'tweet': 5, 'fb-post': 5, 'fb-comment': 5,
}

# Common config parameters.
common_config = {
    'input_file': None, 'encoding': 'utf8', 'class_position': 1, 'output_dir': output_dir, 'output_file': None,
    'min_word_length': 2, 'min_document_frequency': 3, 'output_format': 'SVMlight', 'create_dictionary': 'no',
    'logarithm_type': 'natural', 'case': 'lower case', 'output_decimal_places': 3, 'sort_attributes': 'none',
    'subset_size': 100000, 'n_grams': 1,
}

# Change working directory to VecText.
os.chdir(vectext_dir)
FNULL = open(os.devnull, 'w')
suppress_output = False

# Document types.
doc_types = ['tweet', 'fb-post', 'fb-comment', 'article']

#######
# Performing part
#######

# Process all TEXT files in input directory.
# They have name in following format: <doc type>_<all|company ID>_<price type>_<days delay>_<const border top>.text
for d_type in doc_types:
    print("======Processing %s======") % d_type

    # Process all applicable files.
    for file_name in sorted(os.listdir(input_dir)):
        if file_name.startswith(d_type) and file_name.endswith('.text'):
            print('===%s===') % file_name
            # Create path to file.
            file_path = os.path.join(input_dir, file_name)
            base_name = os.path.splitext(file_name)[0]
            # Build a correct parameter query and run all configurations.
            for r_conf in run_configs:
                print(r_conf['conf_id'])
                if check_if_vector_file_exists(output_dir, base_name, r_conf['conf_id']):
                    print('Output SVMlight.dat file already exists, skipping it.')
                    continue
                # Choose corect parameters.
                all_params = common_config  # get template
                all_params.update(r_conf)   # run config
                all_params.update({'min_document_frequency': doc_freqs_param[d_type]})  # document frequency
                all_params.update({'input_file': file_path})    # path to input file
                out_filename = base_name + '_' + r_conf['conf_id']
                all_params.update({'output_file': out_filename})
                del(all_params['conf_id'])
                # Build a parameter query.
                p_query = build_query_from_params(all_params)
                # Run it with VecText.
                run_cmd = 'perl vectext-cmdline.pl ' + p_query
                if suppress_output:
                    ret_code = subprocess.call(run_cmd, shell=True, stdout=FNULL, stderr=FNULL)
                else:
                    ret_code = subprocess.call(run_cmd, shell=True)
                # ok
                print ret_code
