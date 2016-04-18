import os
import subprocess


def build_query_from_params(par_dict):
    query = ''
    for (par_name, par_value) in par_dict.items():
        query += '--%s="%s" ' % (par_name, par_value)
    return query


# Set file paths
vectext_dir = os.path.abspath('../libs/VecText')
input_dir = os.path.abspath('../../outputs/class_text')
output_dir = os.path.abspath('../../outputs/vec_text')

# Specific run configurations for VecText.
run_configs = [
    {'conf_id': 'tp-no-no', 'local_weights': 'Binary (Term Presence)', 'global_weights': 'none', 'normalization': 'none'},
    {'conf_id': 'tf-idf-cos', 'local_weights': 'Term Frequency (TF)', 'global_weights': 'Inverse Document Frequency (IDF)', 'normalization': 'Cosine'},
]

# Specific configurations for min_document_frequency based on document type.
doc_freqs_param = {
    'article': 50, 'tweet': 5, 'fb-post': 5, 'fb-comment': 5,
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

# Process all TEXT files in input directory.
# They have name in following format: <doc type>_<all|company ID>_<price type>_<days delay>_<const border top>.text
for file_name in os.listdir(input_dir):
    print('===%s===') % file_name
    if file_name.endswith('.text'):
        # Create path to file.
        file_path = os.path.join(input_dir, file_name)
        # Get info about documents in the file.
        base_name = os.path.splitext(file_name)[0]
        file_features = base_name.split('_')
        f_doc_type = file_features[0]
        # Skip unkwown doc types.
        if f_doc_type not in doc_freqs_param.keys():
            continue
        # Build a correct parameter query and run all configurations.
        for r_conf in run_configs:
            print(r_conf['conf_id'])
            # Choose corect parameters.
            all_params = common_config  # get template
            all_params.update(r_conf)   # run config
            all_params.update({'min_document_frequency': doc_freqs_param[f_doc_type]})  # document frequency
            all_params.update({'input_file': file_path})    # path to input file
            out_filename = base_name + '_' + r_conf['conf_id']
            all_params.update({'output_file': out_filename})
            del(all_params['conf_id'])
            # Build a parameter query.
            p_query = build_query_from_params(all_params)
            #print p_query
            # Run it with VecText.
            run_cmd = 'perl vectext-cmdline.pl ' + p_query
            ret_code = subprocess.call(run_cmd, shell=True, stdout=FNULL, stderr=FNULL)
            print ret_code
    break
